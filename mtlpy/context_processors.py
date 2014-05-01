from django.conf import settings

def extra_context(request):
    return {
        "DISQUS_SITENAME": getattr(settings, "DISQUS_SITENAME"),
        "GOOGLE_ANALYTICS": getattr(settings, "GOOGLE_ANALYTICS"),
        "SITENAME": getattr(settings, "SITENAME"),
    }
