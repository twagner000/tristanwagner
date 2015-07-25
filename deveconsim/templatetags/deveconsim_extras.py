from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def percent(v,dec=0):
    return ('{0:.'+str(dec)+'%}').format(v) if v or v==0 else None

@register.filter
def percentint(v):
    return ('{0:.0%}').format(v/100) if v or v==0 else None

@register.filter    
def currency(v,arg=None): #couldn't figure out how to adjust decimals for locale.currency
    divs = {'K':10**3, 'M':10**6, 'B':10**9}
    dec,div = (arg+',').split(',')[:2] if arg else ('0','')
    if v or v==0:
        s = ('${0:,.'+dec+'f}').format(abs(v)/divs.get(div,1))
        if div:
            s = '{0} {1}'.format(s,div)
        if v<0:
            s = '<span class=\"neg-currency\">({0})</span>'.format(s)
        return mark_safe(s)
    return None
    