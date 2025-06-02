# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.5] - 2025-06-02

### Added
- Support for extracting nutritional information from food/beverage products
- New examples for nutritional data integration with Django
- Documentation for nutritional data structure and nutrient code mapping
- List of known food product GTINs with reliable nutritional information

### Fixed
- Corrected documentation on the location of nutritional information in the API response
- Updated README with key findings about nutritional data structure

## [0.2.4] - 2025-05-27

### Fixed
- Fixed `fetch_next_page` method to preserve original search criteria when fetching subsequent pages
- Added `original_criteria` parameter to `fetch_next_page` to maintain filtering across paginated requests

## [0.2.3] - 2025-05-24

### Added
- Added fields parameter for more granular control over returned data
- Improved GTIN handling in API requests
- Enhanced examples with real-world use cases

### Changed
- Removed default US target market from CLI tool
- Updated CLI documentation for clarity

### Fixed
- Fixed target-market examples to use valid market values (EU is not valid)

## [0.2.2] - 2025-05-23

### Added
- New command line interface (CLI) tool 'ows' for common Content1 API operations
- CLI commands for login verification, product fetching, counting, and hierarchy retrieval
- CLI configuration support via ~/.ows/credentials file
- Added --version option to CLI to display package version

## [0.2.1] - 2025-05-20

### Changed
- Complete migration from marketplace API to Content1 API
- Removed legacy marketplace API client and authentication
- Updated all documentation to focus on Content1 API
- Replaced legacy models with Content1-specific models
- Removed legacy example files

### Added
- New Content1-specific model classes: Content1Product, Content1ProductResults, Content1Hierarchy, Content1HierarchyResults
- OpenAPI 3.0.1 specification documentation
- Enhanced examples for Content1 API usage

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