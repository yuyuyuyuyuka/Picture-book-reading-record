from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid


class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        if not password:
            raise ValueError('パスワードを入力してください')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_active'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, username, password, **extra_fields)
    

# ユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):
    family_id = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


User = get_user_model()

# PasswordResetTokenのモデルが必要
# パスワード再設定
class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"


# 家族モデル
class Family(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Family {self.id}'

