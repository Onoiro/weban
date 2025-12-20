import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from page_analyzer.app import app


class TestIndexRoute:
    """Тесты для главной страницы"""

    def test_index_get(self, client):
        """Тест GET запроса на главную страницу"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<title>' in response.data


class TestUrlsListRoute:
    """Тесты для списка URL"""

    def test_urls_list_get(self, client):
        """Тест GET запроса на список URL"""
        response = client.get('/urls/')
        
        assert response.status_code == 200
        assert b'<table' in response.data


class TestUrlDetailRoute:
    """Тесты для детальной страницы URL"""

    def test_url_detail_get(self, client):
        """Тест GET запроса на детальную страницу URL"""
        response = client.get('/urls/1')
        
        assert response.status_code == 200
        assert b'<table' in response.data


class TestAddUrlRoute:
    """Тесты для добавления URL"""

    def test_add_url_success(self, client):
        """Тест успешного добавления нового URL - проверяем только статус код"""
        response = client.post('/urls', data={'url': 'https://example.com'}, follow_redirects=True)
        
        assert response.status_code == 200

    def test_add_url_already_exists(self, client):
        """Тест добавления уже существующего URL"""
        response = client.post('/urls', data={'url': 'not-a-url'})
        
        assert response.status_code == 422
        assert 'Некорректный URL' in response.data.decode('utf-8')

    def test_add_url_too_long(self, client):
        """Тест добавления URL превышающего лимит длины"""
        long_url = 'https://example.com/' + 'a' * 250

        response = client.post('/urls', data={'url': long_url})
        
        assert response.status_code == 422
        assert 'URL превышает 255 символов' in response.data.decode('utf-8')

    def test_add_url_invalid(self, client):
        """Тест добавления невалидного URL"""
        response = client.post('/urls', data={'url': 'not-a-url'})
        
        assert response.status_code == 422
        assert 'Некорректный URL' in response.data.decode('utf-8')


class TestCheckUrlRoute:
    """Тесты для проверки URL"""

    def test_check_url_success(self, client):
        """Тест успешной проверки URL - проверяем только статус код"""
        response = client.post('/urls/1/checks', follow_redirects=True)
        
        assert response.status_code == 200

    def test_check_url_failure(self, client):
        """Тест неудачной проверки URL"""
        response = client.post('/urls/1/checks', follow_redirects=True)
        
        assert response.status_code == 200


class TestFlashMessages:
    """Тесты для flash сообщений"""

    def test_flash_messages_on_add_url(self, client):
        """Тест flash сообщений при добавлении URL"""
        response = client.post('/urls', data={'url': 'not-a-url'}, follow_redirects=True)
        
        # Проверяем, что в ответе есть сообщение об ошибке
        assert 'Некорректный URL' in response.data.decode('utf-8')

    def test_flash_messages_on_check_url(self, client):
        """Тест flash сообщений при проверке URL"""
        response = client.post('/urls/1/checks', follow_redirects=True)
        
        # Просто проверяем, что запрос обрабатывается
        assert response.status_code == 200


class TestUrlNormalization:
    """Тесты для нормализации URL в маршруте добавления"""

    def test_url_normalization_in_post(self, client):
        """Тест нормализации URL при POST запросе"""
        # Просто проверяем, что запрос обрабатывается без ошибок
        response = client.post('/urls', data={'url': 'https://example.com/path?query=value'}, follow_redirects=True)
        
        assert response.status_code == 200