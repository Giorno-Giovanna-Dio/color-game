import time, hmac, hashlib, os
from django.utils import timezone
from rest_framework import permissions, views, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import GameSession, LevelResult, Leaderboard
from .serializers import LeaderboardSerializer  # GameSessionSerializer 若目前沒用可先不匯入

from rest_framework.views import APIView
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from .models import UserProfile

import logging
logger = logging.getLogger(__name__)

SECRET = os.getenv("DJANGO_SECRET_KEY", "secret")

def make_checksum(payload: str) -> str:
    return hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()

def _user_or_none(request):
    return request.user if getattr(request.user, "is_authenticated", False) else None

def _uid_or_zero(request):
    return request.user.id if getattr(request.user, "is_authenticated", False) else 0

class StartSessionView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = GameSession.objects.create(user=_user_or_none(request))
        nonce = str(int(time.time() * 1000))
        sig = make_checksum(f"{s.id}:{nonce}:{_uid_or_zero(request)}")
        return Response({"session_id": s.id, "start_nonce": nonce, "sig": sig})

class SubmitLevelView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, session_id: int):
        session = get_object_or_404(GameSession, id=session_id)
        data = request.data  # 需包含: level_index, grid_size, elapsed_ms, correct
        LevelResult.objects.create(
            session=session,
            level_index=int(data.get("level_index")),
            grid_size=int(data.get("grid_size")),
            elapsed_ms=int(data.get("elapsed_ms")),
            correct=bool(data.get("correct")),
        )
        return Response({"ok": True})

class FinishSessionView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, session_id: int):

        logger.info(f"[FinishSession] raw user={request.user}, is_auth={request.user.is_authenticated}")

        session = get_object_or_404(GameSession, id=session_id)
        session.finished_at = timezone.now()
        session.total_ms = int(request.data.get("total_ms", 0))

        # 驗簽（匿名時 user_id=0）
        start_nonce = request.data.get("start_nonce", "")
        sig = request.data.get("sig", "")
        expect = make_checksum(f"{session.id}:{start_nonce}:{_uid_or_zero(request)}")
        if sig != expect:
            return Response({"detail": "bad signature"}, status=400)

        session.checksum = sig
        session.save()

        # 匿名就不寫排行榜；已登入才更新
        if getattr(request.user, "is_authenticated", False):
            lb, created = Leaderboard.objects.get_or_create(
                user=request.user, defaults={"best_total_ms": session.total_ms or 0}
            )
            logger.info(f"[FinishSession] user={request.user.id}, total_ms={session.total_ms}, lb_created={created}, lb_best={lb.best_total_ms}")

            if session.total_ms and (lb.best_total_ms == 0 or session.total_ms < lb.best_total_ms):
                lb.best_total_ms = session.total_ms
                lb.save()
                logger.info(f"[FinishSession] leaderboard updated for user={request.user.id}, best_total_ms={lb.best_total_ms}")

        return Response({"ok": True})

class LeaderboardListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LeaderboardSerializer
    def get_queryset(self):
        limit = int(self.request.query_params.get("limit", 50))
        return Leaderboard.objects.order_by("best_total_ms", "updated_at")[:limit]
    
class GoogleLoginView(APIView):
    
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.debug("[GoogleLoginView] post called ----------------------------------------")
        token = request.data.get("token")
        if not token:
            return Response({"error": "Missing token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            )

            email = idinfo["email"]
            name = idinfo.get("name", email.split("@")[0])
            picture = idinfo.get("picture", "")

            # 建立/取得 User
            user, created = User.objects.get_or_create(username=email, defaults={"email": email})

            # 建立/更新 UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if picture:
                profile.avatar = picture
            profile.save()

            logger.info(f"[GoogleLoginView] login success: {email}, created_user={created}, profile_id={profile.id}")

            # 頒發 JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "name": name,
                "email": email,
                "avatar": profile.avatar,
                "nickname": profile.nickname,
            })
        
        except Exception as e:
            logger.exception("[GoogleLoginView] token verification failed")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class SetNicknameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nickname = request.data.get("nickname")
        if not nickname:
            return Response({"error": "Missssssing nickname"}, status=400)

        # 檢查是否重複（避免兩人同名）
        if UserProfile.objects.filter(nickname=nickname).exclude(user=request.user).exists():
            return Response({"error": "Nickname already taken"}, status=400)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.nickname = nickname
        if "avatar" in request.data:
            profile.avatar = request.data["avatar"]
        profile.save()

        return Response({
            "ok": True,
            "nickname": profile.nickname,
            "avatar": profile.avatar,
        })