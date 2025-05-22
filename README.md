# 1WorldSync Python Client

A Python Client library module for accessing the 1WorldSync APIs, including both the Marketplace Search API and the Content1 API.

## Package Structure

``` text
oneworldsync_python/
├── oneworldsync/
│   ├── __init__.py      # Package exports
│   ├── auth.py          # HMAC authentication for Marketplace API
│   ├── client.py        # Main Marketplace API client
│   ├── content1_auth.py # HMAC authentication for Content1 API
│   ├── content1_client.py # Content1 API client
│   ├── exceptions.py    # Custom exceptions
│   ├── models.py        # Data models for API responses
│   └── utils.py         # Utility functions
├── examples/
│   ├── search_example.py           # Example for product search
│   ├── advanced_search_example.py  # Example for advanced product search
│   ├── product_fetch_example.py    # Example for fetching product details
│   ├── enhanced_search_example.py  # Example for enhanced data extraction
│   └── content1_example.py         # Example for Content1 API usage
├── tests/               # Test suite
│   ├── conftest.py      # Test configuration and fixtures
│   ├── test_auth.py     # Tests for authentication
│   ├── test_client.py   # Tests for API client
│   └── ...              # Other test files
├── README.md            # Documentation
├── .env.example         # Example environment variables file
└── setup.py             # Package installation
```

## Key Features

* **HMAC Authentication**: Handles the complex HMAC authentication required by the 1WorldSync APIs.
* **Easy-to-use Clients**: Provides simple interfaces for interacting with both Marketplace and Content1 APIs.
* **Data Models**: Structured models for API responses, making it easier to work with the data.
* **Enhanced Data Extraction**: Simplified access to product data with clean properties and dictionary conversion.
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

### Development Installation

To install with development dependencies:

```bash
pip install -e ".[dev]"
```

Or using the requirements files:

```bash
pip install -r requirements-dev.txt
```

## Authentication

The 1WorldSync APIs use HMAC authentication. You'll need an App ID and Secret Key from 1WorldSync.

You can store these credentials in a `.env` file:

``` ini
# For Marketplace API
ONEWORLDSYNC_APP_ID=your_app_id
ONEWORLDSYNC_SECRET_KEY=your_secret_key
ONEWORLDSYNC_API_URL=marketplace.api.1worldsync.com

# For Content1 API
ONEWORLDSYNC_USER_GLN=your_gln
ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com
```

**Important Note**: The 1WorldSync APIs are very particular about the order of parameters in the authentication process. The parameters must be in a specific order when constructing the string to hash. This library handles this complexity for you, ensuring that parameters are ordered correctly for authentication.

## Usage

### Marketplace API Usage

```python
from oneworldsync import OneWorldSyncClient
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
app_id = os.getenv("ONEWORLDSYNC_APP_ID")
secret_key = os.getenv("ONEWORLDSYNC_SECRET_KEY")

# Initialize client
client = OneWorldSyncClient(app_id, secret_key)

# Perform a free text search
results = client.free_text_search("milk")

# Print number of results
print(f"Found {len(results.products)} products")

# Print details of the first product
if results.products:
    product = results.products[0]
    print(f"Product: {product.brand_name} - {product.product_name}")
    print(f"Description: {product.description}")
```

### Content1 API Usage

```python
from oneworldsync import Content1Client
import os
import json
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
app_id = os.getenv("ONEWORLDSYNC_APP_ID")
secret_key = os.getenv("ONEWORLDSYNC_SECRET_KEY")
gln = os.getenv("ONEWORLDSYNC_USER_GLN")

# Initialize Content1 client
client = Content1Client(app_id, secret_key, gln)

# Count products
count = client.count_products()
print(f"Total products: {count}")

# Fetch products with criteria
criteria = {
    "targetMarket": "US",
    "lastModifiedDate": {
        "from": {
            "date": "2023-01-01",
            "op": "GTE"
        },
        "to": {
            "date": "2023-12-31",
            "op": "LTE"
        }
    }
}
products = client.fetch_products(criteria, page_size=10)

# Save the raw product details to a file for inspection
with open("content1_products.json", "w") as f:
    json.dump(products, f, indent=2)
```

### Enhanced Data Access (Marketplace API)

```python
# Search for products
results = client.free_text_search("milk")

# Access enhanced product properties
for product in results:
    print(f"ID: {product.item_id}")
    print(f"GTIN: {product.gtin}")
    print(f"Brand: {product.brand_name}")
    print(f"Name: {product.product_name}")
    print(f"Primary Image: {product.primary_image_url}")
    print(f"Dimensions: {product.formatted_dimensions}")
    
    # Convert to dictionary for easier handling
    product_dict = product.to_dict()
    
# Convert entire search results to dictionary
results_dict = results.to_dict()
```

### Advanced Search (Marketplace API)

```python
# Search for a product by UPC
results = client.advanced_search("itemIdentifier", "16241419122223")

# Search with geo location
results = client.free_text_search(
    "coffee",
    geo_location=(37.7749, -122.4194)  # San Francisco coordinates
)
```

### Working with Products (Marketplace API)

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

### Content1 API - Fetching Products

```python
# Fetch products by GTIN
gtins = ["00000000000000"]  # Replace with actual GTINs
products = client.fetch_products_by_gtin(gtins)

# Fetch products by Information Provider GLN
ip_gln = "0838016005012"  # Replace with actual GLN
products = client.fetch_products_by_ip_gln(ip_gln)

# Fetch products by target market
target_market = "US"
products = client.fetch_products_by_target_market(target_market)

# Fetch next page of products
if "searchAfter" in products:
    next_page = client.fetch_next_page(products)
```

## Error Handling

```python
from oneworldsync import OneWorldSyncClient, Content1Client, AuthenticationError, APIError

try:
    # For Marketplace API
    marketplace_client = OneWorldSyncClient(app_id, secret_key)
    results = marketplace_client.free_text_search("apple")
    
    # For Content1 API
    content1_client = Content1Client(app_id, secret_key)
    products = content1_client.count_products()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
```

## Development

### VS Code Integration

This project includes VS Code configuration files to streamline development:

#### Debug Configurations (launch.json)

- **Python: Current File** - Run and debug the currently open file
- **Python: Search Example** - Run the basic search example
- **Python: Advanced Search Example** - Run the advanced search example
- **Python: Product Fetch Example** - Run the product fetch example
- **Python: Debug Tests** - Debug the current test file
- **Python: All Tests** - Run all tests with verbose output
- **Python: Tests with Coverage** - Run tests with coverage reporting

To use these configurations, press F5 or select from the debug dropdown in VS Code.

#### Tasks (tasks.json)

Run common development tasks with `Ctrl+Shift+P` → "Tasks: Run Task":

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

### Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"
# or
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=oneworldsync
```

### Version Management

To update the version number across all files (`oneworldsync/__init__.py`, `pyproject.toml`, and `setup.py`), use the provided script:

```bash
# Update to version 0.1.4
python version_update.py 0.1.4
```

## Troubleshooting

If you encounter authentication issues, check that:

1. Your ONEWORLDSYNC_APP_ID and ONEWORLDSYNC_SECRET_KEY are correct
2. You're using the correct environment (production vs. preprod) for your credentials
3. Your system clock is synchronized (timestamp accuracy is important for authentication)

For API errors with status code 400, check the response message for details about which parameters might be invalid.