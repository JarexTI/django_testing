#  fixtures.py
from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SLUG = 'note-slug'

URL_NAME = namedtuple(
    'NAME',
    [
        'home',
        'add',
        'list',
        'detail',
        'edit',
        'delete',
        'success',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('notes:home'),
    reverse('notes:add'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
    reverse('notes:success'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


class BaseFixture(TestCase):
    TITLE = 'Заголовок'
    TEXT = 'Текст'
    NEW_TITLE = 'Новый заголовок'
    TEST_TEXT = 'Тестовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Пользователь')
        cls.author_user = User.objects.create(username='Автор пользователь')

        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.author_user_client = Client()
        cls.author_user_client.force_login(cls.author_user)

        cls.note = Note.objects.create(
            author=cls.user,
            title=cls.TITLE,
            text=cls.TEXT,
            slug=SLUG,
        )
        cls.data = {
            'slug': 'slug',
            'title': cls.NEW_TITLE,
            'text': cls.TEST_TEXT,
        }
        cls.another_note = Note.objects.create(
            author=cls.author_user,
            title=cls.TITLE,
            text=cls.TEXT,
            slug='unique-slug'
        )

        cls.NOTE_EDIT_PAGE = reverse(
            'notes:edit', args=(cls.note.slug,)
        )
