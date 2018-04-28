from django.test import TestCase

from mtlpy import views
from mtlpy.models import Sponsor


class IntegrationTestCase(TestCase):
    def setUp(self):
        self.sponsor = Sponsor.objects.create(
            name='test', slug='test', url='http://testserver.com', logo=None)

    def test_home_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/en/')

    def test_home_page_redirected(self):
        resp = self.client.get('/en/')
        self.assertEqual(resp.status_code, 200)

    def test_styleguide(self):
        resp = self.client.get('/en/styleguide/')
        self.assertEqual(resp.status_code, 200)

    def test_videos(self):
        views.get_all_videos = lambda x: []
        resp = self.client.get('/en/videos/')
        self.assertEqual(resp.status_code, 200)

    def test_sponsor_details(self):
        resp = self.client.get('/en/sponsor/invalid/')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get('/en/sponsor/test/')
        self.assertEqual(resp.status_code, 200)

    def test_sponsorship(self):
        resp = self.client.get('/en/sponsorship/')
        self.assertEqual(resp.status_code, 200)
