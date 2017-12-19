# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import re

from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_control
from django.views.static import serve as static_view


def media():
    return serve(settings.MEDIA_URL, settings.MEDIA_ROOT)


def serve(prefix, document_root):
    pattern = r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/'))
    kwargs = {'document_root': document_root}

    view = static_view
    if not settings.DEBUG:
        view = permanent_public_cache(view)

    return url(pattern, view, kwargs=kwargs)


def permanent_public_cache(view):
    one_year = 60 * 60 * 24 * 365
    decorator = cache_control(public=True, max_age=one_year)
    return decorator(view)
