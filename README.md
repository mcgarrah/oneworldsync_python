# 1WorldSync Content1 API Python Client

A Python client for interacting with the 1WorldSync Content1 API.

## Installation

```bash
pip install oneworldsync
```

## Command Line Interface

The package includes a command-line tool called `ows` that provides quick access to common operations:

```bash
# Set up credentials (one-time setup)
mkdir -p ~/.ows
echo "ONEWORLDSYNC_APP_ID=your_app_id
ONEWORLDSYNC_SECRET_KEY=your_secret_key
ONEWORLDSYNC_USER_GLN=your_gln" > ~/.ows/credentials

# Test your credentials
ows login

# Count products
ows count
ows count --target-market US
ows count --last-days 30 --target-market US

# Fetch products
ows fetch --gtin 12345678901234
ows fetch --target-market US --output results.json
ows fetch --last-days 30 --target-market US

# Get products from the last 30 days
ows recent --target-market US

# Get product hierarchies
ows hierarchy --gtin 12345678901234
```

## Basic Usage

```python
from oneworldsync import Content1Client

# Initialize client with credentials
client = Content1Client(
    app_id="your_app_id",
    secret_key="your_secret_key",
    gln="your_gln"  # Optional
)

# Count products
count = client.count_products()
print(f"Total products: {count}")

# Fetch products by GTIN
products = client.fetch_products_by_gtin(["00000000000000"])

# Fetch products by target market
products = client.fetch_products_by_target_market("US")
```

## Using the Criteria Builder

The library provides a fluent interface for building search criteria:

```python
from oneworldsync import ProductCriteria, DateRangeCriteria, SortField

# Create criteria using the builder pattern
criteria = ProductCriteria() \
    .with_target_market("US") \
    .with_last_modified_date(DateRangeCriteria.last_30_days()) \
    .with_brand_name("Brand Name") \
    .with_sort([
        SortField.create("lastModifiedDate", descending=True)
    ])

# Use the criteria with the client
products = client.fetch_products(criteria)

# Process results
for product in products:
    print(f"{product.brand_name} - {product.gtin}")
```

## Convenience Methods

```python
# Get products from the last 30 days
products = client.fetch_products_last_30_days(target_market="US")

# Get products by date range
products = client.fetch_products_by_date_range(
    from_date="2023-01-01", 
    to_date="2023-01-31",
    target_market="US"
)

# Get products by brand
products = client.fetch_products_by_brand("Brand Name", target_market="US")

# Get products by GPC code
products = client.fetch_products_by_gpc_code("10000248", target_market="US")
```

## Pagination

```python
# Fetch first page
products = client.fetch_products(criteria, page_size=100)

# Process first page
for product in products:
    print(f"GTIN: {product.gtin}")

# Check if there are more pages
if products.search_after:
    # Fetch next page
    next_page = client.fetch_next_page(products, original_criteria=criteria)
```

## Documentation

For more detailed documentation, see the [full documentation](https://oneworldsync-python.readthedocs.io/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.