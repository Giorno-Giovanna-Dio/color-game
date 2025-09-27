from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from game.views import (
    StartSessionView,
    SubmitLevelView,
    FinishSessionView,
    LeaderboardListView,
    GoogleLoginView,
    SetNicknameView,
)

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # 遊戲 API
    path("api/", include("game.urls")),

    # Google OAuth (由 social_django 提供)
    path("auth/", include("social_django.urls", namespace="social")),

    path("api/google-login/", GoogleLoginView.as_view(), name="google_login"),

    # JWT Token API
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/set-nickname/", SetNicknameView.as_view(), name="set-nickname"),
]