from hashlib import md5

from django.template import Library


register = Library()


@register.filter
def email_hash(user):
    return md5(user.email).hexdigest()
