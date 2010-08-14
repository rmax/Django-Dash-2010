from django.conf import settings
from django.template import Library

UNSAFE_PATHS = getattr(settings, 'UNSAFE_PATHS', [])

def unsafepath(value):
    """
    Removes sensitive path information from given path
    """
    for path in UNSAFE_PATHS:
        if value.startswith(path):
            return value[len(path):]

    return value

register = Library()
register.filter(unsafepath)
