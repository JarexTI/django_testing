from notes.forms import NoteForm
from notes.tests.fixtures import BaseFixture


class TestContent(BaseFixture):

    def test_note_passed_to_page_in_object_list(self):
        users_statuses = (
            (self.user_client, True),
            (self.author_user_client, False),
        )
        for user, note_list in users_statuses:
            with self.subTest(user=user):
                url = self.URL.list
                response = user.get(url)
                response_context = response.context['object_list']
                self.assertIs((self.note in response_context), note_list)

    def test_forms_passed_to_create_and_edit_pages(self):
        urls = (
            self.URL.add,
            self.URL.edit,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(url)
                self.assertIn('form', response.context)
                form = response.context['form']
                self.assertIsInstance(form, NoteForm)
