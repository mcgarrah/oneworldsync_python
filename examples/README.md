# OneWorldSync Python Client Examples

This directory contains example scripts demonstrating how to use the OneWorldSync Python client.

## Setup

Before running the examples, make sure you have:

1. Installed the OneWorldSync Python client
2. Created a `.env` file in this directory with your credentials:

```
ONEWORLDSYNC_APP_ID=your_app_id
ONEWORLDSYNC_SECRET_KEY=your_secret_key
ONEWORLDSYNC_API_URL=api_url_if_not_using_default
```

## Available Examples

### Basic Examples

- **search_example.py**: Demonstrates basic product search functionality
- **advanced_search_example.py**: Shows how to use advanced search features
- **product_fetch_example.py**: Shows how to fetch detailed product information

### Enhanced Examples

- **enhanced_search_example.py**: Demonstrates the enhanced product data extraction functionality, making it easier to work with search results

## Running the Examples

```bash
# Make sure you're in the examples directory
cd examples

# Run an example
python search_example.py

# Run the enhanced search example
python enhanced_search_example.py
```

## Example Output

The enhanced search example will show:

1. Search metadata (total results, response code, etc.)
2. Detailed product information for each result
3. Examples of converting products and search results to dictionaries

This demonstrates how the enhanced functionality makes it easier to work with product data from the 1WorldSync API.