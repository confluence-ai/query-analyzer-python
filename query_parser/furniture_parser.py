"""Furniture Parser using ML/NLP models and hybrid techniques"""

# Import necessary libraries
import re
import logging

# Import custom modules
from config.config import ParserResult
from query_parser.product_type_extractor import ProductTypeExtractor
from query_parser.feature_extractor import FeatureExtractor
from query_parser.price_extractor import PriceExtractor
from query_parser.classification_extractor import StyleClassification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class FurnitureParser:
    """ Furniture parser with ML/NLP models """
    
    def __init__(self):
        """
            Initialize the furniture parser
        """
        # Load Extraction models
        self.product_type_extractor = ProductTypeExtractor()
        self.price_extractor = PriceExtractor()
        self.classification_extractor = StyleClassification()
        self.feature_extractor = FeatureExtractor()
    
    def structureQuery(self, query: str) -> ParserResult:
        """
            Enhanced parsing with ML models
            
            Args:
                query (str): Input text to parse

            Returns:
                ParserResult: Parsed result with product type, features, price range, location, and confidence    
        """
        logger.info(f"ML parsing query: {query}")
                

        # STEP 1: Extract features, type, classification from ORIGINAL query
        product_types, product_confidence, corrected_query = self.product_type_extractor.classifyProductType(query)
        features, corrected_query = self.feature_extractor.extractFeatures(corrected_query)
        classifications = self.classification_extractor.extractClassification(query)
        
        # STEP 2: Extract price from query
        price_range = self.price_extractor.extractPriceRange(query)
        
        result = ParserResult(
            product_type=product_types if product_types != ["Unknown"] else [],
            features=features,
            price_range=price_range,
            location="",
            confidence_score=product_confidence[0] if product_confidence else 0.0,
            classification_summary=classifications,
            extras=[],
            original_query=query,
            suggested_query=corrected_query if corrected_query != query else None
        )
        
        return result
    
    def analyzeQueryText(self, query: str) -> ParserResult:
        """
            Parse query and return as dictionary

            Args:
                query (str): Input text to parse

            Returns:
                ParserResult: Parsed result with product type, features, price range, location, and confidence
        """
        result = self.structureQuery(query)
        
        return {
            "product_type": result.product_type, 
            "features": result.features,
            "price_range": result.price_range,
            "location": result.location,
            "classification_summary": result.classification_summary,
            "extras": result.extras,
            "confidence_score": result.confidence_score,
            "original_query": result.original_query,
            "suggested_query": result.suggested_query  # Include in output
        }