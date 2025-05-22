OneWorldSync Content1 API Python Client
=================================

A Python Client library module for accessing the 1WorldSync Content1 API.

.. image:: https://readthedocs.org/projects/oneworldsync-python/badge/?version=latest
   :target: https://oneworldsync-python.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/oneworldsync.svg
   :target: https://pypi.org/project/oneworldsync/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/oneworldsync.svg
   :target: https://pypi.org/project/oneworldsync/
   :alt: Python Versions

.. image:: https://img.shields.io/pypi/l/oneworldsync.svg
   :target: https://github.com/mcgarrah/oneworldsync_python/blob/main/LICENSE
   :alt: License

Key Features
-----------

* **HMAC Authentication**: Handles the complex HMAC authentication required by the 1WorldSync API.
* **Easy-to-use Client**: Provides a simple interface for interacting with the API.
* **Data Models**: Structured models for API responses, making it easier to work with the data.
* **Error Handling**: Custom exceptions for different types of errors.
* **Examples**: Ready-to-use example scripts demonstrating common use cases.

Installation
-----------

.. code-block:: bash

   pip install oneworldsync

Or install from source:

.. code-block:: bash

   git clone https://github.com/mcgarrah/oneworldsync_client.git
   cd oneworldsync_python
   pip install -e .

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user/installation
   user/authentication
   user/quickstart
   user/advanced_usage
   user/error_handling
   openapi

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/content1_client
   api/content1_auth
   api/models
   api/exceptions
   api/utils

.. toctree::
   :maxdepth: 1
   :caption: Development

   dev/contributing
   dev/testing
   dev/releasing
   dev/vscode

Indices and tables
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`