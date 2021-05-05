from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # AbstractUser 는  디비에 등록되지 않아  abstract이어어서

    """ Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),  # see Male , DB male
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGRAGE_ENGLISH = "en"
    LANGRAGE_KOREAN = "kr"

    LANGRAGE_CHOICES = ((LANGRAGE_ENGLISH, "English"), (LANGRAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGRAGE_CHOICES, max_length=2, blank=True, default=LANGRAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )

    superhost = models.BooleanField(default=False)
