# Release Process

This document outlines the process for releasing new versions of the OneWorldSync Python Client.

## Prerequisites

1. Install the GitHub CLI (`gh`):
   ```bash
   # For macOS
   brew install gh
   
   # For Linux
   sudo apt install gh  # Debian/Ubuntu
   sudo dnf install gh  # Fedora
   
   # For Windows
   winget install --id GitHub.cli
   ```

2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

## Release Process

### 1. Update Version Numbers

Use the version update script to update the version number in all necessary files:

```bash
python version_update.py X.Y.Z
```

This will update the version in:
- `oneworldsync/__init__.py`
- `pyproject.toml`
- `setup.py`

### 2. Update Changelog

Update the `CHANGELOG.md` file with the changes in the new version.

### 3. Create a Pull Request from Dev to Main

```bash
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
```

### 4. Review and Merge the Pull Request

```bash
# List open pull requests
gh pr list

# View the pull request
gh pr view [PR_NUMBER]

# Merge the pull request
gh pr merge [PR_NUMBER] --merge
```

### 5. Create a GitHub Release

```bash
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
```

### 6. Build and Upload to PyPI

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Example Release Process

Here's an example of releasing version 0.1.7:

```bash
# Update version numbers
python version_update.py 0.1.7

# Update changelog
# (Edit CHANGELOG.md manually)

# Commit and push changes
git add .
git commit -m "Bump version to v0.1.7"
git push origin dev

# Create a pull request
gh pr create --base main --head dev --title "Release v0.1.7" --body "Release version 0.1.7 with the following changes:
- Added new feature X
- Fixed bug Y
- Improved documentation Z"

# Merge the pull request (after review)
gh pr merge [PR_NUMBER] --merge

# Switch to main branch
git checkout main
git pull origin main

# Create a tag and push it
git tag v0.1.7
git push origin v0.1.7

# Create a GitHub release
gh release create v0.1.7 --title "Release v0.1.7" --notes "Release version 0.1.7 with the following changes:
- Added new feature X
- Fixed bug Y
- Improved documentation Z"

# Build and upload to PyPI
python -m build
python -m twine upload dist/*
```

## Automated Release with VS Code Tasks

You can also use VS Code tasks to automate parts of the release process. See the `.vscode/tasks.json` file for available tasks.