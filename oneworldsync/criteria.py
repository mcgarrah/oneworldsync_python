"""
Criteria builders for the 1WorldSync Content1 API

This module provides classes to build search criteria for the 1WorldSync Content1 API.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union


class DateRangeCriteria:
    """Builder for date range criteria"""
    
    @staticmethod
    def between(from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Create a date range criteria between two dates
        
        Args:
            from_date (str): Start date in YYYY-MM-DD format
            to_date (str): End date in YYYY-MM-DD format
            
        Returns:
            dict: Date range criteria
        """
        return {
            "from": {
                "date": from_date,
                "op": "GTE"
            },
            "to": {
                "date": to_date,
                "op": "LTE"
            }
        }
    
    @staticmethod
    def last_days(days: int) -> Dict[str, Any]:
        """
        Create a date range criteria for the last N days
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            dict: Date range criteria
        """
        today = datetime.now().date()
        from_date = (today - timedelta(days=days)).isoformat()
        to_date = today.isoformat()
        
        return DateRangeCriteria.between(from_date, to_date)
    
    @staticmethod
    def last_30_days() -> Dict[str, Any]:
        """
        Create a date range criteria for the last 30 days
        
        Returns:
            dict: Date range criteria
        """
        return DateRangeCriteria.last_days(30)


class SortField:
    """Builder for sort field criteria"""
    
    @staticmethod
    def create(field: str, descending: bool = False) -> Dict[str, str]:
        """
        Create a sort field criteria
        
        Args:
            field (str): Field name to sort by
            descending (bool, optional): Sort in descending order. Defaults to False.
            
        Returns:
            dict: Sort field criteria
        """
        return {
            "field": field,
            "desc": str(descending).lower()
        }


class ProductCriteria:
    """Builder for product search criteria"""
    
    def __init__(self):
        """Initialize an empty product criteria"""
        self._criteria = {}
    
    def with_gtin(self, gtins: List[str]) -> 'ProductCriteria':
        """
        Add GTIN criteria
        
        Args:
            gtins (List[str]): List of GTINs to search for
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['gtin'] = gtins
        return self
    
    def with_ip_gln(self, ip_gln: str) -> 'ProductCriteria':
        """
        Add Information Provider GLN criteria
        
        Args:
            ip_gln (str): Information Provider GLN
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['ipGln'] = ip_gln
        return self
    
    def with_target_market(self, target_market: str) -> 'ProductCriteria':
        """
        Add target market criteria
        
        Args:
            target_market (str): Target market code (e.g., 'US')
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['targetMarket'] = target_market
        return self
    
    def with_last_modified_date(self, date_range: Dict[str, Any]) -> 'ProductCriteria':
        """
        Add last modified date criteria
        
        Args:
            date_range (Dict): Date range criteria created with DateRangeCriteria
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['lastModifiedDate'] = date_range
        return self
    
    def with_brand_name(self, brand_name: str) -> 'ProductCriteria':
        """
        Add brand name criteria
        
        Args:
            brand_name (str): Brand name to search for
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['brandName'] = brand_name
        return self
    
    def with_product_type(self, product_type: str) -> 'ProductCriteria':
        """
        Add product type criteria
        
        Args:
            product_type (str): Product type (e.g., 'EA')
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['productType'] = product_type
        return self
    
    def with_consumer_unit(self, is_consumer_unit: bool) -> 'ProductCriteria':
        """
        Add consumer unit criteria
        
        Args:
            is_consumer_unit (bool): Whether the product is a consumer unit
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['isConsumerUnit'] = str(is_consumer_unit).lower()
        return self
    
    def with_gpc_code(self, gpc_code: str) -> 'ProductCriteria':
        """
        Add GPC code criteria
        
        Args:
            gpc_code (str): GPC code to search for
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['gpcCode'] = gpc_code
        return self
    
    def with_upc_code(self, upc_code: str) -> 'ProductCriteria':
        """
        Add UPC code criteria
        
        Args:
            upc_code (str): UPC code to search for
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['upcCode'] = upc_code
        return self
    
    def with_sort(self, sort_fields: List[Dict[str, str]]) -> 'ProductCriteria':
        """
        Add sort criteria
        
        Args:
            sort_fields (List[Dict]): List of sort fields created with SortField
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['sortFields'] = sort_fields
        return self
    
    def with_fields(self, include: List[str] = None, exclude: List[str] = None) -> 'ProductCriteria':
        """
        Add field inclusion/exclusion criteria
        
        Args:
            include (List[str], optional): Fields to include. Defaults to None.
            exclude (List[str], optional): Fields to exclude. Defaults to None.
            
        Returns:
            ProductCriteria: Self for chaining
        """
        fields = {}
        if include:
            fields['include'] = include
        if exclude:
            fields['exclude'] = exclude
        
        if fields:
            self._criteria['fields'] = fields
        
        return self
    
    def with_search_after(self, search_after: List[Any]) -> 'ProductCriteria':
        """
        Add search after criteria for pagination
        
        Args:
            search_after (List): Search after token from previous response
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['searchAfter'] = search_after
        return self
    
    def with_hierarchy(self, pull_hierarchy: bool = True) -> 'ProductCriteria':
        """
        Add hierarchy criteria
        
        Args:
            pull_hierarchy (bool, optional): Whether to pull hierarchy. Defaults to True.
            
        Returns:
            ProductCriteria: Self for chaining
        """
        self._criteria['pullHierarchy'] = pull_hierarchy
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Build the criteria dictionary
        
        Returns:
            dict: Complete criteria dictionary
        """
        return self._criteria