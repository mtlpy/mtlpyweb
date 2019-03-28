from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from mtlpy.blog.models import Category, Post


class PostListViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.now = datetime.now() - timedelta(days=1)
        self.user = User.objects.create(email='test@mtlpy.org')

        self.category_1 = Category.objects.create(slug='category-1', title_en='Example category 1')
        self.category_2 = Category.objects.create(slug='category-2', title_en='Example category 2')

        self.unpublished_post = Post.objects.create(
            author=self.user,
            category=self.category_1,
            publish=self.now,
            status=1,
            slug='unpublished-post',
            title_en='Unpublished post',
        )

        self.post_1 = Post.objects.create(
            author=self.user,
            category=self.category_1,
            publish=self.now,
            status=2,
            slug='post-1',
            title_en='Example post 1',
        )
        self.post_2 = Post.objects.create(
            author=self.user,
            category=self.category_2,
            publish=self.now - timedelta(days=1),
            status=2,
            slug='post-2',
            title_en='Example post 2',
        )

    def test_lists_all_published_posts_by_default(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['posts']), [self.post_1, self.post_2])

    def test_can_list_published_posts_of_a_specific_category(self):
        response = self.client.get(reverse('blog_category', args=['category-1']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['posts']), [self.post_1])

    def test_includes_the_requested_category_in_the_context(self):
        response = self.client.get(reverse('blog_category', args=['category-1']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'], self.category_1)


class UserPostListViewTestView(TestCase):
    def setUp(self):
        super().setUp()
        self.now = datetime.now() - timedelta(days=1)
        self.user_1 = User.objects.create(username='test-1', email='test1@mtlpy.org')
        self.user_2 = User.objects.create(username='test-2', email='test2@mtlpy.org')

        self.category = Category.objects.create(slug='category-1', title_en='Example category 1')

        self.post_1 = Post.objects.create(
            author=self.user_1,
            category=self.category,
            publish=self.now,
            status=2,
            slug='post-1',
            title_en='Example post 1',
        )
        self.post_2 = Post.objects.create(
            author=self.user_2,
            category=self.category,
            publish=self.now - timedelta(days=1),
            status=2,
            slug='post-2',
            title_en='Example post 2',
        )

    def test_lists_all_published_posts_of_a_specific_user(self):
        response = self.client.get(reverse('user_posts', args=[self.user_1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['posts']), [self.post_1])


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
