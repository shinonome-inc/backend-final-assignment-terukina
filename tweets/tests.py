from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class Homeview(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="testpassword")

    def test_success_get(self):
        login_success = self.client.login(username="test", password="testpassword")
        self.assertTrue(login_success)

        url = reverse("tweets:home")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")


# class TestTweetCreateView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_empty_content(self):

#     def test_failure_post_with_too_long_content(self):


# class TestTweetDetailView(TestCase):
#     def test_success_get(self):


# class TestTweetDeleteView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
