from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

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
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "test",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=invalid_data["email"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "test",
            "email": "test@test.com",
            "password1": "",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(password=invalid_data["password1"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(username="test", email="test@test.com", password="testpassword")

        duplicated_user = {
            "username": "test",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, duplicated_user)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

        self.assertEqual(User.objects.all().count(), 1)

    def test_failure_post_with_invalid_email(self):
        invalid_email = {
            "username": "test",
            "email": "test123",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_email)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_too_short_password(self):
        too_short_password = {
            "username": "test",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
        }
        response = self.client.post(self.url, too_short_password)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        similar_to_username = {
            "username": "testpass",
            "email": "test@test.com",
            "password1": "testpassn",
            "password2": "testpassn",
        }
        response = self.client.post(self.url, similar_to_username)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])

        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        only_numbers_password = {
            "username": "test",
            "email": "test@test.com",
            "password1": "77777777",
            "password2": "77777777",
        }
        response = self.client.post(self.url, only_numbers_password)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.errors["password2"], ["このパスワードは一般的すぎます。", "このパスワードは数字しか使われていません。"])

        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_mismatch_password(self):
        mismatch_password = {
            "username": "test",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassward",
        }
        response = self.client.post(self.url, mismatch_password)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])

        self.assertEqual(User.objects.all().count(), 0)


# class Homeview(TestCase):
# def test_success_get(self):
# self.url = reverse("tweets:home")
# response = self.client.get(self.url)
# self.assertEqual(response.status_code, 200)
# self.assertTemplateUsed(response, "home.html")


#  class TestLoginView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_empty_password(self):


# class TestLogoutView(TestCase):
#     def test_success_post(self):


# class TestUserProfileView(TestCase):
#     def test_success_get(self):


# class TestUserProfileEditView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_user(self):

#     def test_failure_post_with_self(self):


# class TestUnfollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowingListView(TestCase):
#     def test_success_get(self):


# class TestFollowerListView(TestCase):
#     def test_success_get(self):
