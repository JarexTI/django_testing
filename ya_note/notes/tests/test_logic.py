#  test_logic.py
from http import HTTPStatus

from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.fixtures import URL, BaseFixture


class TestLogic(BaseFixture):
    NEW_TITLE = 'Новый заголовок'
    TEST_TEXT = 'Тестовый текст'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.data = {
            'slug': 'slug',
            'title': cls.NEW_TITLE,
            'text': cls.TEST_TEXT,
        }

    def setUp(self):
        Note.objects.all().delete()
        self.note = Note.objects.create(
            author=self.user,
            title=self.TITLE,
            text=self.TEXT,
        )

    def test_logged_in_user_can_create_note(self):
        url = reverse(URL.get('add', None))
        response = self.user_client.post(url, data=self.data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 2)
        note = Note.objects.exclude(id=self.note.id).first()
        self.assertEqual(note.slug, self.data['slug'])
        self.assertEqual(note.title, self.data['title'])
        self.assertEqual(note.text, self.data['text'])
        self.assertEqual(note.author, self.user)

    def test_anonymous_user_cant_create_note(self):
        initial_note_count = Note.objects.count()
        url = reverse(URL.get('add', None))
        response = self.client.post(url, self.data)
        login_url = reverse(URL.get('login', None))
        expected_url = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), initial_note_count)

    def test_not_create_two_note(self):
        url = reverse(URL.get('add', None))
        response = self.user_client.post(
            url,
            data={
                'slug': self.note.slug,
                'title': self.NEW_TITLE,
                'text': self.TEST_TEXT,
            },
        )
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_auto_filled_by_pytils_if_empty(self):
        url = reverse(URL.get('add', None))
        self.data.pop('slug')
        response = self.user_client.post(url, data=self.data)
        self.assertRedirects(response, reverse(URL.get('success', None)))
        note = Note.objects.get(title=self.NEW_TITLE)
        expected_slug = slugify(self.data['title'])
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_note(self):
        another_note = Note.objects.create(
            author=self.author_user,
            title=self.TITLE,
            text=self.TEXT,
            slug='unique-slug'
        )
        url = reverse(URL.get('edit', None), args=(another_note.slug,))
        response = self.user_client.post(url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        unchanged_note = Note.objects.get(id=another_note.id)
        self.assertEqual(unchanged_note.slug, another_note.slug)
        self.assertEqual(unchanged_note.title, another_note.title)
        self.assertEqual(unchanged_note.text, another_note.text)

    def test_user_can_edit_others_note(self):
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author_user_client.post(url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        unchanged_note = Note.objects.get(id=self.note.id)
        self.assertEqual(unchanged_note.slug, self.note.slug)
        self.assertEqual(unchanged_note.title, self.note.title)
        self.assertEqual(unchanged_note.text, self.note.text)

    def test_user_can_delete_note(self):
        url = reverse(URL.get('delete', None), args=(self.note.slug,))
        response = self.user_client.post(url)
        self.assertRedirects(response, reverse(URL.get('success', None)))
        self.assertEqual(Note.objects.count(), 0)

    def test_user_can_delete_others_note(self):
        url = reverse(URL.get('delete', None), args=(self.note.slug,))
        response = self.author_user_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
