from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# PasswordResetTokenのモデルが必要
class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
