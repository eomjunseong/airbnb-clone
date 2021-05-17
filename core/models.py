from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    """ Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)  # 새로운 model 생성할때 자동 주입
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:  # 확장용  이설정을 안해주면 디비에 이것 자체가 등록이 되어벌임 우리는 이걸 원하지 않음
        abstract = True


# 수정일자 : auto_now=True 사용
# auto_now=True 는 django model 이 save 될 때마다 현재날짜(date.today()) 로 갱신됩니다.
# 주로 최종수정일자 field option 으로 주로 사용됩니다.
# 생성일자 : auto_now_add=True 사용
# auto_now_add=True 는 django model 이 최초 저장(insert) 시에만 현재날짜(date.today()) 를 적용합니다.
