# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='i18nflatpage',
            name='listed',
            field=models.BooleanField(default=True, help_text=b'Display a link for this page'),
            preserve_default=True,
        ),
    ]
