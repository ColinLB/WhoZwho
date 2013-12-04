from django import template
from WhoZwho.SessionFunctions import Age

register = template.Library()

@register.filter(name='Age')
def filter_Age(value, since=None):
    return Age(value, since)
