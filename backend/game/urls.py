# urls.py
from django.urls import path
from .views import StartSessionView, SubmitLevelView, FinishSessionView, LeaderboardListView


urlpatterns = [
    path("session/start/", StartSessionView.as_view()),
    path("session/<int:session_id>/level", SubmitLevelView.as_view()),
    path("session/<int:session_id>/finish", FinishSessionView.as_view()),
    path("leaderboard/", LeaderboardListView.as_view()),
    
]