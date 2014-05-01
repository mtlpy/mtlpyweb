# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time
import re
from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from BeautifulSoup import BeautifulStoneSoup

from mtlpy.users.models import MtlPyUser
from mtlpy.blog.models import Post, Category

def get_author(username):
    try:
        return MtlPyUser.objects.get(username=username)
    except MtlPyUser.DoesNotExist:
        return MtlPyUser.objects.create(
            username=username,
            password='!', # Disable password import
        )

def get_category(slug, english, french):
    cat, is_new = Category.objects.get_or_create(
        slug=slug,
        title_en=english,
        title_fr=french
    )
    return cat

def create_post(english, french):
    french_title = french.title()

    if english.is_event():
        category = get_category('event', 'Event', 'Évènement')
    elif english.is_workshop():
        category = get_category('workshop', 'Tutorials/Workshops', 'Tutorat/Ateliers')
    else:
        category = next(english.category())
        for slug, name in french.category():
            if slug == category[0]:
                fr_name = name
                break
        else:
            raise Exception("Cannot find category in french for %s/%s for post %s" % (slug, name, english.title()))

        category = get_category(
            category[0], category[1], fr_name
        )

    content = english.content()

    data = dict(
        status=2,
        title_fr=french.title(),
        title_en=english.title(),
        publish=english.publish_date(),
        author=get_author(english.author()),
        slug=english.slug(),
        content_en=content['en'],
        content_fr=content['fr'],
        category=category,
    )
    post = Post.objects.create(**data)

    return post
    

def import_post_bad(md, orig_text):
    author = get_or_create_author(md.Meta['author'][0])
    category = _get_or_create_category(md.Meta['category'][0])
    date = datetime.strptime(md.Meta['date'][0], '%Y-%m-%d %H:%M')
    slug = md.Meta['slug'][0]
    lang = md.Meta['lang'][0]
    title = md.Meta['title'][0]
    post, is_new = Post.objects.get_or_create(publish=date, slug=slug,
                                              author=author, category=category)
    setattr(post, 'content_' + lang, orig_text)
    setattr(post, 'title_' + lang, title)
    post.save()

class Item(object):
    SPLIT_CONTENT = re.compile('<!--:(?P<lang>..)-->(?P<content>.*?)<!--:-->', re.DOTALL)

    def __init__(self, bs_item):
        self.bs_item = bs_item

    def _get_text(self, key):
        return self.bs_item.fetch(key)[0].text

    def is_published(self):
        return self._get_text('wp:status') == 'publish'

    def is_post(self):
        return True

    def link(self):
        return self._get_text('link')

    def title(self):
        return self._get_text('title')

    def publish_date(self):
        raw_date = self._get_text('wp:post_date')
        return datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")

    def author(self):
        return self._get_text('dc:creator')

    def category(self):
        for cat in self.bs_item.fetch(domain='category'):
            yield slugify(cat.get('nicename')), cat.text

    def is_event(self):
        for slug, name in self.category():
            if slug == 'events':
                return True
        return False

    def is_workshop(self):
        for slug, name in self.category():
            if slug == 'tutorialsworkshops':
                return True
        return False


    def slug(self):
        return self._get_text('wp:post_name')

    def content(self):
        text = self._get_text('content:encoded')

        matches = self.SPLIT_CONTENT.findall(text)
        if len(matches) == 0:
            # Some old posts don't have french and english translations
            return {'en': text, 'fr': text}
        if len(matches) == 1:
            # Some posts only have one language
            content = matches[0][1]
            return {'en': content, 'fr': content}
        else:
            return dict(matches)

    @classmethod
    def item_dict(cls, items, verbose=False):
        seen = set([])
        for raw_item in items:
            item = cls(raw_item)
            if verbose:
                print item.link()
            if item.is_post() and item.is_published():
                assert item.link() not in seen
                yield item.link(), item


def read_items(xml_file_path, verbose=False):
    with open(xml_file_path, 'rb') as xmlfile:
        soup = BeautifulStoneSoup(xmlfile)
        return list(soup.rss.channel.findAll('item'))

class Command(BaseCommand):
    help = (
        'Import blog posts from the french and english wordpress dumps '
        'to create the blog posts.\n\nUsage:\n\timportxml ENGLISH_DUMP '
        'FRENCH_DUMP'
       )

    option_list = BaseCommand.option_list + (
        make_option(
            '--verbose',
            action='store_true',
            default=False,
            help='Make the loader print out what it is doing'
        ),
    )

    def handle(self, *args, **options):
        english_dump, french_dump = args
        verbose = options.get('verbose', False)
        seen = set([])

        english_items = dict(Item.item_dict(read_items(english_dump), verbose))
        french_items = dict(Item.item_dict(read_items(french_dump), verbose))
        assert set(english_items.keys()) == set(french_items.keys())

        answer = raw_input(
            'This will delete all pre-existing blog posts! Are you sure you '
            'want to continue?\n(Type "I am sure" to continue.)\n'
        )
        assert answer.lower() == 'i am sure', 'Stopping the import'

        Category.objects.all().delete()
        Post.objects.all().delete()

        for i, (link, english) in enumerate(english_items.items()):
            french = french_items[link]
            try:
                post = create_post(english, french)
            except:
                print "Problem importing ({}) {}".format(i, link)
                raise
