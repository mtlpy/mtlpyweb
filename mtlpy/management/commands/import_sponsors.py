import ConfigParser

from django.core.management.base import BaseCommand

from mtlpy.models import Sponsor


class Command(BaseCommand):
    help = 'Import the sponsor ini file'

    def handle(self, *args, **options):
        self.config = ConfigParser.ConfigParser()
        self.config.read('sponsors.ini')
        sections = self.config.sections()
        self._build_sponsors(sections)

    def _build_sponsors(self, ini_titles):
        for sponsor in ini_titles:
            if sponsor.startswith('sponsor-'):
                name = self.config.get(sponsor, 'name')
                url = self.config.get(sponsor, 'url')
                logo = self.config.get(sponsor, 'logo')
                sponsor = Sponsor(name=name, url=url, logo=logo)
                sponsor.save()
