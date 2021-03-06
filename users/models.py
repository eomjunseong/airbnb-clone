import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string  # template을 load해서 render 하는거임
from core import managers as core_managers


class User(AbstractUser):
    # AbstractUser 는  디비에 등록되지 않아  abstract이어어서

    """ Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),  # see Male , DB male
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGRAGE_ENGLISH = "en"
    LANGRAGE_KOREAN = "kr"

    LANGRAGE_CHOICES = (
        (LANGRAGE_ENGLISH, _("English")),
        (LANGRAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGING_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGING_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(_("bio"), blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        _("language"),
        choices=LANGRAGE_CHOICES,
        max_length=2,
        blank=True,
        default=LANGRAGE_KOREAN,
    )

    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )

    superhost = models.BooleanField(default=False)

    # 16
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    # 17
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    # 25.7
    objects = core_managers.CustomUserManager()

    # 16
    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                _("Verify Airbnb Account"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

    # 21 --> 덤으로 admin panel 에도 새로운 버튼이 생김
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
