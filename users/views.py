from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):

        form = forms.LoginForm(initial={"email": "itn@las.com"})

        return render(request, "users/login.html", {"form": form})

    def post(self, request):

        form = forms.LoginForm(request.POST)

        if form.is_valid():  # is_valid : LoginForm의 clean___: check
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})


# 위 클래스는 아래와 같음
# def login_view(requset):
#    if requset.method=="GET":
#        pass
#    elif requset.method=="POST":
