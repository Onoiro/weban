Add comprehensive test suite for Weban project

This commit adds a complete testing infrastructure to the Weban project to ensure code quality and prevent bugs.

## What was added:

### Test files:
- tests/conftest.py - Common test setup and helper functions
- tests/test_app.py - Tests for web application routes and forms
- tests/test_db.py - Tests for database functions and operations  
- tests/test_parser.py - Tests for HTML parsing and SEO data extraction
- tests/test_urls.py - Tests for URL validation and normalization

### Configuration files:
- pytest.ini - Test runner configuration
- Makefile - Added test commands (make test, make test-coverage, etc.)
- Updated pyproject.toml - Added testing dependencies
- Updated .gitignore - Ignore test coverage reports

### Documentation:
- tests/README.md - Complete guide on how to run and understand tests

## Testing dependencies added:
- pytest - Main testing framework
- pytest-flask - Testing Flask applications
- pytest-mock - Creating test doubles for external services
- responses - Mocking HTTP requests
- pytest-cov - Measuring code coverage

## Test results:
- 50 tests total, all passing ✅
- 94% code coverage
- All tests run in ~4 seconds
- HTML coverage report generated

## How to run tests:

```bash
# Run all tests
make test

# Run tests with coverage report
make test-coverage

# Run specific test file
poetry run pytest tests/test_urls.py

# Run with verbose output
make test-verbose
```

## What these tests cover:

### Web application tests (test_app.py):
- Homepage loading
- URL listing page
- URL detail pages  
- Form validation (checking URL length, format)
- Error handling (404 pages)

### Database tests (test_db.py):
- Database connection handling
- Adding new URLs to database
- Retrieving URL data
- Adding URL check results
- Error handling for database failures

### HTML parser tests (test_parser.py):
- Extracting page titles
- Extracting H1 headers  
- Extracting meta descriptions
- Handling missing or empty content
- Processing different HTML formats

### URL validation tests (test_urls.py):
- Checking valid URL formats
- Checking invalid URL formats
- URL length limits (255 characters)
- URL normalization (removing extra paths/parameters)

## Benefits:

1. **Bug Prevention**: Tests catch errors before they reach users
2. **Code Quality**: High coverage (94%) means most code paths are tested
3. **Confidence**: Developers can make changes knowing tests will catch problems
4. **Documentation**: Tests serve as examples of how code should work
5. **Automation**: Tests can run automatically in CI/CD pipelines

The test suite ensures the Weban application works correctly and helps maintain high code quality as the project grows.