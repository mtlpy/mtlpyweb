# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='I18NFlatPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('language', models.CharField(default=b'en', max_length=2, choices=[(b'fr', b'Fran\xc3\xa7ais'), (b'en', b'English')])),
                ('translation', models.OneToOneField(null=True, blank=True, to='pages.I18NFlatPage', help_text=b'')),
            ],
            options={
            },
            bases=('flatpages.flatpage',),
        ),
    ]
