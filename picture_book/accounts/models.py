from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
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

        # family_id を事前に設定
        family = extra_fields.pop('family_id', None)
        if not family:
            # family_id が指定されていない場合、招待されたユーザーの family_id を設定
            family = extra_fields.get('family_id')
            if not family:
                family = Family.objects.first()
                if not family:
                    family = Family.objects.create()

        # family_id を含めて User インスタンスを作成
        user = self.model(email=email, username=username, family_id=family, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        # family_id を設定
        family = extra_fields.pop('family_id', None)
        if not family:
            family = Family.objects.first()
            if not family:
                family = Family.objects.create()
        extra_fields['family_id'] = family

        return self.create_user(email, username, password, **extra_fields)
    
    

# ユーザーモデル
class User(AbstractBaseUser, PermissionsMixin):
    family_id = models.ForeignKey('Family', on_delete=models.CASCADE, null=False, blank=False)
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

# 家族招待モデル
class Invitation(models.Model):
    family_id = models.ForeignKey('Family', on_delete=models.CASCADE, related_name='family_invitations', default=1)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_invitations', default=1)
    invite_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def get_expiry_data():
        return timezone.now()+timedelta(days=1)
    
    expiry_date = models.DateTimeField(default=get_expiry_data)
    
    STATUS_CHOICES = (
        (0, '未使用'),
        (1, '使用済み'),
        (2, '期限切れ'),
    )
    
    used = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    # 招待の状態
    # 未使用かつ現在時刻より有効期限が前であれば招待OK
    def is_valid(self):
        return self.used ==0 and timezone.now() < self.expiry_date
    
    # 使用済み
    def set_used(self):
        self.used = 1
        self.save()
        
    # 期限切れ
    def set_expired(self):
        self.used = 2
        self.save()
        
    def __str__(self):
        return f"招待トークン {self.invite_token} - {self.get_used_display()}"

