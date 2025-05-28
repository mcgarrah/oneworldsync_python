# 1WorldSync Content1 API Examples

This directory contains example scripts demonstrating how to use the 1WorldSync Content1 API Python client.

## Available Examples

- `content1_example.py`: Basic example of using the Content1 API client to fetch products
- `content1_advanced_example.py`: Advanced example showing more complex queries and pagination

## Setup

1. Install the package:
```
pip install oneworldsync
```

2. Create a `.env` file with your credentials:
```
ONEWORLDSYNC_APP_ID=your_app_id
ONEWORLDSYNC_SECRET_KEY=your_secret_key
ONEWORLDSYNC_USER_GLN=your_gln
ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com
```

3. Run an example:
```
python content1_example.py
```

## API Documentation

For more information about the Content1 API, refer to the official 1WorldSync documentation.

## 1WS US Extraction

Output of the `extract_us_records.py` compressed.

``` shell
tar cJf us_records.xz us_records
tar czf us_records.tgz us_records
```

``` shell
➜  examples git:(dev) ✗ ls -alh
total 1.1G
drwxr-xr-x  3 mcgarrah mcgarrah 4.0K May 24 17:36 .
drwxr-xr-x 14 mcgarrah mcgarrah 4.0K May 24 14:33 ..
-rw-r--r--  1 mcgarrah mcgarrah  816 May 22 17:22 README.md
-rw-r--r--  1 mcgarrah mcgarrah 6.9K May 24 14:37 content1_advanced_example.py
-rw-r--r--  1 mcgarrah mcgarrah 5.2K May 24 12:37 content1_example.py
-rw-r--r--  1 mcgarrah mcgarrah 4.2K May 24 14:27 extract_us_records.py
drwxr-xr-x  2 mcgarrah mcgarrah 128K May 24 15:20 us_records
-rw-r--r--  1 mcgarrah mcgarrah 693M May 24 16:27 us_records.tgz
-rw-r--r--  1 mcgarrah mcgarrah 346M May 24 16:25 us_records.xz
➜  examples git:(dev) ✗ du -msh us_records
11G     us_records
```
