VS Code Integration
=================

This project includes VS Code configuration files to streamline development. These files are located in the ``.vscode`` directory and provide a comprehensive development environment.

Debug Configurations
------------------

The ``launch.json`` file contains debug configurations for running and debugging your code:

- **Python: Current File** - Run and debug the currently open file
- **Python: Search Example** - Run the basic search example
- **Python: Advanced Search Example** - Run the advanced search example
- **Python: Product Fetch Example** - Run the product fetch example
- **Python: Debug Tests** - Debug the current test file
- **Python: All Tests** - Run all tests with verbose output
- **Python: Tests with Coverage** - Run tests with coverage reporting

Key features:

- Sets ``PYTHONPATH`` to include the workspace folder
- Disables "justMyCode" to allow debugging into libraries
- Uses integrated terminal for better output

To use these configurations:

1. Open a file you want to debug
2. Set breakpoints by clicking in the gutter
3. Press F5 or select a configuration from the debug dropdown

Tasks
-----

The ``tasks.json`` file defines common development tasks that can be run with ``Ctrl+Shift+P`` → "Tasks: Run Task":

- **Run Tests** - Run pytest on the project
- **Run Tests with Coverage** - Run tests with coverage reporting
- **Lint with Flake8** - Check code style with Flake8
- **Format with Black** - Format code with Black
- **Sort imports with isort** - Sort imports with isort
- **Type check with mypy** - Run static type checking
- **Build Documentation** - Build Sphinx documentation
- **Update Version** - Run the version update script with a prompt for the new version
- **Install Development Dependencies** - Install dev dependencies
- **Install Documentation Dependencies** - Install docs dependencies

To run a task:

1. Press ``Ctrl+Shift+P`` (or ``Cmd+Shift+P`` on Mac)
2. Type "Tasks: Run Task"
3. Select the task you want to run

Settings
-------

The ``settings.json`` file contains Python-specific settings:

- **Linting** - Enabled Flake8 and mypy
- **Formatting** - Set Black as the formatter with 100 character line length
- **Testing** - Configured pytest as the test framework
- **Editor** - Set format on save and organize imports on save
- **File Exclusions** - Hide common Python cache and build directories
- **Docstrings** - Set Google style for auto-generated docstrings

Extensions
---------

For the best development experience, we recommend installing the following VS Code extensions:

- **Python** - Microsoft's Python extension
- **Pylance** - Language server with rich type information
- **Python Test Explorer** - Test explorer integration for pytest
- **Python Docstring Generator** - Generate docstrings automatically
- **autoDocstring** - Python docstring generator
- **Black Formatter** - Black integration for VS Code
- **Flake8** - Flake8 integration for VS Code
- **isort** - Import sorting integration for VS Code
- **markdownlint** - Markdown linting

You can install these extensions by searching for them in the VS Code extensions panel (``Ctrl+Shift+X``).