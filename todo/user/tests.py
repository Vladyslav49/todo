from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestUser(TestCase):
    def test_render_register(self) -> None:
        register_url = reverse("register")

        response = self.client.get(register_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "user/register.html")

    def test_register(self) -> None:
        register_url = reverse("register")
        username = "username"
        password = "Password1@"

        response = self.client.post(
            register_url,
            data={
                "username": username,
                "password1": password,
                "password2": password,
            },
        )

        login_url = reverse("login")

        self.assertRedirects(response, expected_url=login_url)
