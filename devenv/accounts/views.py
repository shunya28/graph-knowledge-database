from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin  # ログインしたユーザだけ閲覧できるように制限するクラス
from django.contrib.auth.views import LoginView, LogoutView  # ログイン、ログアウト機能
from .forms import LoginForm, UserCreateForm
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/login.html'


class Signup(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()

            # フォームから'username'を読み取る
            username = form.cleaned_data.get('username')

            # フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'accounts/signup.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'accounts/signup.html', {'form': form, })


# create_account = Create_account.as_view()
