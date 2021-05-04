from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    def get(self, request):

        form = forms.LoginForm(initial={"email": "um1129@naver.com"})

        return render(request, "users/login.html", {"form": form})

    def post(self, request):

        form = forms.LoginForm(request.POST)

        if form.is_valid():  # is_valid : LoginForm의 clean___: check
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


# 위 클래스는 아래와 같음
# def login_view(requset):
#    if requset.method=="GET":
#        pass
#    elif requset.method=="POST":


# 로그아웃 무조건 이렇게
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))