from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.conf import settings

from markdown import Markdown


class I18NFlatPage(FlatPage):

    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE[:2])

    translation = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        help_text='',
    )

    def get_absolute_url(self):
        pattern = '/%(lang)s%(url)s'

        return pattern % {
            'lang': self.language,
            'url': self.url,
        }

    @property
    def html_content(self):
        md = Markdown(extensions=['meta'])
        return md.convert(self.content)
