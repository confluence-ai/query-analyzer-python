""" Suggest/Extract top data for Product Name, Brand Name and Styles """

# Import necessary libraries
import logging

# Import custom modules
from config.config import SuggestionResult
from query_suggestion.style_extractor import StyleExtractor
from query_suggestion.product_brand_extractor import ProductBrandExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class QuerySuggestion:
    """ Recommends top 10 matches for product names, brand names, and styles based on the input query. """
    
    def __init__(self):
        """
            Initialize the query suggestion
        """
        # Load Extraction models
        self.style_extractor = StyleExtractor()
        self.product_extractor = ProductBrandExtractor()
    
    def suggestsQuery(self, query: str) -> SuggestionResult:
        """
            Extracts top 5 matches from the query for different data
            
            Args:
                query (str): Input text to parse

            Returns:
                SuggestionResult: Suggestion result with top 5 product name, brand name and styles
        """
        logger.info(f"Suggestion for {query}")

        # STEP 1: Extract product names
        data = self.product_extractor.extractProductBrandName(query)

        product_name = data['product_name']
        brand_name = data['brand_name']
        
        # STEP 3: Extract styles
        styles = self.style_extractor.extractStyles(query)

        result = SuggestionResult(
            # brand_name=brand_name or [],
            brand_name=brand_name or [],
            product_name=product_name or [],
            styles=styles,
        )
        
        return result
    
    def suggestQueryResults(self, query: str) -> SuggestionResult:
        """
            Returns suggestion as dictionary

            Args:
                query (str): Input text to parse

            Returns:
                SuggestionResult: Suggestion result with top 5 product name, brand name and styles
        """
        result = self.suggestsQuery(query)
        
        if result:
            return {
                "product_name": result.product_name, 
                "brand_name": result.brand_name,
                "styles": result.styles,
            }
        
        return False