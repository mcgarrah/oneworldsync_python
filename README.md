# 1WorldSync Python Client

A comprehensive Python Client library module for accessing the 1WorldSync REST API.

## Package Structure

``` text
oneworldsync_python/
├── oneworldsync/
│   ├── __init__.py      # Package exports
│   ├── auth.py          # HMAC authentication
│   ├── client.py        # Main API client
│   ├── exceptions.py    # Custom exceptions
│   ├── models.py        # Data models for API responses
│   └── utils.py         # Utility functions
├── examples/
│   ├── search_example.py        # Example for product search
│   └── product_fetch_example.py # Example for fetching product details
├── README.md            # Documentation
└── setup.py             # Package installation
```

## Key Features

* **HMAC Authentication**: Handles the complex HMAC authentication required by the 1WorldSync API.
* **Easy-to-use Client**: Provides a simple interface for interacting with the API.
* **Data Models**: Structured models for API responses, making it easier to work with the data.
* **Error Handling**: Custom exceptions for different types of errors.
* **Examples**: Ready-to-use example scripts demonstrating common use cases.

## Installation

```bash
pip install oneworldsync
```

Or install from source:

```bash
git clone https://github.com/mcgarrah/oneworldsync_client.git
cd oneworldsync_python
pip install -e .
```

## Authentication

The 1WorldSync API uses HMAC authentication. You'll need an App ID and Secret Key from 1WorldSync.

You can store these credentials in a `.env` file:

``` ini
APP_ID=your_app_id
SECRET_KEY=your_secret_key
```

**Important Note**: The 1WorldSync API is very particular about the order of parameters in the authentication process. The parameters must be in a specific order when constructing the string to hash. This library handles this complexity for you, ensuring that parameters are ordered correctly for authentication.

## Usage

### Basic Usage

```python
from oneworldsync import OneWorldSyncClient
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
app_id = os.getenv("APP_ID")
secret_key = os.getenv("SECRET_KEY")

# Initialize client
client = OneWorldSyncClient(app_id, secret_key)

# Perform a free text search
results = client.free_text_search("apple")

# Print number of results
print(f"Found {len(results.products)} products")

# Print details of the first product
if results.products:
    product = results.products[0]
    print(f"Product: {product.brand_name} - {product.product_name}")
    print(f"Description: {product.description}")
```

### Advanced Search

```python
# Search for a product by UPC
results = client.advanced_search("itemPrimaryId", "00007252147019")

# Search with geo location
results = client.free_text_search(
    "coffee",
    geo_location=(37.7749, -122.4194)  # San Francisco coordinates
)
```

### Working with Products

```python
# Get a specific product by ID
product_data = client.get_product("some_product_id")

# Access product attributes
for product in results.products:
    print(f"ID: {product.item_id}")
    print(f"Brand: {product.brand_name}")
    print(f"Name: {product.product_name}")
    print(f"Description: {product.description}")
    
    # Get product dimensions
    dimensions = product.dimensions
    if dimensions:
        print(f"Dimensions: {dimensions['height']['value']} {dimensions['height']['unit']} x "
              f"{dimensions['width']['value']} {dimensions['width']['unit']} x "
              f"{dimensions['depth']['value']} {dimensions['depth']['unit']}")
    
    # Get product images
    for image in product.images:
        print(f"Image URL: {image['url']} (Primary: {image['is_primary']})")
```

## Error Handling

```python
from oneworldsync import OneWorldSyncClient, AuthenticationError, APIError

try:
    client = OneWorldSyncClient(app_id, secret_key)
    results = client.free_text_search("apple")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
```

## Development

### Running Tests

```bash
pytest
```

## Troubleshooting

If you encounter authentication issues, check that:

1. Your APP_ID and SECRET_KEY are correct
2. You're using the correct environment (production vs. preprod)
3. Your system clock is synchronized (timestamp accuracy is important for authentication)

For API errors with status code 400, check the response message for details about which parameters might be invalid.