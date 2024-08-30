from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm, EditProfileForm
from .models import Profile


def register_view(request):
    # проверка запроса на пост
    if request.method == 'POST':
        # передача данный в форму
        form = RegisterForm(data=request.POST)
        # проверка форы на валидность
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            # redirect -> функция для перенаправления на другой url адрес

            messages.success(request, 'Вы зарегистрировались')
            return redirect('login_path')
        else:
            messages.error(request, 'Вы допустили ошибку')
            return redirect('register_path')
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'title': 'Зарегистрироваться'
    }
    return render(request, 'account/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # get_user -> метод для получения пользователя
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы вошли в аккаунт')
                return redirect('index_path')
        else:
            messages.error(request, 'Вы допустили ошибку')
            return redirect('login_path')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Войти в аккаунт'
    }
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунт')
    return redirect('index_path')


def show_profile_view(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    content = {
        'profile': profile
    }
    return render(request, 'account/profile.html', content)


class EditProfileView(UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'account/edit_profile.html'
    extra_context = {
        'title': 'Изменение профиля'
    }

    def get_success_url(self):
        return reverse_lazy('show_profile_path', kwargs={'user_id': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)
