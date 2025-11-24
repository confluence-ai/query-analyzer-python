""" Brand and Product Extractor for queries """

# Import necessary libraries
import logging
from typing import List, Dict

# Import custom module
from config.database import DatabaseManager

# Import constants and mappings
from config.constants import BRAND_TABLE, PRODUCT_TABLE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class ProductBrandExtractor:
    """ Extract brand and product names from furniture queries using fuzzy matching and spell correction """
    
    def __init__(self):
        """ Initialize the brand and product extractor """
        # Database manager
        self.db = DatabaseManager(use_connection_pool=True)
        
        # Load product and brand data from database
        self.product_names = []
        self.brand_names = []

    def _extractProductFromDB(self, text: str) -> List[str]:
        """
            Extract Product names from database

            Args:
                text (str): Input query text

            Returns:
                List[str]: Lists of product names
        """
        return self.db.fetchProductNames(text=text)
    
    def _extractBrandFromDB(self, text: str) -> List[str]:
        """
            Extract Brand names from database

            Args:
                text (str): Input query text

            Returns:
                List[str]: Lists of brand names
        """
        return self.db.fetchBrandNames(text=text)

    def extractProductBrandName(self, text: str) -> Dict:
        """
            Extract both brand and product from query text
            
            Args:
                text (str): Input query text
                
            Returns:
                Dict:
                    - brand_name: List with brand name
                    - product_name: List with product name
        """
        self.product_names = self._extractProductFromDB(text)
        self.brand_names = self._extractBrandFromDB(text)
        
        return {'product_name':self.product_names, 'brand_name':self.brand_names}