import pytest
from unittest.mock import patch, MagicMock
import psycopg2
from page_analyzer.db import (
    connect_db, close_db, get_all_urls, get_url_data, 
    get_url_checks, get_url_by_name, add_url, add_url_check
)


class TestDatabaseConnection:
    """Тесты для подключения к базе данных"""

    @patch('psycopg2.connect')
    def test_connect_db_success(self, mock_connect, mock_db_connection):
        """Тест успешного подключения к базе данных"""
        mock_connect.return_value = mock_db_connection['conn']
        
        @connect_db
        def test_func(cur):
            return "success"
        
        result = test_func()
        assert result == "success"
        mock_connect.assert_called_once()

    @patch('psycopg2.connect')
    def test_connect_db_failure(self, mock_connect):
        """Тест обработки ошибки подключения к базе данных"""
        mock_connect.side_effect = psycopg2.OperationalError("Connection failed")
        
        @connect_db
        def test_func(cur):
            return "success"
        
        result = test_func()
        assert result is None

    def test_close_db(self, mock_db_connection):
        """Тест закрытия соединения с базой данных"""
        close_db(mock_db_connection['conn'], mock_db_connection['cur'])
        
        mock_db_connection['conn'].close.assert_called_once()
        mock_db_connection['cur'].close.assert_called_once()


class TestGetAllUrls:
    """Тесты для функции get_all_urls"""

    @patch('psycopg2.connect')
    def test_get_all_urls_success(self, mock_connect, sample_url_data):
        """Тест успешного получения всех URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [sample_url_data]
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_all_urls()
        
        assert len(result) == 1
        assert result[0]['name'] == 'https://example.com'
        mock_cur.execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_all_urls_empty(self, mock_connect):
        """Тест получения пустого списка URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_all_urls()
        
        assert result == []


class TestGetUrlData:
    """Тесты для функции get_url_data"""

    @patch('psycopg2.connect')
    def test_get_url_data_success(self, mock_connect, sample_url_data):
        """Тест успешного получения данных URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = sample_url_data
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_url_data(1)
        
        assert result['id'] == 1
        assert result['name'] == 'https://example.com'
        mock_cur.execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_url_data_not_found(self, mock_connect):
        """Тест получения несуществующего URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_url_data(999)
        
        assert result is None


class TestGetUrlChecks:
    """Тесты для функции get_url_checks"""

    @patch('psycopg2.connect')
    def test_get_url_checks_success(self, mock_connect, sample_check_data):
        """Тест успешного получения проверок URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [sample_check_data]
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_url_checks(1)
        
        assert len(result) == 1
        assert result[0]['url_id'] == 1
        mock_cur.execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_url_checks_empty(self, mock_connect):
        """Тест получения пустого списка проверок"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_url_checks(1)
        
        assert result == []


class TestGetUrlByName:
    """Тесты для функции get_url_by_name"""

    @patch('psycopg2.connect')
    def test_get_url_by_name_success(self, mock_connect, sample_url_data):
        """Тест успешного поиска URL по имени"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = sample_url_data
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_url_by_name('https://example.com')
        
        assert result['name'] == 'https://example.com'
        mock_cur.execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_url_by_name_not_found(self, mock_connect):
        """Тест поиска несуществующего URL по имени"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = get_url_by_name('https://nonexistent.com')
        
        assert result is None


class TestAddUrl:
    """Тесты для функции add_url"""

    @patch('psycopg2.connect')
    def test_add_url_success(self, mock_connect, sample_url_data):
        """Тест успешного добавления URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = sample_url_data
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = add_url('https://example.com', '2023-01-01')
        
        assert result['id'] == 1
        mock_cur.execute.assert_called_once()


class TestAddUrlCheck:
    """Тесты для функции add_url_check"""

    @patch('psycopg2.connect')
    def test_add_url_check_success(self, mock_connect, sample_url_data, sample_check_data):
        """Тест успешного добавления проверки URL"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = sample_url_data
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = add_url_check(1, 200, 'Test Header', 'Test Title', 'Test description', '2023-01-01')
        
        assert result is None
        # Проверяем, что были выполнены три запроса: 
        # 1. get_url_data (внутри add_url_check)
        # 2. INSERT в url_checks
        # 3. UPDATE urls
        assert mock_cur.execute.call_count == 3

    @patch('psycopg2.connect')
    def test_add_url_check_with_special_characters(self, mock_connect, sample_url_data):
        """Тест добавления проверки с специальными символами"""
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchone.return_value = sample_url_data
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        
        result = add_url_check(1, 200, 'Test & Header', 'Test "Title"', 'Test <description>', '2023-01-01')
        
        assert result is None