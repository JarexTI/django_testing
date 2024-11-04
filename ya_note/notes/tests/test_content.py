#  test_content.py
from django.urls import reverse

from notes.tests.fixtures import URL, ContentFixture


class TestContent(ContentFixture):

    def test_note_passed_to_page_in_object_list(self):
        users_statuses = (
            (self.user_client, True),
            (self.author_user_client, False),
        )
        for user, note_list in users_statuses:
            with self.subTest(user=user):
                url = reverse(URL.get('list', None))
                response = user.get(url)
                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), note_list)

    def test_forms_passed_to_create_and_edit_pages(self):
        urls = (
            (URL.get('add', None), None),
            (URL.get('edit', None), (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.user_client.get(url)
                self.assertIn('form', response.context)
