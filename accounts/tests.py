from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

from .models import FriendShip

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, valid_data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(username="testuser")
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "ghdag",
            "password2": "ghdag",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "testuser1",
            "password2": "testuser1",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "149596396",
            "password2": "149596396",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test.com",
            "password1": "testuser",
            "password2": "testuser1",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())


class TestLoginView(TestCase):
    def setUp(self):
        self.login_url = reverse("accounts:login")
        User.objects.create_user(username="testuser", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        invalid_data = {
            "username": "Koshi",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。", form.errors["__all__"])
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(self.login_url, invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password"])
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.logout_url = reverse("accounts:logout")

    def test_success_post(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="testpassword1")
        self.user2 = User.objects.create_user(username="tester2", password="testpassword2")
        self.user3 = User.objects.create_user(username="tester3", password="testpassword3")
        self.client.force_login(self.user2)
        Tweet.objects.create(user=self.user2, content="testcontent1")
        Tweet.objects.create(user=self.user2, content="testpassword2")
        FriendShip.objects.create(followee=self.user1, follower=self.user2)
        FriendShip.objects.create(followee=self.user3, follower=self.user2)
        FriendShip.objects.create(followee=self.user2, follower=self.user1)
        self.url = reverse("accounts:user_profile", kwargs=dict(username=self.user2))

    def test_success_get(self):
        response = self.client.get(self.url)
        test_list = response.context["tweet_list"]
        follow_number = response.context["follow_number"]
        follower_number = response.context["follower_number"]
        self.assertEqual(follow_number, FriendShip.objects.filter(follower=self.user2).count())
        self.assertEqual(follower_number, FriendShip.objects.filter(followee=self.user2).count())
        self.assertQuerysetEqual(test_list, Tweet.objects.all(), ordered=False)


# class TestUserProfileEditView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


class TestFollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="testpassword1")
        self.user2 = User.objects.create_user(username="tester2", password="testpassword2")
        self.client.force_login(self.user1)
        self.url = reverse("accounts:follow", kwargs=dict(username=self.user2))

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertTrue(FriendShip.objects.filter(followee=self.user2, follower=self.user1).exists())

    def test_failure_post_with_not_exist_user(self):
        self.url = reverse("accounts:follow", kwargs={"username": "tester3"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FriendShip.objects.filter(follower=self.user1).count(), 0)

    def test_failure_post_with_self(self):
        self.url = reverse("accounts:follow", kwargs=dict(username=self.user1))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(FriendShip.objects.filter(follower=self.user1).count(), 0)


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="testpassword1")
        self.user2 = User.objects.create_user(username="tester2", password="testpassword2")
        self.user3 = User.objects.create_user(username="tester3", password="testpassword3")
        self.client.force_login(self.user1)
        FriendShip.objects.create(followee=self.user2, follower=self.user1)
        FriendShip.objects.create(followee=self.user1, follower=self.user3)
        self.url = reverse("accounts:unfollow", kwargs=dict(username=self.user2))

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertEqual(FriendShip.objects.filter(follower=self.user1).count(), 0)

    def test_failure_post_with_not_exist_tweet(self):
        self.url = reverse("accounts:unfollow", kwargs={"username": "tester4"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FriendShip.objects.filter(follower=self.user1).count(), 1)

    def test_failure_post_with_incorrect_user(self):
        self.url = reverse("accounts:unfollow", kwargs=dict(username=self.user1))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(FriendShip.objects.filter(follower=self.user1).count(), 1)


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="testpassword1")
        self.user2 = User.objects.create_user(username="tester2", password="testpassword2")
        self.client.force_login(self.user1)
        FriendShip.objects.create(followee=self.user2, follower=self.user1)
        self.url = reverse("accounts:following_list", kwargs=dict(username=self.user1))

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="tester1", password="testpassword1")
        self.user2 = User.objects.create_user(username="tester2", password="testpassword2")
        self.client.force_login(self.user2)
        FriendShip.objects.create(followee=self.user2, follower=self.user1)
        self.url = reverse("accounts:follower_list", kwargs=dict(username=self.user2))

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
