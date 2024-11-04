from http import HTTPStatus

from django.urls import reverse

from notes.tests.fixtures import URL, ContentFixture


class TestRoutes(ContentFixture):

    def test_anonymous_user_page_access(self):
        urls = (
            URL.get('home', None),
            URL.get('login', None),
            URL.get('logout', None),
            URL.get('signup', None),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_user_page_access(self):
        urls = (
            URL.get('list', None),
            URL.get('success', None),
            URL.get('add', None),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.user_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_access_for_different_user_types(self):
        users_statuses = (
            (self.user_client, HTTPStatus.OK),
            (self.author_user_client, HTTPStatus.NOT_FOUND),
        )
        urls = (
            URL.get('detail', None),
            URL.get('edit', None),
            URL.get('delete', None),
        )
        for user, status in users_statuses:
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_redirects(self):
        login_url = reverse(URL.get('login', None))
        urls = (
            (URL.get('list', None), None),
            (URL.get('success', None), None),
            (URL.get('add', None), None),
            (URL.get('detail', None), (self.note.slug,)),
            (URL.get('edit', None), (self.note.slug,)),
            (URL.get('delete', None), (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
