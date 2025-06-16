#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line interface for 1WorldSync Content1 API.
"""

import os
import sys
import json
import click
from pathlib import Path
from dotenv import load_dotenv
from .content1_client import Content1Client
from .exceptions import AuthenticationError, APIError
from .criteria import ProductCriteria, DateRangeCriteria, SortField

def load_credentials():
    """Load credentials from ~/.ows/credentials file"""
    credentials_path = Path.home() / '.ows' / 'credentials'
    if not credentials_path.exists():
        return None
    
    load_dotenv(credentials_path)
    
    required_vars = [
        "ONEWORLDSYNC_APP_ID",
        "ONEWORLDSYNC_SECRET_KEY"
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        return None
        
    return {
        'app_id': os.getenv("ONEWORLDSYNC_APP_ID"),
        'secret_key': os.getenv("ONEWORLDSYNC_SECRET_KEY"),
        'gln': os.getenv("ONEWORLDSYNC_USER_GLN"),
        'api_url': os.getenv("ONEWORLDSYNC_CONTENT1_API_URL", "https://content1-api.1worldsync.com")
    }

def get_client():
    """Get Content1Client instance with credentials"""
    credentials = load_credentials()
    if not credentials:
        click.echo("Error: Credentials not found in ~/.ows/credentials", err=True)
        click.echo("Please create the file with the following format:", err=True)
        click.echo("""
ONEWORLDSYNC_APP_ID=your_app_id
ONEWORLDSYNC_SECRET_KEY=your_secret_key
ONEWORLDSYNC_USER_GLN=your_gln  # Optional
ONEWORLDSYNC_CONTENT1_API_URL=https://content1-api.1worldsync.com  # Optional
""", err=True)
        sys.exit(1)
    
    return Content1Client(**credentials)

from . import __version__

@click.group()
@click.version_option(version=__version__)
def cli():
    """1WorldSync Content1 API Command Line Tool"""
    pass

@cli.command()
def login():
    """Verify login credentials"""
    try:
        client = get_client()
        # Test connection with a simple fetch request
        client.fetch_products({})
        click.echo("✓ Login successful")
    except AuthenticationError as e:
        click.echo(f"✗ Authentication failed: {e}", err=True)
        sys.exit(1)
    except APIError as e:
        click.echo(f"✗ API error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Unexpected error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--gtin', help='GTIN to fetch (14-digit format, pad shorter GTINs with leading zeros)')
@click.option('--target-market', help='Target market')
@click.option('--fields', help='Comma-separated list of fields to include (e.g., "gtin,gtinName")')
@click.option('--last-days', type=int, help='Fetch products modified in the last N days')
@click.option('--brand', help='Brand name to filter by')
@click.option('--gpc-code', help='GPC code to filter by')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def fetch(gtin, target_market, fields, last_days, brand, gpc_code, output):
    """Fetch product data with various filters"""
    try:
        client = get_client()
        criteria = ProductCriteria()
        
        if target_market:
            criteria.with_target_market(target_market)
        
        if gtin:
            # Ensure GTIN is 14 digits by padding with leading zeros if needed
            padded_gtin = gtin.zfill(14)
            criteria.with_gtin([padded_gtin])  # API expects an array of GTINs
            
        if fields:
            field_list = [f.strip() for f in fields.split(',')]
            criteria.with_fields(include=field_list)
        
        if last_days:
            criteria.with_last_modified_date(DateRangeCriteria.last_days(last_days))
            
        if brand:
            criteria.with_brand_name(brand)
            
        if gpc_code:
            criteria.with_gpc_code(gpc_code)
            
        result = client.fetch_products(criteria)
        
        # Convert to dictionary for JSON serialization
        result_dict = result.to_dict()
        
        if output:
            with open(output, 'w') as f:
                json.dump(result_dict, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(result_dict, indent=2))
            
    except (AuthenticationError, APIError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--target-market', help='Target market')
@click.option('--last-days', type=int, help='Count products modified in the last N days')
@click.option('--brand', help='Brand name to filter by')
@click.option('--gpc-code', help='GPC code to filter by')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def count(target_market, last_days, brand, gpc_code, output):
    """Count products with various filters"""
    try:
        client = get_client()
        criteria = ProductCriteria()
        
        if target_market:
            criteria.with_target_market(target_market)
            click.echo(f"Counting products for target market: {target_market}")
        else:
            click.echo("Counting all products (no target market specified)")
            
        if last_days:
            criteria.with_last_modified_date(DateRangeCriteria.last_days(last_days))
            click.echo(f"Filtering by last {last_days} days")
            
        if brand:
            criteria.with_brand_name(brand)
            click.echo(f"Filtering by brand: {brand}")
            
        if gpc_code:
            criteria.with_gpc_code(gpc_code)
            click.echo(f"Filtering by GPC code: {gpc_code}")
        
        result = client.count_products(criteria)
        
        response = {"count": result}
        
        if output:
            with open(output, 'w') as f:
                json.dump(response, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(f"Product count: {result}")
            
    except (AuthenticationError, APIError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--gtin', help='GTIN to fetch hierarchy for (14-digit format, pad shorter GTINs with leading zeros)')
@click.option('--target-market', help='Target market')
@click.option('--last-days', type=int, help='Fetch hierarchies modified in the last N days')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def hierarchy(gtin, target_market, last_days, output):
    """Fetch product hierarchy"""
    try:
        client = get_client()
        criteria = ProductCriteria()
        
        if target_market:
            criteria.with_target_market(target_market)
        
        if gtin:
            # Ensure GTIN is 14 digits by padding with leading zeros if needed
            padded_gtin = gtin.zfill(14)
            criteria.with_gtin([padded_gtin])  # API expects an array of GTINs
            
        if last_days:
            criteria.with_last_modified_date(DateRangeCriteria.last_days(last_days))
            
        result = client.fetch_hierarchies(criteria)
        
        # Convert to dictionary for JSON serialization
        result_dict = result.to_dict()
        
        if output:
            with open(output, 'w') as f:
                json.dump(result_dict, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(result_dict, indent=2))
            
    except (AuthenticationError, APIError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
@cli.command()
@click.option('--target-market', help='Target market')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def recent(target_market, output):
    """Fetch products modified in the last 30 days"""
    try:
        client = get_client()
        
        click.echo(f"Fetching products modified in the last 30 days...")
        if target_market:
            click.echo(f"Filtering by target market: {target_market}")
            
        result = client.fetch_products_last_30_days(target_market=target_market)
        
        # Convert to dictionary for JSON serialization
        result_dict = result.to_dict()
        
        if output:
            with open(output, 'w') as f:
                json.dump(result_dict, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(f"Found {len(result)} products")
            for i, product in enumerate(result):
                if i >= 5:  # Only show first 5 products
                    click.echo("...")
                    break
                click.echo(f"{i+1}. {product.brand_name} - {product.gtin} - {product.last_modified_date}")
            
    except (AuthenticationError, APIError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)