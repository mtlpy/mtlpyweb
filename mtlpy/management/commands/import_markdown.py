# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import codecs
import markdown
import os
import re

from datetime import datetime
from optparse import make_option

from mtlpy.users.models import MtlPyUser
from django.core.management.base import BaseCommand, CommandError

from mtlpy.blog.models import Post, Category


def get_or_create_author(username):
    try:
        return MtlPyUser.objects.get(username=username)
    except MtlPyUser.DoesNotExist:
        return MtlPyUser.objects.create(
            username=username,
            password='!', # Disable password import
        )

def _get_or_create_category(text):
    cat, is_new = Category.objects.get_or_create(slug=text)
    return cat


def import_post(md, orig_text):
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


class Command(BaseCommand):
    help = 'Import all markdown files into the blog post DB'

    option_list = BaseCommand.option_list + (
        make_option('--rootpath',
                    action='store',
                    dest='rootpath',
                    default='data',
                    help='root path (default: working directory)'),
        make_option('--verbose',
                    action='store_true',
                    default=False,
                    help='Make the loader print out what it is doing'),
    )

    def handle(self, *args, **options):
        root_path = options['rootpath'] or os.getcwd()
        md = markdown.Markdown(extensions=['meta', 'nl2br'])

        answer = raw_input('This will delete all pre-existing blog posts! Are you sure you want to continue?\n(Type "I am sure" to continue.)\n')
        assert answer.lower() == 'i am sure', 'Stopping the import'

        Category.objects.all().delete()
        Post.objects.all().delete()

        for root, dirs, files in os.walk(root_path):
            for f in files:
                if f.endswith('.md'):
                    if options.get("verbose"):
                        print "Importing {}/{}".format(root, f)
                        text = codecs.open(os.path.join(root, f), 'r',
                                          encoding='utf-8').read()
                        html = md.convert(text)
                        import_post(md, text)
