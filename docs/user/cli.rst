Command Line Interface
====================

The package includes a command-line interface (CLI) tool called ``ows`` that provides easy access to common Content1 API operations.

Installation
-----------

The CLI is automatically installed when you install the package::

    pip install oneworldsync

Configuration
------------

The CLI requires credentials to be stored in ``~/.ows/credentials`` file with the following format::

    ONEWORLDSYNC_APP_ID=your_app_id
    ONEWORLDSYNC_SECRET_KEY=your_secret_key
    ONEWORLDSYNC_USER_GLN=your_gln  # Optional
    ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com  # Optional

Global Options
-------------

--version
~~~~~~~~

Display the version of the package::

    ows --version

--help
~~~~~

Display help information for the CLI or a specific command::

    # General help
    ows --help

    # Command-specific help
    ows fetch --help

Commands
--------

login
~~~~~

Test if your credentials are valid::

    ows login

fetch
~~~~~

Fetch product data with optional filters::

    # Basic fetch
    ows fetch

    # Fetch by GTIN (14-digit format, shorter GTINs are automatically padded with leading zeros)
    ows fetch --gtin 12345678901234
    ows fetch --gtin 052000050585  # Will be padded to 00052000050585

    # Specify target market
    ows fetch --target-market US

    # Fetch specific fields only
    ows fetch --gtin 052000050585 --fields "gtin,gtinName,brandName"
    
    # Combine options
    ows fetch --gtin 052000050585 --target-market US --fields "gtin,gtinName,brandName"

    # Save results to file
    ows fetch --output results.json
    ows fetch -o results.json

count
~~~~~

Count products matching criteria::

    # Basic count
    ows count

    # Count with target market (US, DE, FR, etc.)
    ows count --target-market DE

    # Limit results
    ows count --limit 10

    # Save count to file
    ows count --output count.json
    ows count -o count.json

hierarchy
~~~~~~~~

Fetch product hierarchies::

    # Basic hierarchy fetch
    ows hierarchy

    # Fetch hierarchy for specific GTIN (14-digit format, shorter GTINs are automatically padded with leading zeros)
    ows hierarchy --gtin 12345678901234
    ows hierarchy --gtin 052000050585  # Will be padded to 00052000050585

    # Specify target market
    ows hierarchy --target-market US

    # Save hierarchy to file
    ows hierarchy --output hierarchy.json
    ows hierarchy -o hierarchy.json