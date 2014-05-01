from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'mtlpy.blog.views',
    url(r'^$', 'home'),
    url(r'^(?P<year>\d{4})/$', 'archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'archive'),
)
