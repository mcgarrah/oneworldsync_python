# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Completely migrate from READ v1 to READ v2 of the REST API
  - This involves migration from marketplace.1worldsync.com to content1-api.1worldsync.com
  - HMAC remains the same for now
  - v0.2.0 will be a complete rewrite to the new REST API endpoint

## [0.1.8] - 2025-05-13

### Added
- We've completely revamped the product data extraction functionality to make it easier for users to work with search results from the 1WorldSync Search REST API. Details in the commit history.

## [0.1.7] - 2025-05-12

### Added
- Release tasks and additional documentation
- CHANGELOG.md file added
- RELEASE.md file added

## [0.1.6] - 2025-05-12

### Added
- Swagger models for pre-prod and prod API for both Search and Fetch models
- GitHub Actions enhancements

### Changed
- Updated client library for new environment variable names

### Fixed
- Small documentation improvements

## [0.1.5] - 2025-05-11

### Added
- VS Code configuration for development workflow

### Fixed
- Small pylint and documentation fixes

## [0.1.4] - 2025-05-11

### Added
- Sphinx documentation for Read the Docs support

## [0.1.3] - 2025-05-11

### Added
- Comprehensive test suite with pytest
- VS Code configuration for development workflow
- Documentation with Sphinx and Read the Docs support
- Version management script

### Fixed
- Datetime compatibility issue for Python <3.11

## [0.1.2] - 2025-05-10

### Added
- Initial public release
- Basic API client functionality
- HMAC authentication
- Search and fetch capabilities
- Data models for API responses

## [0.1.1] - 2025-05-10

### Changed
- Refactored environment variables handling
- Fixed parameter ordering issues

## [0.1.0] - 2025-05-10

### Added
- Initial project setup
- PyPi workflow configuration
- License file
