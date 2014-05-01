# -*- coding: utf-8 -*-

import arrow
import datetime

from django.template import Library
from django.utils.translation import get_language


register = Library()


@register.filter
def humanize_date(date):
    if isinstance(date, datetime.date):
        date = datetime.datetime(date.year, date.month, date.day)

    locale = get_language().split('-')[0] # transforming 'en-us' into 'en'

    return arrow.get(date).humanize(locale=locale)

