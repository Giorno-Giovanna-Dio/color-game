# backend/auth_urls.py
from django.urls import path
from .oauth_views import google_login_url, google_callback, exchange_tokens

urlpatterns = [
  path("google/url", google_login_url),
  path("google/callback", google_callback),
  path("google/exchange", exchange_tokens),
]