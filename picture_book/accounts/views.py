from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistForm, UserLoginForm, RequestPasswordResetForm,NewSetPasswordForm
from .models import PasswordResetToken
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
import logging
from django.utils import timezone
from datetime import timedelta

# アカウント作成
def regist(request):
    user_form = RegistForm(request.POST or None)
    if user_form.is_valid():
        user = user_form.save()
        login(request, user)
        messages.success(request,'アカウントが作成されました')
        return redirect ('picture_book_app:home')
    return render(request, 'accounts/registration.html', context={
        'user_form': user_form
    })
    
# ログイン
def user_login(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        # 認証処理
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            messages.success(request, 'ログインできました')
            return redirect('picture_book_app:home')
        else:
            messages.error(request,'メールアドレスまたはバスワードが間違っています')
    return render(request, 'accounts/login.html', context={
        'login_form': login_form
    })
    
# ログアウト
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:login')

# パスワード再設定
def request_password_reset(request):
    form = RequestPasswordResetForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        User = get_user_model()
        user = get_object_or_404(User, email=email)
        
        # メールアドレスをセッションに保存
        request.session['password_reset_email'] = email
        
        # 新しいトークン作成
        password_reset_token, created = PasswordResetToken.objects.get_or_create(user=user)
        if not created:
            password_reset_token.token = uuid.uuid4()
            password_reset_token.used = False
            password_reset_token.save()
        user.is_active = False
        user.save()
        
        # リセット用URL作成
        token = password_reset_token.token
        uidb64 = urlsafe_base64_encode(str(user.pk).encode())
        reset_url = request.build_absolute_uri(reverse('accounts:password_reset_confirm', args=[uidb64, token]))
        
        # メールの内容作成
        subject = '【お話の足跡】パスワード再設定のお知らせ'
        message = render_to_string('accounts/password_reset_email.html', context={
            'user':user,
            'reset_url':reset_url,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return redirect('accounts:password_reset_done')
    return render(request, 'accounts/password_reset_form.html', context={
        'reset_form':form
    })
    
# パスワード再設定リンク送信完了画面
def password_reset_done(request):
    email = request.session.get('password_reset_email', None)
    if email is None:
        email = 'メールアドレスを取得できませんでした'
    return render (request, 'accounts/password_reset_done.html', context={
        'email':email
    })

# 新しいパスワード再設定画面
logger = logging.getLogger(__name__)

def password_reset_confirm(request, token, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        logger.error(f"Password reset token does not exist or has already been used for token: {token} and user: {user.username}")
        return redirect('accounts:request_password_reset')
    
    logger.info(f"Token received: {token} for user: {user.username}")
    try:
        # パスワードリセットトークン取得
        password_reset_token = get_object_or_404(
            PasswordResetToken,
            token=token,
            user=user,
            used=False
        )
        logger.info(f"Password reset token found: {password_reset_token.token}")
        
        # トークンの期限切れか確認
        token_expiry = timedelta(minutes=10)
        if password_reset_token and (timezone.now() - password_reset_token.created_at > token_expiry):
            logger.error(f"Token {token} has expired for user: {user.username}")
            raise ValidationError('パスワードリセットリンクが無効です。再度パスワードリセットを試してください。')

    except PasswordResetToken.DoesNotExist:
        logger.error(f"Password reset token does not exist or has been used already for token: {token} and user: {user.username}")
        raise ValidationError('パスワードリセットリンクが無効です。再度パスワードリセットを試してください。')
        
    # トークンの有効性
    if not default_token_generator.check_token(user, token):
        logger.error(f"Invalid token: {token} for user: {user.username}")
        raise ValidationError('パスワードリセットリンクが無効です。再度パスワードリセットを試してください。')
    
    # パスワードのリセットのフォーム
    form = NewSetPasswordForm(request.POST or None, user=user)
    
    if form.is_valid():
        password = form.cleaned_data['new_password1']
        user.set_password(password)
        user.is_active = True
        user.save()
        
        # トークン使用済み
        password_reset_token = PasswordResetToken.objects.get(user=user, token=token)
        password_reset_token.used = True
        password_reset_token.save()
        
        return redirect('accounts:password_reset_complete')
    
    # パスワードのルール表示
    password_rules = [
        '●あなたの他の個人情報と似ているパスワードにはできません。',
        '●パスワードは最低 8 文字以上必要です。',
        '●使える文字は半角英数になります。',
        '●英大文字・小文字・数字を必ず含んでください。'
    ]
        
    return render(request, 'accounts/password_reset_confirm.html', context={
        'form':form,
        'password_rules':password_rules,
        'error_message': 'パスワードリセットリンクが無効です。再度パスワードリセットを試してください。',
    })

# パスワード再設定完了画面
def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')