# Testing Guide for Grievance Module API

This document explains how to run unit tests for the Grievance Module FastAPI backend.

## Overview

The test suite covers:
- ✅ Root endpoint verification
- ✅ Creating grievances (anonymous and with complainant info)
- ✅ Creating grievances with household registration
- ✅ Retrieving individual grievances
- ✅ Updating grievance status and metadata
- ✅ Batch updates
- ✅ Exporting recent grievances
- ✅ Generating PDF receipts
- ✅ Error handling (404s, validation errors, etc.)

## Test Setup

### Structure
```
backend/
├── app/                    # Application code
├── tests/                  # Test files
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and configuration
│   ├── test_main.py       # Root endpoint tests
│   └── test_grievances.py # Grievance API tests
├── Dockerfile             # Production Docker image
├── Dockerfile.test        # Test Docker image
├── pytest.ini             # Pytest configuration
└── requirements.txt       # Dependencies (includes pytest, httpx)
```

### Test Dependencies
- `pytest==8.3.2` - Testing framework
- `httpx==0.27.0` - HTTP client for API testing
- `pytest-cov==5.0.0` - Code coverage reports

## Running Tests

### Option 1: Using Docker (Recommended)

Since Python is not installed on your local machine, tests run in a Docker container:

```powershell
# Build the test image
docker build -f backend/Dockerfile.test -t grievance-api-test backend/

# Run all tests
docker run --rm grievance-api-test
```

**One-liner:**
```powershell
docker build -f backend/Dockerfile.test -t grievance-api-test backend/ ; docker run --rm grievance-api-test
```

### Option 2: Using PowerShell Script

A PowerShell script is provided for convenience (requires execution policy changes):

```powershell
.\run_tests.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Option 3: With Python (if installed locally)

If you have Python installed:

```powershell
cd backend
pip install -r requirements.txt
pytest
```

## Test Configuration

### In-Memory Database
Tests use SQLite in-memory database instead of PostgreSQL:
- Faster test execution
- No external dependencies
- Clean state for each test
- Automatic setup and teardown

### Test Fixtures (`conftest.py`)
- `test_db`: Provides a fresh database session for each test
- `client`: TestClient with dependency overrides for isolated testing

## Test Coverage

### Current Test Suite (14 tests)

#### Main API Tests (`test_main.py`)
- ✅ `test_read_root` - Verifies root endpoint returns correct response

#### Grievance API Tests (`test_grievances.py`)
1. ✅ `test_create_grievance_anonymous` - Anonymous grievance creation
2. ✅ `test_create_grievance_with_complainant` - With full complainant info
3. ✅ `test_create_grievance_with_household` - With household registration
4. ✅ `test_create_grievance_with_attachments` - Basic attachment handling
5. ✅ `test_create_grievance_details_too_long` - Validation (10k char limit)
6. ✅ `test_get_grievance` - Retrieve by ID
7. ✅ `test_get_grievance_not_found` - 404 handling
8. ✅ `test_update_grievance_status` - Status updates
9. ✅ `test_update_grievance_with_hh_id` - Household ID updates with Odoo lookup
10. ✅ `test_update_grievance_invalid_id_format` - ID format validation
11. ✅ `test_update_grievance_not_found` - Update 404 handling
12. ✅ `test_export_recent_grievances` - Export endpoint
13. ✅ `test_get_receipt_pdf` - PDF generation

## Writing New Tests

### Basic Test Structure

```python
def test_my_feature(client):
    """Test description"""
    # Arrange - prepare test data
    payload = {...}
    
    # Act - call the API
    response = client.post("/api/grievances/", json=payload)
    
    # Assert - verify results
    assert response.status_code == 200
    data = response.json()
    assert data["field"] == expected_value
```

### Using the Test Client

The `client` fixture provides a TestClient with access to all API endpoints:

```python
def test_example(client):
    # GET request
    response = client.get("/api/grievances/GRV-123...")
    
    # POST request
    response = client.post("/api/grievances/", json={...})
    
    # PUT request
    response = client.put("/api/grievances/GRV-123/status", json={...})
    
    # Check response
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines. Example GitHub Actions workflow:

```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build test image
        run: docker build -f backend/Dockerfile.test -t grievance-api-test backend/
      - name: Run tests
        run: docker run --rm grievance-api-test
```

## Troubleshooting

### Issue: Tests fail with database errors
**Solution:** Ensure the test database is using SQLite. Check `conftest.py` configuration.

### Issue: Import errors
**Solution:** Make sure all `__init__.py` files exist in the `app` and `tests` directories.

### Issue: Docker build fails
**Solution:** Verify all test files are included in the Docker context and not ignored by `.dockerignore`.

### Issue: Individual test fails
**Solution:** Run with verbose output:
```powershell
docker run --rm grievance-api-test pytest -v -s
```

## Code Coverage

To run tests with coverage report:

```powershell
docker run --rm grievance-api-test pytest --cov=app --cov-report=term-missing
```

This will show which lines of code are covered by tests.

## Next Steps

Consider adding tests for:
- Batch update endpoints
- File upload/attachment validation
- Integration with external services (Odoo)
- Performance/load testing
- Security testing (authentication, authorization)

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [TestClient Documentation](https://www.starlette.io/testclient/)
