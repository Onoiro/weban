import pytest
import os
from unittest.mock import patch, MagicMock
import psycopg2
from page_analyzer.app import app


@pytest.fixture
def client():
    """Фикстура для тестирования Flask приложения"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    """Мок для подключения к базе данных"""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = None
    mock_cur.fetchall.return_value = []
    with patch('psycopg2.connect') as mock_connect:
        mock_connect.return_value = mock_conn
        yield {'conn': mock_conn, 'cur': mock_cur}


@pytest.fixture
def sample_url_data():
    """Пример данных URL для тестов"""
    return {
        'id': 1,
        'name': 'https://example.com',
        'created_at': '2023-01-01',
        'last_check': '2023-01-02',
        'status_code': 200
    }


@pytest.fixture
def sample_check_data():
    """Пример данных проверки для тестов"""
    return {
        'id': 1,
        'url_id': 1,
        'status_code': 200,
        'h1': 'Test Header',
        'title': 'Test Title',
        'description': 'Test description',
        'created_at': '2023-01-01'
    }


@pytest.fixture
def mock_requests_response():
    """Мок для ответа requests"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <head>
            <title>Test Title</title>
            <meta name="description" content="Test description">
        </head>
        <body>
            <h1>Test Header</h1>
        </body>
    </html>
    '''
    return mock_response