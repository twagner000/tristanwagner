from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def percent(v,arg=None):
    mult,dec = (100,0) if not arg else map(int,arg.split(','))
    return ('{0:.'+str(dec)+'f}%').format(v*mult) if v is not None else None