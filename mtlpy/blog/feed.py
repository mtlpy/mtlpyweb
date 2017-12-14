from datetime import datetime

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy

from mtlpy.blog.models import Post


class BlogEntriesFeed(Feed):
    title = u"Montréal-Python"
    link = "/feed/"
    description = u"News from the Montréal-Python community"

    def items(self):
        return Post.objects.order_by('-publish')[:5]

    def item_pubdate(self, item):
        return datetime.combine(item.publish, datetime.min.time())

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html_content()

    # item_link is only needed if NewsItem has no get_absolute_url
    # method.
    def item_link(self, item):
        return reverse_lazy('blog_detail', kwargs={
            'year': item.publish.year,
            'month': item.publish.strftime('%m').lower(),
            'slug': item.slug})
