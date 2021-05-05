from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # 정해져 있는 형식임 그대로 갖다 써야함,위와 맞추면됨
        # +, is_valid()할떄 검사됨
        # clean__email...  method : 에러 검사 + 정리--> return 안하면 그 영역 지움
        # 걍 clean 은 한번에 통합 느낌 --> error 직접 추가
        email = self.cleaned_data.get("email")
        passowrd = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(passowrd):
                return (
                    self.cleaned_data
                )  # def clean: 을 했으면 무조건 self.cleaned_data return해야함
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        # password 는 유저가 갖고있지 않음 그래서 밖으로 뺌

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # clean_email은 ModelForm이 알아서함 .
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # Override
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()