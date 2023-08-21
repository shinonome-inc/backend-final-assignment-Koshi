from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.url = reverse("tweets:home")
        Tweet.objects.create(user=self.user, content="testcontent1")
        Tweet.objects.create(user=self.user, content="testcontent2")

    def test_success_get(self):
        response = self.client.get(self.url)
        test_list = response.context["tweet_list"]
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(test_list, Tweet.objects.all(), ordered=False)


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_data = {
            "username": self.user,
            "content": "testcontent",
        }
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Tweet.objects.filter(id=1).exists())
        self.assertEqual(Tweet.objects.get(id=1).content, valid_data["content"])

    def test_failure_post_with_empty_content(self):
        invalid_data = {
            "username": self.user,
            "content": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["content"])
        self.assertFalse(Tweet.objects.filter(id=1).exists())

    def test_failure_post_with_too_long_content(self):
        invalid_data = {
            "username": self.user,
            "content": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("この値は 50 文字以下でなければなりません( 60 文字になっています)。", form.errors["content"])
        self.assertFalse(Tweet.objects.filter(id=1).exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="testcontent")
        self.url = reverse("tweets:detail", kwargs=dict(pk=self.tweet.pk))

    def test_success_get(self):
        response = self.client.get(self.url)
        test = response.context["tweet"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test, self.tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="testcontent")
        self.url = reverse("tweets:delete", kwargs=dict(pk=self.tweet.pk))
        self.client.login(username="tester", password="testpassword")

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Tweet.objects.filter(id=self.tweet.pk).exists())

    def test_failure_post_with_not_exist_tweet(self):
        self.url = reverse("tweets:delete", kwargs=dict(pk=self.tweet.pk + 1))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Tweet.objects.filter(id=self.tweet.pk + 1).exists())

    def test_failure_post_with_incorrect_user(self):
        self.another_user = User.objects.create_user(username="Koshi", password="testpass")
        self.client.login(username="Koshi", password="testpass")
        response = self.client.post(self.url)
        first_count = Tweet.objects.count()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tweet.objects.count(), first_count)


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
