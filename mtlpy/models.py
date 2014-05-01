# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

from mtlpy.blog.models import Post


MEDAL_CHOICES = (('GOLD', _('Gold')),
                 ('SILVER', _('Silver')),
                 ('BRONZE', _('Bronze')))


class Sponsor(models.Model):
    name = models.CharField(max_length=32)
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

    def __unicode__(self):
        return self.name


class EventSponsor(models.Model):
    post = models.ForeignKey(Post, null=True, related_name='event_sponsors')
    sponsor = models.ForeignKey(Sponsor)
    medal = models.CharField(max_length=8, choices=MEDAL_CHOICES)
    def __unicode__(self):
        return '%s sponsoring %s' % (
            self.sponsor.name,
            self.post,
            )
