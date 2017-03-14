from django.contrib.flatpages.views import render_flatpage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import get_current_site
from django.utils.translation import get_language
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect)
from .models import I18NFlatPage as FlatPage


def i18n_flatpage(request, url):
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(
            FlatPage,
            url__exact=url,
            sites__id__exact=site_id,
            language=get_language()[:2],
        )
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(FlatPage,
                url__exact=url, sites__id__exact=site_id)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_flatpage(request, f)
