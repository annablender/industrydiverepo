from django import template
from django.contrib import messages

register = template.Library()


@register.simple_tag
def example_alert(request):
    messages.add_message(request, messages.ERROR, 'There is no cover story!')
