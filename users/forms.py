from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Введите ваш email'}))

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'}))

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        """Сохраняет пользователя и отправляет приветственное письмо"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            self._send_welcome_email(user)

        return user

    def _send_welcome_email(self, user):
        """Отправляет приветственное письмо пользователю"""
        subject = 'Добро пожаловать в Skystore!'
        message = f'''Здравствуйте, {user.email}! Добро пожаловать в Skystore! Ваш аккаунт был успешно создан.'''

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,)
        except Exception as e:
            print(f"Ошибка отправки email: {e}")


class UserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя"""

    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'}))

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'}))

    class Meta:
        fields = ('username', 'password')