from hashlib import md5

from django.template import Library


register = Library()


@register.filter
def email_hash(user):
    if user.email:
        return md5(user.email.encode('utf-8')).hexdigest()
