from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import google.generativeai as genai
import os
import logging
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
import functools

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            static_folder=BASE_DIR,  
            static_url_path='')
CORS(app)

# In-memory storage for tracking daily queries
daily_query_counts = {}

# Configure rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="memory://"
)

# Configuration for Gemini API Key
# IMPORTANT: Replace this with your actual Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
try:
    if not GEMINI_API_KEY:
        logger.error("Gemini API key is not set. Please set it in environment variables.")
        raise ValueError("Gemini API key must be set")
    
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")

# Predefined list of government schemes as a fallback
FALLBACK_SCHEMES = [
    {
        "name": "Pradhan Mantri Jan Dhan Yojana",
        "description": "Financial inclusion scheme providing bank accounts, credit, insurance, and pension",
        "eligibility": "All Indian citizens",
        "applicationProcess": "Visit nearest bank branch with Aadhaar/ID proof"
    },
    {
        "name": "Pradhan Mantri Mudra Yojana",
        "description": "Loan scheme for non-corporate small business sectors",
        "eligibility": "Individuals with business plans, small entrepreneurs",
        "applicationProcess": "Apply through bank or online portal"
    },
    {
        "name": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana",
        "description": "Health insurance scheme providing coverage up to ₹5 lakhs per family",
        "eligibility": "Economically weaker sections, based on SECC database",
        "applicationProcess": "Register through empaneled hospitals or online portal"
    }
]

def check_daily_query_limit(ip_address):
    """
    Check and update daily query limit for an IP address
    Returns:
    - True if query is allowed
    - False if limit exceeded
    """
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{ip_address}:{today}"
    
    # Initialize or increment query count
    if key not in daily_query_counts:
        daily_query_counts[key] = 1
    else:
        daily_query_counts[key] += 1
    
    # Allow only 4 queries per day
    return daily_query_counts[key] <= 4

def daily_limit(f):
    """
    Decorator to apply daily query limit
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr or request.headers.get('X-Forwarded-For', '127.0.0.1')
        
        # Check daily query limit
        if not check_daily_query_limit(client_ip):
            return jsonify({
                'error': 'Daily query limit exceeded',
                'message': 'You have reached the maximum of 4 queries per day. Please try again tomorrow.',
                'limit_reached': True
            }), 429
        
        return f(*args, **kwargs)
    return decorated_function

def generate_scheme_prompt(user_data):
    """Generate a comprehensive prompt for Gemini to find relevant government schemes."""
    language = user_data.get('language', 'en')
    
    # Log the incoming user data for debugging
    logger.info(f"Generating prompt for language: {language}")
    logger.info(f"User Data: {json.dumps(user_data, indent=2)}")
    
    if language == 'hi':
        prompt = f"""
        निम्न प्रोफ़ाइल के लिए सबसे उपयुक्त सरकारी योजनाएँ खोजें:
        
        व्यक्तिगत विवरण:
        - आयु: {user_data.get('age', 'निर्दिष्ट नहीं')}
        - लिंग: {user_data.get('gender', 'निर्दिष्ट नहीं')}
        - सामाजिक श्रेणी: {user_data.get('socialCategory', 'निर्दिष्ट नहीं')}
        
        आर्थिक विवरण:
        - रोजगार की स्थिति: {user_data.get('employmentStatus', 'निर्दिष्ट नहीं')}
        - बीपीएल कार्ड की स्थिति: {user_data.get('bplCardStatus', 'निर्दिष्ट नहीं')}
        
        अतिरिक्त जानकारी:
        - विकलांगता की स्थिति: {user_data.get('disabilityStatus', 'निर्दिष्ट नहीं')}
        - शिक्षा का स्तर: {user_data.get('educationLevel', 'निर्दिष्ट नहीं')}
        
        स्थान:
        - राज्य: {user_data.get('state', 'निर्दिष्ट नहीं')}
        - जिला: {user_data.get('district', 'निर्दिष्ट नहीं')}
        
        व्यवसाय और उद्यमिता विवरण:
        - व्यवसाय की स्थिति: {user_data.get('businessStatus', 'निर्दिष्ट नहीं')}
        - व्यवसाय का प्रकार: {user_data.get('businessType', 'निर्दिष्ट नहीं')}
        - निवेश श्रेणी: {user_data.get('investmentRange', 'निर्दिष्ट नहीं')}
        - व्यवसाय क्षेत्र: {user_data.get('businessSector', 'निर्दिष्ट नहीं')}
        - पिछला अनुभव: {user_data.get('previousExperience', 'निर्दिष्ट नहीं')}
        - आवश्यक समर्थन प्रकार: {', '.join(user_data.get('supportType', [])) or 'कोई नहीं'}
        
        कृपया इस प्रोफ़ाइल के अनुरूप सरकारी योजनाओं की एक JSON सूची प्रदान करें। प्रत्येक योजना में शामिल होना चाहिए:
        - name: योजना का नाम
        - description: योजना का संक्षिप्त विवरण
        - eligibility: विशिष्ट पात्रता मानदंड
        - applicationProcess: योजना के लिए आवेदन कैसे करें
        
        केवल एक वैध JSON सरणी लौटाएं। कोई अतिरिक्त पाठ या व्याख्या शामिल न करें।
        """
    else:  # Default to English
        prompt = f"""
        Find the most suitable government schemes for an individual with the following profile:
        
        Personal Details:
        - Age: {user_data.get('age', 'Not specified')}
        - Gender: {user_data.get('gender', 'Not specified')}
        - Social Category: {user_data.get('socialCategory', 'Not specified')}
        
        Economic Details:
        - Employment Status: {user_data.get('employmentStatus', 'Not specified')}
        - BPL Card Status: {user_data.get('bplCardStatus', 'Not specified')}
        
        Additional Information:
        - Disability Status: {user_data.get('disabilityStatus', 'Not specified')}
        - Education Level: {user_data.get('educationLevel', 'Not specified')}
        
        Location:
        - State: {user_data.get('state', 'Not specified')}
        - District: {user_data.get('district', 'Not specified')}
        
        Business & Entrepreneurship Details:
        - Business Status: {user_data.get('businessStatus', 'Not specified')}
        - Business Type: {user_data.get('businessType', 'Not specified')}
        - Investment Range: {user_data.get('investmentRange', 'Not specified')}
        - Business Sector: {user_data.get('businessSector', 'Not specified')}
        - Previous Experience: {user_data.get('previousExperience', 'Not specified')}
        - Support Types Required: {', '.join(user_data.get('supportType', [])) or 'None'}
        
        Please provide a JSON list of government schemes that match this profile. Each scheme should include:
        - name: Scheme name
        - description: Brief description of the scheme
        - eligibility: Specific eligibility criteria
        - applicationProcess: How to apply for the scheme
        
        Return ONLY a valid JSON array. Do not include any additional text or explanation.
        """
    
    return prompt

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory(BASE_DIR, filename)

@app.route('/find-schemes', methods=['POST'])
@daily_limit
def find_schemes():
    """
    Endpoint to find government schemes based on user profile
    """
    try:
        # Parse the incoming request body
        user_data = request.json
        logger.info(f"Received user data: {json.dumps(user_data, indent=2)}")
    except Exception as e:
        logger.error(f"Failed to parse request body: {e}")
        return jsonify({
            'error': 'Invalid request data',
            'message': 'Could not parse the request data',
            'details': str(e)
        }), 400
    
    try:
        # Use Gemini to generate scheme recommendations
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = generate_scheme_prompt(user_data)
        
        try:
            logger.info(f"Sending prompt to Gemini: {prompt}")
            response = model.generate_content(prompt)
            logger.info(f"Received Gemini response: {response.text}")
            
            # Try to parse the JSON response
            try:
                # Extract JSON from markdown code block or direct text
                json_match = response.text.strip()
                if json_match.startswith('```json'):
                    json_match = json_match[7:-3].strip()
                elif json_match.startswith('```'):
                    json_match = json_match[3:-3].strip()
                
                schemes = json.loads(json_match)
                
                # Validate schemes structure
                if not isinstance(schemes, list):
                    raise ValueError("Response is not a list of schemes")
                
                logger.info(f"Successfully retrieved {len(schemes)} schemes from Gemini")
                return jsonify(schemes)
            
            except (json.JSONDecodeError, ValueError) as parse_error:
                logger.warning(f"Failed to parse Gemini response: {parse_error}")
                logger.warning(f"Raw Gemini response: {response.text}")
                
                # Fallback to predefined schemes
                return jsonify(FALLBACK_SCHEMES)
        
        except Exception as gemini_error:
            logger.error(f"Gemini API error: {gemini_error}")
            return jsonify({
                'error': 'Gemini API error',
                'details': str(gemini_error),
                'fallback_schemes': FALLBACK_SCHEMES
            }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in find-schemes: {e}")
        return jsonify({
            'error': 'Could not fetch schemes',
            'details': str(e),
            'fallback_schemes': FALLBACK_SCHEMES
        }), 500

if __name__ == '__main__':
    # Ensure environment variables are set
    if not os.getenv('GEMINI_API_KEY'):
        logger.warning("GEMINI_API_KEY is not set. Please set it in .env file.")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
