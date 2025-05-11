"""
Pytest configuration for 1WorldSync tests
"""

import os
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_credentials():
    """Fixture to provide mock credentials for testing"""
    return {
        'app_id': 'test_app_id',
        'secret_key': 'test_secret_key',
        'api_url': 'test.api.1worldsync.com'
    }


@pytest.fixture
def mock_env_credentials(monkeypatch):
    """Fixture to mock environment variables for credentials"""
    monkeypatch.setenv('ONEWORLDSYNC_APP_ID', 'env_app_id')
    monkeypatch.setenv('ONEWORLDSYNC_SECRET_KEY', 'env_secret_key')
    monkeypatch.setenv('ONEWORLDSYNC_API_URL', 'env.api.1worldsync.com')


@pytest.fixture
def mock_response():
    """Fixture to provide a mock API response"""
    return {
        'responseCode': '0',
        'responseMessage': 'Success',
        'totalNumOfResults': '2',
        'nextCursorMark': 'cursor123',
        'results': [
            {
                'item': {
                    'itemIdentificationInformation': {
                        'itemIdentifier': [
                            {
                                'isPrimary': 'true',
                                'itemId': 'item123'
                            }
                        ]
                    },
                    'tradeItemInformation': [
                        {
                            'tradeItemDescriptionModule': {
                                'tradeItemDescriptionInformation': [
                                    {
                                        'brandNameInformation': {
                                            'brandName': 'Test Brand'
                                        },
                                        'regulatedProductName': [
                                            {
                                                'statement': {
                                                    'values': [
                                                        {
                                                            'value': 'Test Product'
                                                        }
                                                    ]
                                                }
                                            }
                                        ],
                                        'additionalTradeItemDescription': {
                                            'values': [
                                                {
                                                    'value': 'Test Description'
                                                }
                                            ]
                                        }
                                    }
                                ]
                            },
                            'referencedFileDetailInformationModule': {
                                'referencedFileHeader': [
                                    {
                                        'referencedFileTypeCode': {
                                            'value': 'PRODUCT_IMAGE'
                                        },
                                        'uniformResourceIdentifier': 'https://example.com/image.jpg',
                                        'isPrimaryFile': {
                                            'value': 'true'
                                        }
                                    }
                                ]
                            },
                            'tradeItemMeasurementsModuleGroup': [
                                {
                                    'tradeItemMeasurementsModule': {
                                        'tradeItemMeasurements': {
                                            'height': {
                                                'value': '10',
                                                'qual': 'CM'
                                            },
                                            'width': {
                                                'value': '20',
                                                'qual': 'CM'
                                            },
                                            'depth': {
                                                'value': '30',
                                                'qual': 'CM'
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            {
                'item': {
                    'itemIdentificationInformation': {
                        'itemIdentifier': [
                            {
                                'isPrimary': 'true',
                                'itemId': 'item456'
                            }
                        ]
                    },
                    'tradeItemInformation': [
                        {
                            'tradeItemDescriptionModule': {
                                'tradeItemDescriptionInformation': [
                                    {
                                        'brandNameInformation': {
                                            'brandName': 'Another Brand'
                                        },
                                        'regulatedProductName': [
                                            {
                                                'statement': {
                                                    'values': [
                                                        {
                                                            'value': 'Another Product'
                                                        }
                                                    ]
                                                }
                                            }
                                        ],
                                        'additionalTradeItemDescription': {
                                            'values': [
                                                {
                                                    'value': 'Another Description'
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }