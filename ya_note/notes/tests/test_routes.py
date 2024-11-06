from http import HTTPStatus

from notes.tests.fixture_content import ContentFixture
from notes.tests.fixtures import URL


class TestRoutes(ContentFixture):

    def test_anonymous_user_page_access(self):
        urls = (
            URL.home,
            URL.login,
            URL.logout,
            URL.signup,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_user_page_access(self):
        urls = (
            URL.list,
            URL.success,
            URL.add,
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
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for user, status in users_statuses:
            for url in urls:
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_redirects(self):
        login_url = URL.login
        urls = (
            URL.list,
            URL.success,
            URL.add,
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
