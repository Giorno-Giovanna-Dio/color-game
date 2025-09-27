# game/views_auth.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            # 驗證 Google token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

            email = idinfo["email"]
            username = email.split("@")[0]

            # 找到或建立使用者
            user, _ = User.objects.get_or_create(username=username, defaults={"email": email})

            # 簽發 JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)