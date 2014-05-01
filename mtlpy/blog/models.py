# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime
from markdown import Markdown

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import (get_language,
                                      ugettext_lazy as _)

from mtlpy.users.models import MtlPyUser
from sorl.thumbnail import ImageField


def i18n_field(name, default=settings.LANGUAGE_CODE[:2], fallback=True):
    # This creates a property on this model, that will basically attempt
    # to access a property called <name>_<get_language()>, else return
    # return <name>_<default>.
    #
    # Sample usage:
    # class User(models.Model):
    #     bio_en = models.TextField(blank=True, null=True)
    #     bio_fr = models.TextField(blank=True, null=True)
    #     bio = i18n_field('bio')
    #
    # user1 = User.objects.get(id=1)
    # print user1.bio
    #
    # 'fallback' parameter will allow the field to return the default
    # language value if the requested language content does not exist.

    @property
    def i18n_field_getter(inst):
        lang = get_language()[:2]
        try:
            res = getattr(inst, '_'.join((name, lang)))
            if not res and fallback:
                res = getattr(inst, '_'.join((name, default)))
        except AttributeError:
            res = getattr(inst, '_'.join((name, default)))

        return res

    return i18n_field_getter


class PublishedManager(models.Manager):
    def published(self):
        return self.get_query_set().filter(
            status__gte=2, publish__lte=datetime.date.today())


class Post(models.Model):
    PUBLISH_CHOICES = ((1, _('Draft')),
                       (2, _('Published')))

    slug = models.SlugField(max_length=256)

    title_en = models.CharField(max_length=1024, blank=True)
    title_fr = models.CharField(max_length=1024, blank=True)
    title = i18n_field('title')

    content_en = models.TextField(blank=True)
    content_fr = models.TextField(blank=True)
    content = i18n_field('content')

    created = models.DateField(auto_now_add=True)
    publish = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=PUBLISH_CHOICES, default=2)
    logo = ImageField(upload_to='post', null=True, blank=True)

    author = models.ForeignKey(MtlPyUser)
    category = models.ForeignKey('Category', related_name='posts')

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        db_table='blog_post'
        ordering = ('-publish', )
        get_latest_by = 'publish'

    def __unicode__(self):
        return u"{0}".format(self.slug)

    def get_absolute_url(self):
        return reverse_lazy('blog_detail', kwargs={
            'year': self.publish.year,
            'month': self.publish.strftime('%m').lower(),
            'slug': self.slug})

    def html_content(self):
        try:
            return self._html_content
        except AttributeError:
            md = Markdown(extensions=['meta'])
            self._html_content = md.convert(self.content)
            return self._html_content

    def striped_content(self):
        return strip_tags(self.html_content())

    def clean(self):
        if self.status == 2 and self.publish is None:
            raise ValidationError(
                _("Need a valid publish date before publishing")
            )


class Category(models.Model):
    slug = models.SlugField(max_length=64)
    title_en = models.CharField(max_length=64)
    title_fr = models.CharField(max_length=64)
    title = i18n_field('title')
    logo = ImageField(upload_to='category', default='category/default.jpg')

    class Meta:
        db_table = 'blog_categories'
        ordering = ('slug', )
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return u"{0}".format(self.slug)

    def get_absolute_url(self):
        return reverse_lazy('blog_category', kwargs={'slug': self.slug})
