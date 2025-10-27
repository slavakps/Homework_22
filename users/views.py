from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(CreateView):
    """Представление для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Обработка успешной регистрации"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Регистрация прошла успешно! Проверьте вашу почту для приветственного письма.'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок регистрации"""
        messages.error(
            self.request,
            'Ошибка регистрации. Проверьте введенные данные.'
        )
        return super().form_invalid(form)


def login_view(request):
    """Представление для авторизации пользователя"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.email}!')
                return redirect('catalog:home')
            else:
                messages.error(request, 'Неверный email или пароль.')
        else:
            messages.error(request, 'Ошибка входа. Проверьте данные.')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """Представление для выхода из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('catalog:home')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Представление для профиля пользователя"""
    template_name = 'profile.html'
    login_url = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context