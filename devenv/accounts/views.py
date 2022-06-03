from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin  # ログインしたユーザだけ閲覧できるように制限するクラス
from django.contrib.auth.views import(LoginView, LogoutView)  # ログイン、ログアウト機能
from .forms import LoginForm


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'track/index.html'