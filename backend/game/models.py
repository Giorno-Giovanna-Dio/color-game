from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.nickname or self.user.username

class GameSession(models.Model):
    """
    一次從第1關玩到結束（或中途結束）的紀錄。
    """
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    total_ms = models.IntegerField(default=0)  # 前端送上來的總用時（毫秒）
    checksum = models.CharField(max_length=64, blank=True, default="")  # 簽章防作弊（可選）

class LevelResult(models.Model):

    session = models.ForeignKey(GameSession,  null=True, blank=True, on_delete=models.SET_NULL)
    level_index = models.IntegerField()  # 1..8
    grid_size = models.IntegerField()   # 3..10
    elapsed_ms = models.IntegerField()  # 該關用時
    correct = models.BooleanField(default=False)

class Leaderboard(models.Model):
    """
    存最佳成績：總用時越少越好。
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    best_total_ms = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["best_total_ms", "updated_at"]),
        ]