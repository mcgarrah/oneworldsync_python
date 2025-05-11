Testing
=======

This document provides information about testing the OneWorldSync Python Client.

Test Structure
------------

The test suite is organized as follows:

- ``tests/conftest.py``: Contains pytest fixtures used across multiple test files
- ``tests/test_auth.py``: Tests for the authentication module
- ``tests/test_client.py``: Tests for the API client
- ``tests/test_models.py``: Tests for the data models
- ``tests/test_exceptions.py``: Tests for the custom exceptions
- ``tests/test_utils.py``: Tests for the utility functions
- ``tests/test_integration.py``: Integration tests that make actual API calls

Running Tests
-----------

To run the tests, use pytest:

.. code-block:: bash

   # Run all tests
   pytest

   # Run tests with verbose output
   pytest -v

   # Run a specific test file
   pytest tests/test_client.py

   # Run a specific test
   pytest tests/test_client.py::test_client_init_with_params

Integration Tests
---------------

Integration tests are disabled by default because they require valid API credentials and will make actual API calls. To enable them, set the ``ONEWORLDSYNC_RUN_INTEGRATION_TESTS`` environment variable to ``true``:

.. code-block:: bash

   # Enable integration tests
   export ONEWORLDSYNC_RUN_INTEGRATION_TESTS=true
   pytest tests/test_integration.py

Test Coverage
-----------

To run tests with coverage reporting:

.. code-block:: bash

   # Install pytest-cov if not already installed
   pip install pytest-cov

   # Run tests with coverage
   pytest --cov=oneworldsync

   # Generate HTML coverage report
   pytest --cov=oneworldsync --cov-report=html

Mocking
------

Most tests use mocking to avoid making actual API calls. The ``unittest.mock`` module is used to mock:

- API responses
- Authentication
- Environment variables

Adding New Tests
--------------

When adding new tests:

1. Follow the existing pattern of test files
2. Use fixtures from ``conftest.py`` where appropriate
3. Mock external dependencies
4. Test both success and error cases
5. Add docstrings to explain what each test is checking