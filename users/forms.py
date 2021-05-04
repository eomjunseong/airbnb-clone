from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        # 정해져 있는 형식임 그대로 갖다 써야함,위와 맞추면됨
        # +, is_valid()할떄 검사됨
        # clean__  method : 에러 검사 + 정리--> return 안하면 그 영역 지움
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        print("2")