"""
Pytest configuration for 1WorldSync Content1 API tests
"""

import os
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_content1_credentials():
    """Fixture to provide mock Content1 API credentials for testing"""
    return {
        'app_id': 'test_app_id',
        'secret_key': 'test_secret_key',
        'gln': 'test_gln',
        'api_url': 'https://test.content1-api.1worldsync.com'
    }


@pytest.fixture
def mock_content1_env_credentials(monkeypatch):
    """Fixture to mock environment variables for Content1 API credentials"""
    monkeypatch.setenv('ONEWORLDSYNC_APP_ID', 'env_app_id')
    monkeypatch.setenv('ONEWORLDSYNC_SECRET_KEY', 'env_secret_key')
    monkeypatch.setenv('ONEWORLDSYNC_USER_GLN', 'env_gln')
    monkeypatch.setenv('ONEWORLDSYNC_CONTENT1_API_URL', 'https://env.content1-api.1worldsync.com')


@pytest.fixture
def mock_content1_response():
    """Fixture to provide a mock Content1 API response"""
    return {
        'items': [
            {
                'gtin': '00000000000001',
                'informationProviderGLN': '1234567890123',
                'targetMarket': 'US',
                'lastModifiedDate': '2023-01-01T12:00:00Z',
                'item': {
                    'brandName': 'Test Brand',
                    'gpcCategory': '10000000'
                }
            },
            {
                'gtin': '00000000000002',
                'informationProviderGLN': '1234567890123',
                'targetMarket': 'US',
                'lastModifiedDate': '2023-01-02T12:00:00Z',
                'item': {
                    'brandName': 'Another Brand',
                    'gpcCategory': '20000000'
                }
            }
        ],
        'searchAfter': 'next_page_token'
    }


@pytest.fixture
def mock_content1_hierarchy_response():
    """Fixture to provide a mock Content1 API hierarchy response"""
    return {
        'hierarchies': [
            {
                'gtin': '00000000000001',
                'informationProviderGLN': '1234567890123',
                'targetMarket': 'US',
                'hierarchy': [
                    {
                        'parentGtin': '00000000000001',
                        'gtin': '00000000000002',
                        'quantity': 2,
                        'children': [
                            {
                                'parentGtin': '00000000000002',
                                'gtin': '00000000000003',
                                'quantity': 3
                            }
                        ]
                    }
                ]
            }
        ],
        'searchAfter': 'next_hierarchy_token'
    }