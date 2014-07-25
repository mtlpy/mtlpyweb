# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime
from markdown import Markdown

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from mtlpy.lib.models import i18n_field
from mtlpy.users.models import MtlPyUser

from sorl.thumbnail import ImageField


class PublishedManager(models.Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(
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


class Video(models.Model):
    slug = models.SlugField(max_length=256)

    code = models.CharField(max_length=15)

    post = models.ForeignKey(Post, related_name="videos")

    title_en = models.CharField(max_length=64)
    title_fr = models.CharField(max_length=64)
    title = i18n_field('title')

    class Meta:
        db_table = 'blog_video'
        ordering = ('post', )
        verbose_name_plural = _('Videos')

    def __unicode__(self):
        return u"{0}".format(self.title)

    def get_absolute_url(self):
        return reverse_lazy('video', kwargs={"slug": self.slug})
