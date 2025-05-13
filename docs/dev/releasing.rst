Releasing
=========

This document describes the process for releasing new versions of the OneWorldSync Python Client.

Prerequisites
------------

1. Install the GitHub CLI (``gh``):

   .. code-block:: bash

      # For macOS
      brew install gh
      
      # For Linux
      sudo apt install gh  # Debian/Ubuntu
      sudo dnf install gh  # Fedora
      
      # For Windows
      winget install --id GitHub.cli

2. Authenticate with GitHub:

   .. code-block:: bash

      gh auth login

3. Install build and twine:

   .. code-block:: bash

      pip install build twine

Version Numbering
---------------

This project follows `Semantic Versioning <https://semver.org/>`_:

- **MAJOR** version for incompatible API changes
- **MINOR** version for adding functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

Release Process
-------------

You can release using either the CLI method or the VS Code method.

CLI Method
~~~~~~~~~

1. Update Version Numbers
^^^^^^^^^^^^^^^^^^^^^^^

Use the version update script to update the version number in all necessary files:

.. code-block:: bash

   python version_update.py X.Y.Z

This will update the version in:

- ``oneworldsync/__init__.py``
- ``pyproject.toml``
- ``setup.py``

2. Update Changelog
^^^^^^^^^^^^^^^^

Update the ``CHANGELOG.md`` file with the changes in the new version.

3. Create a Pull Request from Dev to Main
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Ensure you're on the dev branch with latest changes
   git checkout dev
   git pull origin dev

   # Commit version changes
   git add .
   git commit -m "Bump version to vX.Y.Z"
   git push origin dev

   # Create a pull request
   gh pr create --base main --head dev --title "Release vX.Y.Z" --body "Release version X.Y.Z with the following changes:
   - Feature 1
   - Feature 2
   - Bug fix 1"

4. Review and Merge the Pull Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # List open pull requests
   gh pr list

   # View the pull request
   gh pr view [PR_NUMBER]

   # Merge the pull request
   gh pr merge [PR_NUMBER] --merge

5. Create a GitHub Release
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Switch to main branch
   git checkout main
   git pull origin main

   # Create a tag
   git tag vX.Y.Z
   git push origin vX.Y.Z

   # Create a GitHub release
   gh release create vX.Y.Z --title "Release vX.Y.Z" --notes "Release version X.Y.Z with the following changes:
   - Feature 1
   - Feature 2
   - Bug fix 1"

6. Build and Upload to PyPI
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Build the package
   python -m build

   # Upload to PyPI
   python -m twine upload dist/*

VS Code Method
~~~~~~~~~~~~

VS Code tasks are provided to automate the release process. This method uses the same steps as the CLI method but with a more user-friendly interface.

1. Prepare for Release
^^^^^^^^^^^^^^^^^^^

Before starting, make sure:

- You have the latest changes from the dev branch
- All tests are passing
- You have updated the CHANGELOG.md file

2. Run the Release Tasks
^^^^^^^^^^^^^^^^^^^^^

a. **Start the Release Process**:

   1. Press ``Ctrl+Shift+P`` (or ``Cmd+Shift+P`` on Mac)
   2. Type "Tasks: Run Task"
   3. Select "Release: Complete Process"
   4. Enter the version number when prompted (e.g., "0.1.7")
   5. Enter the release notes when prompted

   This will run the first three steps in sequence:
   
   - Update version numbers in all files
   - Commit and push the changes to the dev branch
   - Create a pull request from dev to main

b. **After PR Review**:

   Once the pull request has been reviewed and approved:

   1. Press ``Ctrl+Shift+P`` (or ``Cmd+Shift+P`` on Mac)
   2. Type "Tasks: Run Task"
   3. Select "Release: 4. Merge Pull Request"
   4. Enter the pull request number when prompted

c. **Create the GitHub Release**:

   1. Press ``Ctrl+Shift+P`` (or ``Cmd+Shift+P`` on Mac)
   2. Type "Tasks: Run Task"
   3. Select "Release: 5. Create GitHub Release"
   4. Enter the version number when prompted
   5. Enter the release notes when prompted

   This task will:
   
   - Switch to the main branch
   - Pull the latest changes
   - Create and push a tag with the version number
   - Create a GitHub release with the provided notes

d. **Publish to PyPI**:

   1. Press ``Ctrl+Shift+P`` (or ``Cmd+Shift+P`` on Mac)
   2. Type "Tasks: Run Task"
   3. Select "Release: 6. Build and Upload to PyPI"

   This task will build the package and upload it to PyPI.

3. Individual Tasks
^^^^^^^^^^^^^^^^

You can also run individual tasks as needed:

- **Release: 1. Update Version** - Update version numbers in all files
- **Release: 2. Commit Version Changes** - Commit and push version changes
- **Release: 3. Create Pull Request** - Create a pull request from dev to main
- **Release: 4. Merge Pull Request** - Merge the pull request
- **Release: 5. Create GitHub Release** - Create a GitHub release with tag
- **Release: 6. Build and Upload to PyPI** - Build and upload to PyPI

Each task will prompt for necessary information like version number and release notes.

Post-Release
-----------

After releasing, update the version number to the next development version:

.. code-block:: bash

   python version_update.py X.Y.(Z+1)-dev

Commit this change:

.. code-block:: bash

   git checkout dev
   git add .
   git commit -m "Bump version to X.Y.(Z+1)-dev"
   git push origin dev