""" Style Extractor for furniture queries """

# Import necessary libraries
import re
from typing import List, Optional

# Import constants and mappings
from config.constants import FURNITURE_STYLES

class StyleExtractor:
    """ Extract furniture styles from text using fuzzy matching and spell correction """
    
    def __init__(self):
        """ Initialize the style extractor """

        # Build mappings for efficient lookup
        self.all_style_terms = set()
        self._buildStyleMappings()
    
    def _buildStyleMappings(self):
        """ Build reverse mapping from synonyms to main styles """
        for main_style, synonyms in FURNITURE_STYLES.items():
            # Map the main style name to itself (case-insensitive)
            self.all_style_terms.add(main_style.lower())
        
    def _extractFurnitureStyles(self, text: str) -> List[str]:
        """
            Extracts design styles from the input text.

            Args:
                text (str): The raw text string to scan for style keywords.

            Returns:
                List[str]: A list of unique, standardized style labels detected in the text.
        """
        text_lower = text.lower()
        
        # Check for multi-word phrases first (longer matches are more specific)
        style_matches = [
            style.title() for style in self.all_style_terms 
            if style.lower().startswith(text_lower)
        ][:10]
        
        return style_matches
    
    def extractStyles(self, text: str) -> List[str]:
        """
            Main method to extract styles from dictionary
            
            Args:
                text (str): Input text
                
            Returns:
                List[str]: List of detected style names
        """
        # Direct exact matching
        matches = self._extractFurnitureStyles(text)
        
        return matches