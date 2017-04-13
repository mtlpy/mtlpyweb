# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import gettext_lazy as _
from markdown import Markdown

from mtlpy.lib.models import i18n_field
from mtlpy.blog.models import Post


MEDAL_CHOICES = (('GOLD', _('Gold')),
                 ('SILVER', _('Silver')),
                 ('BRONZE', _('Bronze')))


class Sponsor(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=256)
    url = models.URLField(
        blank=True,
        null=True,
        )
    logo = models.ImageField(upload_to='sponsors')
    ordering = models.IntegerField(default=0)
    frontpage = models.BooleanField(
        default=False,
        help_text='Display on frontpage',
    )
    partner = models.BooleanField(
        default=False,
        help_text='Display as a partner',
    )

    description_en = models.TextField(blank=True)
    description_fr = models.TextField(blank=True)
    description = i18n_field('description')

    @property
    def description_html(self):
        md = Markdown(extensions=['meta'])
        return md.convert(self.description)

    def __unicode__(self):
        return self.name

    @property
    def has_description(self):
        return self.description_en and self.description_fr


class EventSponsor(models.Model):
    post = models.ForeignKey(Post, null=True, related_name='event_sponsors')
    sponsor = models.ForeignKey(Sponsor)
    medal = models.CharField(max_length=8, choices=MEDAL_CHOICES)
    def __unicode__(self):
        return '%s sponsoring %s' % (
            self.sponsor.name,
            self.post,
            )
