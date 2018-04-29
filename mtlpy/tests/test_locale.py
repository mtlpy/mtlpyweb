from django.test import TestCase
from django.utils import translation


class TestLocale(TestCase):

    def test_redirect_default(self):
        # Should redirect to 'en' since it's the default language
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/en/')

    def test_change_locale(self):
        translation.activate('en')

        resp = self.client.get('/en/change_locale/fr/', HTTP_REFERER='http://www.montrealpython.org/en/blog/')

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/fr/blog/')
        self.assertEqual(translation.get_language(), 'fr')

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/fr/')

    def test_change_locale_without_referer(self):
        resp = self.client.get('/en/change_locale/fr/')

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/fr/')

    def test_change_locale_from_root_path(self):
        # Sent by some bots? Like Datanyze
        translation.activate('en')

        resp = self.client.get('/en/change_locale/fr/', HTTP_REFERER='http://www.montrealpython.org')

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/fr/')
