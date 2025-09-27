from django.contrib import admin
from .models import UserProfile, GameSession, LevelResult, Leaderboard

admin.site.register(UserProfile)
admin.site.register(GameSession)
admin.site.register(LevelResult)
admin.site.register(Leaderboard)