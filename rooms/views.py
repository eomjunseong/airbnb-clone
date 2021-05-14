from django.http.response import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):
    # ListView 는 자동적으로  template 을 찾는다 -->Rooms 앱이니까 ,room_list !!!!!!!!!!!!!!
    # 지금 이걸 읽고있으면 바로 위의 주석을 읽어라,
    """HomeView Definition"""

    # ListView 는 아래 를 자동으로 -->object_list 함
    # --> room_list 에서 바로 object_list 사용
    model = models.Room
    paginate_by = 12  # -->page_obj 사용 바로 가능
    paginate_orphans = 5
    context_object_name = "rooms"  # object_list -> rooms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoomDetail(DetailView):

    """RoomDatail Definition"""

    # DetailView ---> arg 로 정확히 pk 가 와야함.
    # 잘못된 값 --> 알아서 Not Found 페이지로 보내 벌임
    model = models.Room


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                print(form)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                print(country)

                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})

        else:
            form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):  # 이게 원래 디폴트로 방찾는데 오버라이딩중
        room = super().get_object(queryset=queryset)  # pk 통해 방찾아옴
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room  # 원래 역할이 방 반환


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    # detailview pk defualt
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):  # 이게 원래 디폴트로 방찾는데 오버라이딩중
        room = super().get_object(queryset=queryset)  # pk 통해 방찾아옴
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room  # 원래 역할이 방 반환


@login_required
def delete_photo(request, room_pk, photo_pk):

    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            # photo = models.Photo
            # photo.delete()
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    # 이게 있어야  model = models.Photo 작동/ 디폴트 pk라 /
    # 내 url에 pk 가 없어서 해줬음
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "Photo updated"  # import SuccessMessageMixin

    # success_url = reverse_lazy("") --> 로직으로 구현해보자 .

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")  # 룸키 얻기위해..
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    # model = models.Photo-->필요없음  이거 createview 에서 필요한거인듯..?

    template_name = "rooms/photo_create.html"
    # fields = ("caption", "file") -->필요없음
    form_class = forms.CreatePhotoForm

    # form_valid : 는 항상 httpresponse를 반환함
    # 빨간 form  -->form_class
    def form_valid(self, form):
        pk = self.kwargs.get("pk")  # 여기서 kwargs 사용한이유 찾기
        form.save(pk)  # 이게 작동해야 form.createphotoform.에서 pk 사용가능// 토스임
        messages.success(self.request, "Photo Uploaded")
        # SuccessMessageMixin 쓰면 -->form_valid를 쓸수가없다.....뭔소리야진짜...
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    # 빨간 form  -->form_class
    def form_valid(self, form):
        # 기존 방법
        # form.save(self.reqeust.user)
        room = form.save()
        room.host = self.request.user
        room.save()  ####!!!!!!!!!!중요
        form.save_m2m()
        messages.success(self.request, "Room Uploaded")
        # room.pk로 리다이랙트하기위해서
        # AddPhotoView 와는 다른구성을 갖게헀음
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))