from http import HTTPStatus

from notes.tests.fixtures import BaseFixture


class TestRoutes(BaseFixture):

    def test_anonymous_user_page_access(self):
        urls = (
            self.URL.home,
            self.URL.login,
            self.URL.logout,
            self.URL.signup,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_user_page_access(self):
        urls = (
            self.URL.list,
            self.URL.success,
            self.URL.add,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_access_for_different_user_types(self):
        users_statuses = (
            (self.user_client, HTTPStatus.OK),
            (self.author_user_client, HTTPStatus.NOT_FOUND),
        )
        urls = (
            self.URL.detail,
            self.URL.edit,
            self.URL.delete,
        )
        for user, status in users_statuses:
            for url in urls:
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_redirects(self):
        login_url = self.URL.login
        urls = (
            self.URL.list,
            self.URL.success,
            self.URL.add,
            self.URL.detail,
            self.URL.edit,
            self.URL.delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
