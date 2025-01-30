from django import template
import math

register = template.Library()

@register.filter(name='stars')
def stars(value):
    filled_stars = math.ceil(float(value) * 5)
    return range(filled_stars)

@register.filter(name='empty_stars')
def empty_stars(value):
    filled_stars = math.ceil(float(value) * 5)
    empty = 5 - filled_stars
    return range(empty)