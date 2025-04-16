from django.shortcuts import render, redirect, get_object_or_404
from .forms import(
    RegistForm, UserLoginForm, RequestPasswordResetForm,NewSetPasswordForm,
    FamilyRegistForm, UserUpdateForm,UserPasswordChangeForm,
    )
from .models import PasswordResetToken, Invitation
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
from django.core.exceptions import ValidationError
import logging
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import update_session_auth_hash



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
            password_reset_token.token = uuid.uuid4() # 独自トークンの発行
            password_reset_token.used = False
            password_reset_token.created_at = timezone.now()
            password_reset_token.save()
        user.is_active = False
        user.save()

        # リセット用URL作成
        token = password_reset_token.token
        uidb64 = urlsafe_base64_encode(str(user.pk).encode())
        reset_path = reverse('accounts:password_reset_confirm', args=[uidb64, token])
        reset_url = f"https://YukaMurata.pythonanywhere.com{reset_path}"

        # メールの内容作成
        subject = '【お話の足跡】パスワード再設定のお知らせ'
        message = render_to_string('accounts/password_reset_email.txt', context={
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
    context = {}
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
        logger.info(f"Token received: {token} for user: {user.username}")
            # トークンの有効性

        # if not default_token_generator.check_token(user, token):
        #    logger.error(f"Invalid token for uid: {uidb64} (user: {user.username})")
        #    raise ValidationError('パスワードリセットリンクが無効です。再度パスワードリセットを試してください。')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        logger.error(f"Password reset failed for token: {token} and uid: {uidb64} - {str(e)}")
        context['exception_notes'] = str(e)
        return render(request, 'accounts/request_password_reset.html', context)


    try:
        # パスワードリセットトークン取得
        password_reset_token = PasswordResetToken.objects.get(
        token=token,
        user=user,
        used=False
        )
        logger.info(f"Password reset token found: {password_reset_token.token}")


        # トークンの期限切れか確認　⇦ちゃんとチェックできてる
        token_expiry = timedelta(hours=1)
        if timezone.now() - password_reset_token.created_at > token_expiry:
            logger.error(f"Token {token} has expired for user: {user.username}")
            context['exception_notes'] = 'パスワードリセットリンクの有効期限が切れています。再度お試しください。'
            return render(request, 'accounts/request_password_reset.html', context)

    except PasswordResetToken.DoesNotExist:
        logger.error(f"Password reset token does not exist for uid: {uidb64}")
        context['exception_notes'] = 'パスワードリセットリンクが無効です。再度お試しください。'
        return render(request, 'accounts/request_password_reset.html', context)


    # パスワードのリセットのフォーム
    form = NewSetPasswordForm(request.POST or None, user=user)

    if request.method == 'POST' and form.is_valid():
        password = form.cleaned_data['password1']
        user.set_password(password)
        user.is_active = True
        user.save()

        # トークン使用済み
        password_reset_token.used = True
        password_reset_token.save()

        return redirect('accounts:password_reset_complete')

    # パスワードのルール表示
    password_rules = [
        'あなたの他の個人情報と似ているパスワードにはできません。',
        'パスワードは最低 8 文字以上必要です。',
        '使える文字は半角英数になります。',
        '英大文字・小文字・数字を必ず含んでください。'
    ]

    # エラーメッセージが存在する場合
    error_message = None
    if not form.is_valid() and 'new_password1' in form.errors:
        error_message = "入力内容に誤りがあります。再度確認してください。"

    return render(request, 'accounts/password_reset_confirm.html', context={
        'form':form,
        'password_rules':password_rules,
        'error_message':error_message,
    })

# パスワード再設定完了画面
def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')


# マイページ
@login_required
def mypage(request):
    return render(request, 'accounts/mypage.html')


# 家族招待URL画面の招待URLを作成
@login_required
def create_invitation(request):
    invitation_url = ''

    if request.method == 'POST':
        user = request.user
        family = user.family_id

        invitation = Invitation.objects.create(
            family_id = family,
            user_id = user,
            invite_token = uuid.uuid4()
        )
        # 招待URL作成
        invite_url = reverse('accounts:accept_invitation', kwargs={'invite_token':invitation.invite_token})
        invitation_url = request.build_absolute_uri(invite_url)


    return render(request, 'accounts/create_invitation.html', context={
        'invitation_url':invitation_url,
    })


# URLクリック→家族アカウント作成
def accept_invitation(request, invite_token):
    invitation = get_object_or_404(Invitation, invite_token=invite_token)

    # 招待が無効だった時
    if not invitation.is_valid():
        return redirect('accounts:invalid_invitation')

    # パスワードのルール表示
    password_rules = [
        'あなたの他の個人情報と似ているパスワードにはできません。',
        'パスワードは最低 8 文字以上必要です。',
        '使える文字は半角英数になります。',
        '英大文字・小文字・数字を必ず含んでください。'
    ]

    if request.method == 'POST':
        form = FamilyRegistForm(request.POST, family=invitation.family_id)
        if form.is_valid():
            # ユーザー作成
            user = form.save(commit=True)
            user.is_active = True
            user.save()


            # 招待を使用済みにする
            invitation.set_used()
            return redirect('picture_book_app:home')

        # アカウント登録が上手くいかなかったとき
        else:
            return render(request, 'accounts/family_registration.html', context={
                'form': form,
                'invitation':invitation,
                'password_rules': password_rules,
            })

    else:
        form = FamilyRegistForm()

    return render(request, 'accounts/family_registration.html', context={
        'form': form,
        'invitation':invitation,
        'password_rules': password_rules,
    })

# 招待が無効だった時
def invalid_invitation(request):
    return render(request, 'accounts/invalid_invitation.html')


# アカウント情報変更（名前・メールアドレス）
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:mypage')
    else:
        form = UserUpdateForm()
    return render (request, 'accounts/profile_update.html', context={
        'form': form,
    })

# アカウント情報の変更（パスワード）
@login_required
def password_change(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()

            # パスワード変更後もログイン状態を維持
            update_session_auth_hash(request, request.user)
            return redirect('accounts:mypage')

    else:
        form = UserPasswordChangeForm(user=request.user)
    return render(request, 'accounts/password_change.html', context={
        'form':form
    })

User = get_user_model()
# 家族一覧画面
@login_required
def family_list(request):

    family_id = request.user.family_id_id #
    print("Family ID:", family_id)
    members = User.objects.filter(family_id=family_id)
    print("Members:", members)

    return render(request, 'accounts/family_list.html', context={
        'members': members
    })


# 家族編集画面
@login_required
def family_update(request, pk):
    member = get_object_or_404(User, pk=pk)  #このUserは家族のことを指す

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=member)  #記入フォームが同じなのでUserUpdateForm使える
        if form.is_valid():
            form.save()
            return redirect('accounts:family_list')

    else:
        form = UserUpdateForm(instance=member)
        return render(request, 'accounts/family_update.html', context={
            'form': form,
            'member':member,
        })

# 家族削除
@login_required
def family_delete(request, pk):
    member = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        member.delete()
        return redirect('accounts:family_list')
    return render(request, 'accounts/family_update.html', context={
        'member':member,
    })

# トップ画面（ポートフォリオ）
def top(request):
    return render(request, 'top.html', context={
        'MEDIA_URL': settings.MEDIA_URL,
    })