from django import template

register = template.Library()


@register.filter(name="duration_string")
def duration_string(value):
    hours, remainder = divmod(value.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02} heures, {:02} minutes et {:02} secondes".format(
        hours, minutes, seconds
    )
