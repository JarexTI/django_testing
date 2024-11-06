import pytest
from django.conf import settings

from news.forms import CommentForm
from news.pytest_tests.conftest import URL

pytestmark = pytest.mark.django_db


def test_max_10_news_on_homepage(client, list_news):
    url = URL.get('home')
    response = client.get(url)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_sorted_by_freshness(client, list_news):
    url = URL.get('home')
    response = client.get(url)
    news = response.context['object_list']
    sorted_news = sorted(news, key=lambda x: x.date, reverse=True)
    assert list(news) == sorted_news


def test_comments_sorted_chronologically(client, news, list_comments):
    url = URL.get('detail')
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    comments = list(news.comment_set.all())
    sorted_comments = sorted(comments, key=lambda comment: comment.created)
    assert comments == sorted_comments


@pytest.mark.parametrize(
    'parametrized_client, status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True),
    ),
)
def test_comment_form_accessibility(parametrized_client, status, comment):
    url = URL.get('detail')
    response = parametrized_client.get(url)
    form_in_context = 'form' in response.context
    assert form_in_context is status

    if form_in_context:
        assert isinstance(response.context['form'], CommentForm)
