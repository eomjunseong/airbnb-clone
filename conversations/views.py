from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView
from django.shortcuts import render
from users import models as user_models
from . import models


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)

    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)  # add many to many ..?
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))

        # 25.7
        # conversation = models.Conversation.objects.get(
        #     Q(participants=user_one)
        #     & Q(participants=user_two)
        #     # Q object -->| & 사용가능 검색해 보기
        # )

        print(conversation)


class ConversationDetailView(DetailView):
    # DetailView 는 defualt로  url 에서 pk 를 찾아줌
    model = models.Conversation