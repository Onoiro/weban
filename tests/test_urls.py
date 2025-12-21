import pytest
from page_analyzer.urls import check_url_len, validate_url, normalize_url


class TestUrlValidation:
    """Тесты для валидации и нормализации URL"""

    def test_check_url_len_with_short_url(self):
        """Тест проверки длины URL с коротким URL"""
        short_url = "https://example.com"
        assert not check_url_len(short_url)

    def test_check_url_len_with_long_url(self):
        """Тест проверки длины URL с длинным URL"""
        long_url = "https://example.com/" + "a" * 250
        assert check_url_len(long_url)

    def test_check_url_len_with_exact_limit(self):
        """Тест проверки длины URL с URL точно 255 символов"""
        # 20 символов для "https://example.com/" + 235 символов для "a" = 255 всего
        url_255 = "https://example.com/" + "a" * 235
        assert len(url_255) == 255
        assert not check_url_len(url_255)

        # URL на 1 символ больше должен превышать лимит
        url_256 = "https://example.com/" + "a" * 236
        assert len(url_256) == 256
        assert check_url_len(url_256)

    def test_check_url_len_with_empty_string(self):
        """Тест проверки длины URL с пустой строкой"""
        assert not check_url_len("")

    def test_validate_url_with_valid_url(self):
        """Тест валидации корректного URL"""
        valid_urls = [
            "https://example.com",
            "http://example.com", # NOSONAR - test data for check valid url
            "https://www.example.com/path?query=value",
            "http://subdomain.example.org" # NOSONAR - test data for check valid url
        ]
        for url in valid_urls:
            assert not validate_url(url), f"URL {url} должен быть валидным"

    def test_validate_url_with_invalid_url(self):
        """Тест валидации некорректного URL"""
        invalid_urls = [
            "not-a-url",
            "",
            "just_text",
            "http://", # NOSONAR - test data for check valid url
            "https://",
            "example.com"
        ]
        for url in invalid_urls:
            assert validate_url(url), f"URL {url} должен быть невалидным"

    def test_normalize_url_with_https(self):
        """Тест нормализации URL с HTTPS"""
        url = "https://example.com/path?query=value"
        expected = "https://example.com"
        assert normalize_url(url) == expected

    def test_normalize_url_with_http(self):
        """Тест нормализации URL с HTTP"""
        url = "http://example.com/path?query=value" # NOSONAR - test data
        expected = "http://example.com" # NOSONAR - test data
        assert normalize_url(url) == expected

    def test_normalize_url_with_www(self):
        """Тест нормализации URL с www"""
        url = "https://www.example.com/path"
        expected = "https://www.example.com"
        assert normalize_url(url) == expected

    def test_normalize_url_without_path(self):
        """Тест нормализации URL без пути"""
        url = "https://example.com"
        expected = "https://example.com"
        assert normalize_url(url) == expected

    def test_normalize_url_with_port(self):
        """Тест нормализации URL с портом"""
        url = "https://example.com:8080/path"
        expected = "https://example.com:8080"
        assert normalize_url(url) == expected