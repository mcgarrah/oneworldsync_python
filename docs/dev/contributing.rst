Contributing
============

Thank you for your interest in contributing to the OneWorldSync Python Client! This document provides guidelines and instructions for contributing to the project.

Setting Up Development Environment
--------------------------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/mcgarrah/oneworldsync_python.git
      cd oneworldsync_python

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install development dependencies:

   .. code-block:: bash

      pip install -e ".[dev]"

Code Style
---------

This project follows the PEP 8 style guide. We use the following tools to maintain code quality:

- **Black**: For code formatting
- **Flake8**: For style guide enforcement
- **isort**: For import sorting
- **mypy**: For type checking

You can run these tools using:

.. code-block:: bash

   # Format code
   black oneworldsync tests

   # Sort imports
   isort oneworldsync tests

   # Check style
   flake8 oneworldsync tests

   # Type checking
   mypy oneworldsync

Pull Request Process
------------------

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass (`pytest`)
5. Update documentation if necessary
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

Commit Message Guidelines
-----------------------

Please follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Testing
------

All new code should include tests. Run the test suite with:

.. code-block:: bash

   pytest

To run tests with coverage:

.. code-block:: bash

   pytest --cov=oneworldsync

Documentation
------------

Please update documentation when necessary. You can build the documentation locally with:

.. code-block:: bash

   cd docs
   make html

Then open `_build/html/index.html` in your browser.