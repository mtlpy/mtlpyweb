from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from mtlpy.blog.feed import BlogEntriesFeed

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',  'mtlpy.views.home_page', name='home_page'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        'mtlpy.blog.views.post', name='blog_detail'),
    url(r'^blog/transfer_tool/$', 'mtlpy.blog.views.transfer_posts_tool',
        name='transfer_tool'),
    url(r'^blog/(?P<slug>[-\w|\W]+)/$', 'mtlpy.blog.views.category',
        name='blog_category'),
    url(r'^blog/$', 'mtlpy.blog.views.category', name='blog'),
    url(r'^user/(?P<userid>\d+)/$', 'mtlpy.blog.views.user_posts',
        name='user_posts'),
    url(r'^sponsor/(?P<slug>[-\w|\W]+)/$', 'mtlpy.views.sponsor_details',
        name='sponsor_details'),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^styleguide', 'mtlpy.views.styleguide'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^contact/', 'mtlpy.views.contact', name='contact'),
    url(r'^videos/', 'mtlpy.views.videos', name='videos'),
    url(r'^sponsorship/', 'mtlpy.views.sponsorship', name='sponsorship'),
    url(r'^feed/$', BlogEntriesFeed(), name="feed")
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    '',
    url(r'^(?P<url>.*)$', 'mtlpy.pages.views.i18n_flatpage', name='flatpage'),
)
