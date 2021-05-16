from django import template

register = template.Library()


@register.filter()
def sexy_capitals(value):
    return value.capitalize()

    # 즉 필터이름과 함수 이름이 같으면 필터이름 생략가능
    # def werid_name(value): --> @register.filter(name=sexy_capitals) 이라고 해줘야 사용가능