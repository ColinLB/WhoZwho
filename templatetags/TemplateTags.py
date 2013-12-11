from django import template
from WhoZwho.SessionFunctions import Age, Birthday, FamilyName, FormatAddress, PersonalContacts, PersonalName, Kids, Parents

register = template.Library()

@register.filter(name='Age')
def filter_Age(value, since=None):
    return Age(value, since)

@register.filter(name='Birthday')
def filter_Birthday(birthday):
    return Birthday(birthday)

@register.filter(name='FamilyName')
def filter_FamilyName(name, option='lastfirst', prefix=''):
    return FamilyName(name, option, prefix)

@register.filter(name='FormatAddress')
def filter_FormatAddress(address, prefix=''):
    return FormatAddress(address, prefix)

@register.filter(name='PersonalContacts')
def filter_PersonalContacts(name):
    return PersonalContacts(name)

@register.filter(name='PersonalName')
def filter_PersonalName(name, option='firstlast', prefix=''):
    return PersonalName(name, option, prefix)

@register.filter(name='Kids')
def filter_Kids(name, prefix=''):
    return Kids(name, prefix)

@register.filter(name='Parents')
def filter_Parents(name):
    return Parents(name)
