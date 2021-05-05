from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm  # LoginForm() 아님 LoginForm임
    success_url = reverse_lazy("core:home")
    initial = {"email": "um1129@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)  # success_url 작동


# 로그아웃 무조건 이렇게
# 근데 또 이게 LogoutView로 가능 .. ㅅㅂ
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm  # LoginForm() 아님 LoginForm임
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "eom",
        "last_name": "jun",
        "email": "e1@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)