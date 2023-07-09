from django import template

from datetime import datetime

register = template.Library()

@register.filter(name='initials')
def initials(value):
    initials = ''

    for name in value.split(' '):
        if name and len(initials) < 3:
            initials += name[0].upper()
    
    return initials

@register.filter(name='convert_to_24hr')
def convert_to_24hr(time_value):
    time_str = time_value.strftime('%I:%M %p')
    converted_time = datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
    return converted_time