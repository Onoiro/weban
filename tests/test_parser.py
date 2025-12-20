import pytest
from unittest.mock import patch, MagicMock
import requests
from page_analyzer.parser import try_get_url, get_status_code, get_url_seo_data


class TestParser:
    """Тесты для парсера HTML и получения SEO данных"""

    @patch('page_analyzer.parser.requests.get')
    def test_try_get_url_success(self, mock_get, mock_requests_response):
        """Тест успешного получения URL"""
        mock_get.return_value = mock_requests_response
        
        result = try_get_url("https://example.com")
        
        assert result is not None
        assert result.status_code == 200
        mock_get.assert_called_once_with("https://example.com")

    @patch('page_analyzer.parser.requests.get')
    def test_try_get_url_http_error(self, mock_get):
        """Тест обработки HTTP ошибок"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        result = try_get_url("https://example.com")
        
        assert result is None

    @patch('page_analyzer.parser.requests.get')
    def test_try_get_url_connection_error(self, mock_get):
        """Тест обработки ошибок соединения"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = try_get_url("https://example.com")
        
        assert result is None

    @patch('page_analyzer.parser.requests.get')
    def test_try_get_url_timeout(self, mock_get):
        """Тест обработки таймаута"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        result = try_get_url("https://example.com")
        
        assert result is None

    def test_get_status_code_success(self, mock_requests_response):
        """Тест получения статус кода"""
        status_code = get_status_code(mock_requests_response)
        assert status_code == 200

    def test_get_status_code_404(self):
        """Тест получения статус кода 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        status_code = get_status_code(mock_response)
        assert status_code == 404

    def test_get_url_seo_data_with_full_html(self, mock_requests_response):
        """Тест извлечения SEO данных из полного HTML"""
        h1, title, description = get_url_seo_data(mock_requests_response)
        
        assert h1 == "Test Header"
        assert title == "Test Title"
        assert description == "Test description"

    def test_get_url_seo_data_empty_h1(self):
        """Тест извлечения SEO данных без h1"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <head>
                <title>Test Title</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <!-- no h1 tag -->
            </body>
        </html>
        '''
        
        h1, title, description = get_url_seo_data(mock_response)
        
        assert h1 == ""
        assert title == "Test Title"
        assert description == "Test description"

    def test_get_url_seo_data_empty_title(self):
        """Тест извлечения SEO данных без title"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <head>
                <meta name="description" content="Test description">
            </head>
            <body>
                <h1>Test Header</h1>
            </body>
        </html>
        '''
        
        h1, title, description = get_url_seo_data(mock_response)
        
        assert h1 == "Test Header"
        assert title == ""
        assert description == "Test description"

    def test_get_url_seo_data_empty_description(self):
        """Тест извлечения SEO данных без description"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <head>
                <title>Test Title</title>
                <!-- no description meta tag -->
            </head>
            <body>
                <h1>Test Header</h1>
            </body>
        </html>
        '''
        
        h1, title, description = get_url_seo_data(mock_response)
        
        assert h1 == "Test Header"
        assert title == "Test Title"
        assert description == ""

    def test_get_url_seo_data_no_meta_description_tag(self):
        """Тест извлечения SEO данных без meta description тега"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <head>
                <title>Test Title</title>
                <!-- no description meta tag at all -->
            </head>
            <body>
                <h1>Test Header</h1>
            </body>
        </html>
        '''
        
        h1, title, description = get_url_seo_data(mock_response)
        
        assert h1 == "Test Header"
        assert title == "Test Title"
        assert description == ""

    def test_get_url_seo_data_malformed_html(self):
        """Тест обработки некорректного HTML"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <head>
                <title>Test Title</title>
                <meta name="description" content="Test description">
            <body>
                <h1>Test Header</h1>
        </html>
        '''
        
        # Тест не должен падать с исключением
        h1, title, description = get_url_seo_data(mock_response)
        
        assert h1 == "Test Header"
        assert title == "Test Title"
        assert description == "Test description"

    def test_get_url_seo_data_special_characters_in_description(self):
        """Тест обработки специальных символов в description"""
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <head>
                <title>Test & Title</title>
                <meta name="description" content="Test description with special chars">
            </head>
            <body>
                <h1>Test Header</h1>
            </body>
        </html>
        '''
        
        h1, title, description = get_url_seo_data(mock_response)
        
        # BeautifulSoup декодирует HTML entities
        assert h1 == "Test Header"
        assert title == "Test & Title"
        assert description == "Test description with special chars"