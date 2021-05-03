from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):
    # ListView 는 자동적으로  template 을 찾는다 -->Rooms 앱이니까 ,room_list !!!!!!!!!!!!!!
    # 지금 이걸 읽고있으면 바로 위의 주석을 읽어라,
    """HomeView Definition"""

    # ListView 는 아래 를 자동으로 -->object_list 함 --> room_list 에서 바로 object_list 사용
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"  # object_list -> rooms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoomDatail(DetailView):

    """RoomDatail Definition"""

    # DetailView ---> arg 로 정확히 pk 가 와야함.
    # 잘못도니값 --> 알아서 Not Found 페이지로 보내 벌임
    model = models.Room
    print(model)
    pk_url_kwarg = "potato"
    # pk-->potato

    # templates/ 안해줘도 되는건가?

    # page_kwarg = "bitch" ?page= 대신에 "?bitch="

    # 지금 이걸 읽고있으면 제일 위의 주석을 읽어라,

    # ===========================================================
    # ===========ListView--Classy CBV////// ccbv.co.uk 참고------
    # ===========================================================
    # ===========ClassBasedBoew VS FunctionBasedView-------------
    # ===========================================================


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))  # pk 를 int 로 활용하여 check 하기 위해서
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {  # 고르는거
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {  # 디비에서 오는거
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},  # 둘을 합쳐서 보내는거 form+choices 풀어서 보내는 느낌임 **
    )
