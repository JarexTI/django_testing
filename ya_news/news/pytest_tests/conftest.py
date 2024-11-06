from datetime import datetime, timedelta

import pytest
from pytest_lazyfixture import lazy_fixture
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

NEW_TEXT = 'Новый текст'
TITLE = 'Заголовок'
TEXT_NEWS = 'Текст новости'
TEXT_COMMENT = 'Текст комментария'
NEWS = 'Новость'
TEXT = 'Текст'
PK = 1
ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')

URL = {
    'home': reverse('news:home'),
    'detail': reverse('news:detail', args=(PK,)),
    'edit': reverse('news:edit', args=(PK,)),
    'delete': reverse('news:delete', args=(PK,)),
    'login': reverse('users:login'),
    'logout': reverse('users:logout'),
    'signup': reverse('users:signup'),
}


@pytest.fixture
def new_comment_text():
    return {'text': NEW_TEXT}


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    test_news = News.objects.create(
        title=TITLE,
        text=TEXT_NEWS,
        date=datetime.today(),
    )
    return test_news


@pytest.fixture
def comment(news, author):
    test_comment = Comment.objects.create(
        author=author,
        news=news,
        text=TEXT_COMMENT,
    )
    return test_comment


@pytest.fixture
def list_news():
    today = datetime.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        News.objects.create(
            title=f'{NEWS} {index}',
            text=TEXT_NEWS,
            date=today - timedelta(days=index),
        )


@pytest.fixture
def list_comments(news, author):
    now, comment_list = timezone.now(), []
    for index in range(2):
        test_comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'{TEXT} {index}',
        )
        test_comment.created = now + timedelta(days=index)
        test_comment.save()
        comment_list.append(test_comment)
