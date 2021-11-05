"""Tests for views are at this file."""
from unittest.mock import patch
from unittest.mock import Mock
from datetime import datetime
from http.client import OK as HTTP_OK

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


from blog.models import Post


class ViewsTest(TestCase):
    """Testing class for views."""

    def setUp(self):
        """Prepare data for testing."""
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            password='123456',
            is_superuser=True, is_staff=True,
            email='testuser@gmail.com',
            is_active=True,
        )

    def test_index_view_rendering(self):
        """Testing main page for render needed posts."""
        time_zone = timezone.get_current_timezone()
        post = Post.objects.create(
            author=self.user,
            title='test_post',
            text='superText',
            created_date=datetime(
                day=1, month=10,
                year=2021,
                tz=time_zone,
            ),
            published_date=datetime(
                day=1,
                month=10,
                year=2021,
                tz=time_zone,
            ),
        )

        future_post = Post.objects.create(
            author=self.user, title='FuturePost',
            text='superText',
            created_date=datetime(
                day=1, month=5,
                year=2035,
                tz=time_zone,
            ),
            published_date=datetime(
                day=1, month=5,
                year=2035,
                tz=time_zone,
            ),
        )

        past_post = Post.objects.create(
            author=self.user, title='past_post',
            text='superText',
            created_date=datetime(
                day=1, month=8,
                year=2010,
                tz=time_zone,
            ),
            published_date=datetime(
                day=1, month=8,
                year=2010,
                tz=time_zone,
            ),
        )

        post_list_url = reverse('post_list')
        posts_at_date = {
            # long time ago
            datetime(day=1, month=1, year=1990, tz=time_zone): [],
            # after the first post
            datetime(day=1, month=1, year=2022, tz=time_zone): [past_post],
            # after the two posts
            datetime(
                day=1, month=12, year=2021,
                tz=time_zone,
            ): [post, past_post],
            # far in the future, after all three posts
            datetime(
                day=1, month=4, year=2100,
                tz=time_zone,
            ): [future_post, post, past_post],
        }
        for current_date, expected_posts in posts_at_date.items():
            with self.subTest(msg=f'posts published as of {current_date!s}'):
                # pretend that right now it's `current_date`
                with patch(
                        'django.utils.timezone.now',
                        Mock(return_value=current_date),
                ):
                    response = self.client.get(post_list_url)
                self.assertListEqual(
                    list(response.context['posts']),
                    expected_posts,
                )
                self.assertEqual(HTTP_OK, response.status_code)
                self.assertTemplateUsed(response, 'blog/post_list.html')

    def tearDown(self):
        """Clean data after each test."""
        del self.client
        del self.user
