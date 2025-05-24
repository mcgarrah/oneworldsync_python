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
@click.option('--gtin', help='GTIN to fetch')
@click.option('--target-market', default='US', help='Target market (default: US)')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def fetch(gtin, target_market, output):
    """Fetch product data by GTIN"""
    try:
        client = get_client()
        criteria = {"targetMarket": target_market}
        
        if gtin:
            criteria["gtin"] = gtin
            
        result = client.fetch_products(criteria)
        
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(result, indent=2))
            
    except (AuthenticationError, APIError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--target-market', default='US', help='Target market (default: US)')
@click.option('--limit', default=5, help='Number of results to return (default: 5)')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def count(target_market, limit, output):
    """Count products"""
    try:
        client = get_client()
        criteria = {"targetMarket": target_market}
        
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
@click.option('--gtin', help='GTIN to fetch hierarchy for')
@click.option('--target-market', default='US', help='Target market (default: US)')
@click.option('--output', '-o', help='Output file path (default: stdout)')
def hierarchy(gtin, target_market, output):
    """Fetch product hierarchy"""
    try:
        client = get_client()
        criteria = {"targetMarket": target_market}
        
        if gtin:
            criteria["gtin"] = gtin
            
        result = client.fetch_hierarchies(criteria)
        
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(json.dumps(result, indent=2))
            
    except (AuthenticationError, APIError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()