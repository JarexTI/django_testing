from http import HTTPStatus

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import URL
from pytest_django.asserts import assertFormError, assertRedirects

TEXT_COMMENT = 'Текст комментария'

pytestmark = pytest.mark.django_db


def test_no_anon_comment(client, news, new_comment_text):
    expected_count = Comment.objects.count()
    url = URL.get('detail', None)
    client.post(url, data=new_comment_text)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count


def test_author_user_comment(author, author_client, news, new_comment_text):
    Comment.objects.all().delete()
    url = URL.get('detail', None)
    author_client.post(url, data=new_comment_text)
    comment = Comment.objects.get()
    assert Comment.objects.count() == 1
    assert comment.text == new_comment_text['text']
    assert comment.news == news
    assert comment.author == author


def test_comment_with_banned_words_fails(author_client, news):
    expected_count = Comment.objects.count()
    clean_text_data = {
        'text': f'Тестовый текст, {BAD_WORDS[0]}, последующий текст'
    }
    url = URL.get('detail', None)
    response = author_client.post(url, data=clean_text_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert expected_count == comments_count


def test_author_user_edit_comment(author_client, news, comment,
                                  new_comment_text):
    news_url = URL.get('detail', None)
    comment_url = URL.get('edit', None)
    response = author_client.post(comment_url, data=new_comment_text)
    assertRedirects(response, news_url + '#comments')
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == new_comment_text['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_author_user_cannot_edit_comment(admin_client, comment,
                                         new_comment_text):
    comment_url = URL.get('edit', None)
    response = admin_client.post(comment_url, data=new_comment_text)
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == comment.text
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_author_user_delete_comment(author_client, news, comment):
    news_url = URL.get('detail', None)
    comment_url = URL.get('delete', None)
    response = author_client.delete(comment_url)
    assertRedirects(response, news_url + '#comments')
    assert Comment.objects.count() == 0


def test_author_user_cannot_delete_comment(admin_client, comment):
    comment_url = URL.get('delete', None)
    response = admin_client.delete(comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
