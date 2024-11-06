# test_routes.py
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.pytest_tests.conftest import ADMIN, AUTHOR, CLIENT, URL

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (URL.get('home'), CLIENT, HTTPStatus.OK),
        (URL.get('detail'), CLIENT, HTTPStatus.OK),
        (URL.get('login'), CLIENT, HTTPStatus.OK),
        (URL.get('logout'), CLIENT, HTTPStatus.OK),
        (URL.get('signup'), CLIENT, HTTPStatus.OK),
        (URL.get('edit'), AUTHOR, HTTPStatus.OK),
        (URL.get('delete'), AUTHOR, HTTPStatus.OK),
        (URL.get('edit'), ADMIN, HTTPStatus.NOT_FOUND),
        (URL.get('delete'), ADMIN, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability_for_anonymous_user(
    reverse_url, parametrized_client, status, comment
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'reverse_url',
    (URL.get('edit'), URL.get('delete')),
)
def test_redirect_for_anonymous_client(client,
                                       reverse_url,
                                       comment):
    """Проверка редиректа для анонимного пользователя."""
    expected_url = f'{URL.get("login")}?next={reverse_url}'
    response = client.get(reverse_url)
    assertRedirects(response, expected_url)
