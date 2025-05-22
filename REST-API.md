# 1WorldSync API Documentation

This document provides information about the 1WorldSync APIs supported by this client library.

## Supported APIs

This client library supports two main 1WorldSync APIs:

1. **Marketplace API** - Used for product search and retrieval
2. **Content1 API** - Used for product count, fetch, and hierarchy operations

## Marketplace API

The Marketplace API provides endpoints for searching and retrieving product information.

### Key Endpoints

- **Free Text Search** - Search for products using free text
- **Advanced Search** - Search for products using specific fields
- **Product Retrieval** - Get detailed information about a specific product

### Authentication

The Marketplace API uses HMAC authentication with the following parameters:

- `app_id` - Your application ID
- `hash_code` - HMAC-SHA256 hash of the request URI
- `TIMESTAMP` - Current timestamp in ISO 8601 format

## Content1 API

The Content1 API provides endpoints for counting, fetching, and retrieving hierarchy information for products.

### Key Endpoints

- **Product Count** (`/V1/product/count`) - Count products matching specific criteria
- **Product Fetch** (`/V1/product/fetch`) - Fetch products matching specific criteria
- **Product Hierarchy** (`/V1/product/hierarchy`) - Fetch hierarchy information for products

### Authentication

The Content1 API uses HMAC authentication with the following headers:

- `appId` - Your application ID
- `hashcode` - HMAC-SHA256 hash of the request URI
- `gln` (optional) - Your Global Location Number

### Request Format

#### Product Count Request

```json
POST /V1/product/count?timestamp=2023-02-28T13:37:59Z
Headers:
  appId: your_app_id
  hashcode: generated_hash_code
  gln: your_gln (optional)

Body:
{
  "gtin": ["00000000000000"],
  "ipGln": "0838016005012",
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
```

#### Product Fetch Request

```json
POST /V1/product/fetch?timestamp=2023-02-28T13:37:59Z&pageSize=1000
Headers:
  appId: your_app_id
  hashcode: generated_hash_code
  gln: your_gln (optional)

Body:
{
  "gtin": ["00000000000000"],
  "ipGln": "0838016005012",
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
  },
  "fields": {
    "include": [
      "gtin",
      "informationProviderGLN",
      "targetMarket",
      "lastModifiedDate",
      "brandName",
      "gpcCategory"
    ]
  }
}
```

### Response Format

#### Product Count Response

```json
{
  "count": 1000
}
```

#### Product Fetch Response

```json
{
  "items": [
    {
      "gln": "0838016005012",
      "dataPoolType": "SDP",
      "item": {
        // Product data
      }
    }
  ],
  "totalPages": 10,
  "currentPage": 1,
  "totalCount": 1000,
  "searchAfter": ["00637827872406", "US"],
  "message": "To retrieve the next page of products, pick what you have received in searchAfter and set it in next request."
}
```

## Pagination

The Content1 API uses cursor-based pagination with the `searchAfter` parameter. To retrieve the next page of results:

1. Extract the `searchAfter` value from the response
2. Include it in the next request's criteria

Example:

```python
# First page
response = client.fetch_products(criteria)

# Get searchAfter value
search_after = response.get("searchAfter")

# Next page
if search_after:
    criteria["searchAfter"] = search_after
    next_page = client.fetch_products(criteria)
```

## Error Handling

The API may return various error codes:

- **401** - Authentication error (invalid credentials)
- **400** - Bad request (invalid parameters)
- **500** - Internal server error

Error responses include:

```json
{
  "requestId": "12222",
  "code": "REQUIRED_HEADER_APPID_MISSING",
  "reason": "appId is missing in header"
}
```

## References

For more detailed information, refer to the official 1WorldSync API documentation:

- Content1 API: https://content1-api.1worldsync.com/v3/api-docs