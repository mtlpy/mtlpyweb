from datetime import datetime

from django.conf import settings


def extra_context(request):
    return {
        "GOOGLE_ANALYTICS": getattr(settings, "GOOGLE_ANALYTICS"),
        "SITENAME": getattr(settings, "SITENAME"),
        "YEAR": datetime.now().year
    }
