# Import necessary libraries
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

@dataclass
class PriceRange:
    """ Price range model """
    min: Optional[float]
    max: Optional[float]
    currency: str = 'EUR'
    confidence: float = 0.0

@dataclass
class ParserResult:
    """ Represents the structured, extracted, and classified data derived from user input. """
    product_type: List[str]
    features: List[str]
    price_range: Optional[PriceRange]
    location: Optional[str]
    styles: List[str]
    classification_summary: Optional[Dict[str, Any]]
    extras: Optional[List[str]]
    confidence_score: float
    original_query: Optional[str]
    suggested_query: Optional[str]

@dataclass
class SuggestionResult:
    """ Represents the structure of suggestion derived from user input. """
    brand_name: Optional[List[str]]
    product_name: Optional[List[str]]
    styles: Optional[List[str]]