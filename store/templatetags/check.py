from django import template

register = template.Library()

@register.filter(name="check_admin")
def check_admin(groups):
    # print("check-admin")
    for group in groups:
        if "admin" == group.name:
            return True
    return False
