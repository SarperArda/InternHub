from django import template

register = template.Library()

@register.filter
def can_make_announcement(user):
    return user.role not in ["STUDENT", "INSTRUCTOR"]
