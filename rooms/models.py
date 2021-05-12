from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models


# abstractiem 은 name만을 위한 item임
# ----type의 유형을 위해서만 만듬
class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)  # user와 연결

    # related_name="rooms" --> user.room_set 대신 user.rooms 가능
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # user와 연결
    # room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # amenities = models.ManyToManyField(Amenity, blank=True)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    # facilities = models.ManyToManyField(Facility, blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    # house_rules = models.ManyToManyField(HouseRule, blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # OCP # admin 에서의 save_model 과 다름 !!
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # 이건 모델을 컨트롤 하는 느낌 , save_model 은 admin을 컨트롤함

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratrings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratrings += review.rating_average()
            # return all_ratrings / len(all_reviews)
            return round(all_ratrings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        # unpacking value
        (photo,) = self.photos.all()[:1]
        return photo.file.url
        # print(photo.file.url)#/media/room_photos/25.webp

    def get_next_four_photoes(self):
        photos = self.photos.all()[1:5]
        return photos
