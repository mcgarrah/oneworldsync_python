Installation
============

Requirements
-----------

* Python 3.12 or higher
* ``requests`` library
* ``python-dotenv`` library (optional, for loading environment variables)
* ``click`` library (for command line interface)

Installing from PyPI
-------------------

The recommended way to install the OneWorldSync Python Client is from PyPI:

.. code-block:: bash

   pip install oneworldsync

This will install the latest stable version of the package along with its dependencies and the ``ows`` command line tool.

Installing from Source
--------------------

You can also install the package directly from the source code:

.. code-block:: bash

   git clone https://github.com/mcgarrah/oneworldsync_python.git
   cd oneworldsync_python
   pip install -e .

Development Installation
----------------------

If you want to contribute to the development of the package, you can install it with development dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

Or using the requirements files:

.. code-block:: bash

   pip install -r requirements-dev.txt

Documentation Installation
------------------------

To build the documentation locally, install the package with documentation dependencies:

.. code-block:: bash

   pip install -e ".[docs]"

Or using the requirements file:

.. code-block:: bash

   pip install -r requirements-docs.txt

CLI Configuration
---------------

After installation, configure the CLI by creating a credentials file at ``~/.ows/credentials`` with the following format:

.. code-block:: bash

    ONEWORLDSYNC_APP_ID=your_app_id
    ONEWORLDSYNC_SECRET_KEY=your_secret_key
    ONEWORLDSYNC_USER_GLN=your_gln  # Optional
    ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com  # Optional