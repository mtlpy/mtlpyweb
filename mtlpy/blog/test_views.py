from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from mtlpy.blog.models import Category, Post


class BlogIntegrationTestCase(TestCase):
    def setUp(self):
        self.now = datetime.now() - timedelta(days=1)

        self.user = User()
        self.user.email = "test@mtlpy.org"
        self.user.save()

        self.category = Category()
        self.category.slug = "category"
        self.category.title_en = "category_title_en"
        self.category.title_fr = "category_title_fr"
        self.category.save()

        self.post = Post()
        self.post.slug = "slug"
        self.post.title_en = "post_title_en"
        self.post.title_fr = "post_title_fr"
        self.post.publish = self.now
        self.post.status = 2
        self.post.author = self.user
        self.post.category = self.category
        self.post.save()

    def test_category(self):
        resp = self.client.get('/en/blog/category/')
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        resp = self.client.get(f"/en/{self.now.year}/{self.now:%m}/slug/")
        self.assertEqual(resp.status_code, 200)

    def test_user_posts(self):
        resp = self.client.get(f"/en/user/{self.user.id}/")
        self.assertEqual(resp.status_code, 200)
