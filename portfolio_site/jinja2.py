from jinja2 import Environment
from django.templatetags.static import static
from django.urls import reverse
from django.contrib.messages import get_messages


def url(viewname, *args, **kwargs):
    return reverse(viewname, args=args if args else None, kwargs=kwargs if kwargs else None)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': url,
        'get_messages': get_messages,
    })
    return env
