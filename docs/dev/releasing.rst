Releasing
=========

This document describes the process for releasing new versions of the OneWorldSync Python Client.

Version Numbering
---------------

This project follows `Semantic Versioning <https://semver.org/>`_:

- **MAJOR** version for incompatible API changes
- **MINOR** version for adding functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

Release Process
-------------

1. Update Version Numbers
~~~~~~~~~~~~~~~~~~~~~~~

Use the version update script to update the version number in all necessary files:

.. code-block:: bash

   python version_update.py X.Y.Z

This will update the version in:

- ``oneworldsync/__init__.py``
- ``pyproject.toml``
- ``setup.py``

2. Update Changelog
~~~~~~~~~~~~~~~~

Update the ``CHANGELOG.md`` file with the changes in the new version.

3. Create a Release Commit
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "Release vX.Y.Z"
   git tag vX.Y.Z
   git push origin main
   git push origin vX.Y.Z

4. Build and Upload to PyPI
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build the package
   python -m build

   # Upload to PyPI
   python -m twine upload dist/*

5. Create GitHub Release
~~~~~~~~~~~~~~~~~~~~~

Create a new release on GitHub:

1. Go to the repository's Releases page
2. Click "Draft a new release"
3. Select the tag you just created
4. Add release notes (can be copied from the changelog)
5. Publish the release

6. Update Documentation
~~~~~~~~~~~~~~~~~~~~

Ensure that the documentation on Read the Docs is updated:

1. Go to the Read the Docs project page
2. Trigger a new build if necessary

Post-Release
-----------

After releasing, update the version number to the next development version:

.. code-block:: bash

   python version_update.py X.Y.(Z+1)-dev

Commit this change:

.. code-block:: bash

   git add .
   git commit -m "Bump version to X.Y.(Z+1)-dev"
   git push origin main