# 1WorldSync Content1 API Python Client

A Python client for interacting with the 1WorldSync Content1 API.

## Installation

```bash
pip install oneworldsync
```

## Key Features

- Authentication with HMAC
- Product fetching by GTIN, GLN, or target market
- Product hierarchy retrieval
- Pagination support
- Comprehensive error handling
- Content1-specific data models
- OpenAPI 3.0.1 specification support
- Command Line Interface (CLI)

## Package Structure

```
oneworldsync/
├── __init__.py           # Package initialization and version
├── content1_client.py    # Main Content1 API client
├── content1_auth.py      # HMAC authentication for Content1 API
├── cli.py               # Command Line Interface
├── models.py            # Data models for API responses
├── exceptions.py        # Custom exceptions
└── utils.py             # Utility functions
```

## Quick Start

### Python API

```python
from oneworldsync import Content1Client

# Initialize the client
client = Content1Client(
    app_id='your_app_id',
    secret_key='your_secret_key',
    gln='your_gln'  # Optional
)

# Count products
count = client.count_products()
print(f"Total products: {count}")

# Fetch products by GTIN
products = client.fetch_products_by_gtin(['00000000000000'])
print(f"Found {len(products.get('items', []))} products")

# Fetch products with criteria
criteria = {
    "targetMarket": "US",
    "fields": {
        "include": ["gtin", "brandName", "gpcCategory"]
    }
}
results = client.fetch_products(criteria)
```

### Command Line Interface

The package installs a command-line tool called `ows` that can be used to interact with the Content1 API:

```bash
# Test login credentials
ows login

# Fetch products
ows fetch --gtin 12345678901234 --target-market US
ows fetch --output results.json

# Count products
ows count --target-market EU
ows count --output count.json

# Fetch product hierarchies
ows hierarchy --gtin 12345678901234
ows hierarchy --output hierarchy.json
```

The CLI requires credentials to be stored in `~/.ows/credentials` file:
```
ONEWORLDSYNC_APP_ID=your_app_id
ONEWORLDSYNC_SECRET_KEY=your_secret_key
ONEWORLDSYNC_USER_GLN=your_gln  # Optional
ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com  # Optional
```

## Authentication

The client supports authentication using your 1WorldSync Content1 API credentials:

```python
# Using parameters
client = Content1Client(
    app_id='your_app_id',
    secret_key='your_secret_key',
    gln='your_gln'  # Optional
)

# Using environment variables
# ONEWORLDSYNC_APP_ID
# ONEWORLDSYNC_SECRET_KEY
# ONEWORLDSYNC_USER_GLN (optional)
# ONEWORLDSYNC_CONTENT1_API_URL (optional)
client = Content1Client()
```

## Examples

See the [examples](examples/) directory for more detailed usage examples:

### Basic Example (content1_example.py)
Basic usage of the Content1 API client to fetch products.

### Advanced Example (content1_advanced_example.py)
```python
# Create a date range for the last 30 days
today = datetime.datetime.now()
thirty_days_ago = today - datetime.timedelta(days=30)

date_criteria = {
    "lastModifiedDate": {
        "from": {
            "date": thirty_days_ago.strftime("%Y-%m-%d"),
            "op": "GTE"
        },
        "to": {
            "date": today.strftime("%Y-%m-%d"),
            "op": "LTE"
        }
    }
}

# Fetch products with specific fields and sorting
fetch_criteria = {
    "targetMarket": "US",
    "lastModifiedDate": date_criteria["lastModifiedDate"],
    "fields": {
        "include": [
            "gtin", "informationProviderGLN", "targetMarket",
            "lastModifiedDate", "brandName", "gpcCategory"
        ]
    },
    "sortFields": [
        {"field": "lastModifiedDate", "desc": True},
        {"field": "gtin", "desc": False}
    ]
}

# Fetch first page with pagination
products = client.fetch_products(fetch_criteria, page_size=10)

# Handle pagination
if "searchAfter" in products:
    next_page_criteria = fetch_criteria.copy()
    next_page_criteria["searchAfter"] = products["searchAfter"]
    next_page = client.fetch_products(next_page_criteria, page_size=10)
```

## Documentation

For more detailed documentation, see the [docs](docs/) directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.