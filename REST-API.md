# 1WorldSync Content1 REST API

The following APIs are available:

**Product Search API** - Performs a search against the product data published in ContentNOW to find products that meet the supplied criteria. For each search result displayed, a basic set of information about the product is provided. While performing a product search only a subset from the entire list of attributes for an item will be returned.

**Product Fetch API** - Once a Product Search has been performed, the full set of attribute information on a given product can be retrieved using the Product Fetch API and the item reference id (obtained through the search).

You can access the [PreProd Swagger API interface](https://marketplace.preprod.api.1worldsync.com/api/V2/) to test things out.

Learning to perform queries has been challenging along the way.

- 1WorldSync Content1 REST API Product Search Parameters
  - searchType: 
    - `freeTextSearch`: When using the freeText search you would specify a word, phrase, or ID to search on.
    - `categoryCode`: If a categoryCode search is selected the category code should be provided.
    - `advancedSearch`: When advancedSearch is selected you can create a dynamic query using logical operators (and/or/not) along with a corresponding attribute to create a complex query.
    - 1ws searchable [query attributes](https://marketplace.preprod.api.1worldsync.com/api/V2/SearchAttributes.htm)
    - Examples:
      - freeTextSearch - query="Tuscan milk"
      - categoryCode - query="Fruits - Unprepared/Unprocessed(Frozen)"
      - advancedSearch - query=productName:"Healthy and tastySoybeanmilk"
      - To search for Beverages in a freeTextSearch:
        - query="Bever＊"
        - query="＊verag＊"
        - query="＊erages"
        - Note: For partial text search on a single word, append '＊' in the query parameter. You can not use a partial text search for a phrase.
        - query="Tuscan mi＊" - is not valid
  - filter: ???
  - sortOrder: `asc`, `desc`
  - sortColumn:
    - 1ws [sort attributes](https://marketplace.preprod.api.1worldsync.com/api/V2/SortAttributes.htm)
    - isTradeItemAConsumerUnit: True/ False - Indicates whether an item is a consumable unit or not.
    - lastChangeDateTime: System generated time when the last change was made
    - tradeItemUnitDescriptorCode: This field represents the type of the product that this item is.
    - publicationDateTime: System generated time when publication occurred
    - targetMarket: The Target Market indicates the country where the trade item is available for sale.

- 1WorldSync Content1 REST API Product Fetch Parameters
  - `attrset` [Attribute Context Lists](https://marketplace.preprod.api.1worldsync.com/api/V2/AttributeContextLists.htm)
  - Example: `attrset=allergens,ingredients,nutritionals`
