import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).resolve().parents[2])
sys.path.insert(0, project_root)

# Import required libraries
import json
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handler(event, context):
    """
    Netlify function handler for finding government schemes
    """
    # Log function entry
    logger.info("Netlify Function Invoked")
    logger.info(f"Event Details: {json.dumps(event, indent=2)}")

    # Validate API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("GEMINI_API_KEY is not set")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'API Configuration Error',
                'message': 'Gemini API key is missing'
            })
        }

    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Parse input data
        user_data = json.loads(event.get('body', '{}'))
        
        # Use Gemini to generate scheme recommendations
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate prompt (simplified version)
        prompt = f"""
        Find the most suitable government schemes for an individual with the following profile:

        - Age: {user_data.get('age', 'Not specified')}
        - Gender: {user_data.get('gender', 'Not specified')}
        - Social Category: {user_data.get('socialCategory', 'Not specified')}
        - State: {user_data.get('state', 'Not specified')}
        
        Please provide a JSON list of 3 government schemes that match this profile.
        """
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': response.text
        }
    
    except Exception as e:
        logger.error(f"Error in function: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }

# Netlify requires a specific function signature
def lambda_handler(event, context):
    return handler(event, context)