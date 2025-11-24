""" Main entry point for the Furniture Parser API using Flask. """

# Import necessary libraries
import time
import logging
import datetime
import warnings
from flask_cors import CORS
from flask import Flask, request, jsonify

# Import custom modules
from query_parser.furniture_parser import FurnitureParser
from query_suggestion.suggestion import QuerySuggestion

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load parser ONCE at startup (heavy models initialized here)
logger.info("Loading FurnitureParser, QuerySuggestion and ML models...")
parser = FurnitureParser()
suggest = QuerySuggestion()
logger.info("Models loaded successfully.")

@app.route('/query/analyze', methods=['POST'])
def analyzeQuery():
    """ Main processing endpoint for query analyzer """
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({"success": False, "error": "Query is required"}), 400
        
        # Measure processing time
        start = time.time()

        # Analyze the query
        result = parser.analyzeQueryText(query)

        end = time.time()

        # Calculate duration and format it
        duration = end - start

        if duration < 1:
            result["processing_time"] = f"{duration:.2f} ms"
        else:
            result["processing_time"] = f"{duration:.2f} sec"

        logger.info(f"Processed query in {result['processing_time']}: {query}")
        if not result:
            return jsonify({"success": False, "error": "Invalid input type"}), 400

        return jsonify({"success": True, "result": result})

    except Exception as e:
        logger.exception("Error in analyzeQuery")
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500
    
@app.route('/query/suggestion', methods=['POST'])
def querySuggestion():
    """ Main processing endpoint for query suggestion 
        Returns top 5 matches for product names, brand names, and styles based on the input query.
        The search is prefix-matching and case-insensitive.
    """
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({"success": False, "error": "Query is required"}), 400
        
        results = suggest.suggestQueryResults(query)
        
        if results:
            return results
        
        return jsonify({"success": False, "error": "Issue while fetching data."}), 400
    
    except Exception as e:
        logger.exception("Error in querySuggestion")
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

# Health Check Endpoints
@app.route("/health", methods=["GET"])
async def healthCheck():
    """ Basic health check """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "query-parser-api"
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8432)
