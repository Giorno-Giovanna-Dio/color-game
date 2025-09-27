from rest_framework import serializers
from .models import GameSession, LevelResult, Leaderboard

class LevelResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelResult
        fields = ["level_index","grid_size","elapsed_ms","correct"]

class GameSessionSerializer(serializers.ModelSerializer):
    levels = LevelResultSerializer(many=True)
    class Meta:
        model = GameSession
        fields = ["id","started_at","finished_at","total_ms","levels"]

class LeaderboardSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ["nickname", "avatar", "best_total_ms", "updated_at"]

    def get_nickname(self, obj):
        profile = getattr(obj.user, "userprofile", None)
        if profile and profile.nickname:
            return profile.nickname
        return obj.user.username

    def get_avatar(self, obj):
        profile = getattr(obj.user, "userprofile", None)
        return profile.avatar if profile else ""