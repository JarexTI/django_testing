#  test_logic.py
from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.fixtures import BaseFixture


class TestLogic(BaseFixture):

    def test_logged_in_user_can_create_note(self):
        Note.objects.all().delete()
        expected_count = Note.objects.count() + 1
        url = self.URL.add
        response = self.user_client.post(url, data=self.data)
        self.assertRedirects(response, self.URL.success)
        self.assertEqual(expected_count, Note.objects.count())

        note = Note.objects.get()
        self.assertEqual(note.slug, self.data['slug'])
        self.assertEqual(note.title, self.data['title'])
        self.assertEqual(note.text, self.data['text'])
        self.assertEqual(note.author, self.user)

    def test_anonymous_user_cant_create_note(self):
        initial_note_count = Note.objects.count()
        url = self.URL.add
        response = self.client.post(url, self.data)
        login_url = self.URL.login
        expected_url = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), initial_note_count)

    def test_not_create_two_note(self):
        expected_count = Note.objects.count()
        url = self.URL.add
        response = self.user_client.post(
            url,
            data={
                'slug': self.note.slug,
                'title': self.NEW_TITLE,
                'text': self.TEST_TEXT,
            },
        )
        self.assertEqual(expected_count, Note.objects.count())
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING)
        )

    def test_slug_auto_filled_by_pytils_if_empty(self):
        Note.objects.all().delete()
        url = self.URL.add
        self.data.pop('slug')
        response = self.user_client.post(url, data=self.data)
        self.assertRedirects(response, self.URL.success)
        note = Note.objects.get()
        expected_slug = slugify(self.data['title'])
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_note(self):
        url = self.NOTE_EDIT_PAGE
        response = self.user_client.post(url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        unchanged_note = Note.objects.get(id=self.another_note.id)
        self.assertEqual(unchanged_note.slug, self.another_note.slug)
        self.assertEqual(unchanged_note.title, self.another_note.title)
        self.assertEqual(unchanged_note.text, self.another_note.text)
        self.assertEqual(unchanged_note.author, self.another_note.author)

    def test_user_can_edit_others_note(self):
        url = self.URL.edit
        response = self.author_user_client.post(url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        unchanged_note = Note.objects.get(id=self.note.id)
        self.assertEqual(unchanged_note.slug, self.note.slug)
        self.assertEqual(unchanged_note.title, self.note.title)
        self.assertEqual(unchanged_note.text, self.note.text)
        self.assertEqual(unchanged_note.author, self.note.author)

    def test_user_can_delete_note(self):
        expected_count = Note.objects.count() - 1
        url = self.URL.delete
        response = self.user_client.post(url)
        self.assertRedirects(response, self.URL.success)
        self.assertEqual(Note.objects.count(), expected_count)

    def test_user_can_delete_others_note(self):
        expected_count = Note.objects.count()
        url = self.URL.delete
        response = self.author_user_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(expected_count, Note.objects.count())
