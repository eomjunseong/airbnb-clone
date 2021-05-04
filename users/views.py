from django.views import View
from django.shortcuts import render


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        pass


# 위 클래스는 아래와 같음
# def login_view(requset):
#    if requset.method=="GET":
#        pass
#    elif requset.method=="POST":
