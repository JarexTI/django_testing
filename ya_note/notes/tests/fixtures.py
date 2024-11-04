#  fixtures.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()

URL = {
    'home': 'notes:home',
    'add': 'notes:add',
    'list': 'notes:list',
    'detail': 'notes:detail',
    'edit': 'notes:edit',
    'delete': 'notes:delete',
    'success': 'notes:success',
    'login': 'users:login',
    'logout': 'users:logout',
    'signup': 'users:signup',
}


class BaseFixture(TestCase):
    TITLE = 'Заголовок'
    TEXT = 'Текст'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Пользователь')
        cls.author_user = User.objects.create(username='Автор пользователь')

        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.author_user_client = Client()
        cls.author_user_client.force_login(cls.author_user)


class ContentFixture(BaseFixture):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note = Note.objects.create(
            author=cls.user,
            title=cls.TITLE,
            text=cls.TEXT,
        )
