import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# In-memory storage for tracking daily queries
daily_query_counts = {}

def check_daily_query_limit(ip_address):
    """
    Check and update daily query limit for an IP address
    Returns:
    - True if query is allowed
    - False if limit exceeded
    """
    from datetime import datetime
    
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{ip_address}:{today}"
    
    # Initialize or increment query count
    if key not in daily_query_counts:
        daily_query_counts[key] = 1
    else:
        daily_query_counts[key] += 1
    
    # Allow only 4 queries per day
    return daily_query_counts[key] <= 4

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

def generate_scheme_prompt(user_data):
    """Generate a comprehensive prompt for Gemini to find relevant government schemes."""
    language = user_data.get('language', 'en')
    
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
        
        Please provide a JSON list of government schemes that match this profile. Each scheme should include:
        - name: Scheme name
        - description: Brief description of the scheme
        - eligibility: Specific eligibility criteria
        - applicationProcess: How to apply for the scheme
        
        Return ONLY a valid JSON array. Do not include any additional text or explanation.
        """
    
    return prompt

def handler(event, context):
    """
    Netlify serverless function handler for finding government schemes
    """
    # Parse the incoming request body
    try:
        user_data = json.loads(event['body'])
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid request body',
                'message': 'Could not parse the request data'
            })
        }
    
    # Get client IP (use Netlify's header for IP)
    client_ip = event.get('headers', {}).get('x-forwarded-for', '127.0.0.1').split(',')[0].strip()
    
    # Check daily query limit
    if not check_daily_query_limit(client_ip):
        return {
            'statusCode': 429,
            'body': json.dumps({
                'error': 'Daily query limit exceeded',
                'message': 'You have reached the maximum of 4 queries per day. Please try again tomorrow.',
                'limit_reached': True
            })
        }
    
    try:
        # Use Gemini to generate scheme recommendations
        model = genai.GenerativeModel('gemini-pro')
        prompt = generate_scheme_prompt(user_data)
        
        try:
            response = model.generate_content(prompt)
            
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
                
                return {
                    'statusCode': 200,
                    'body': json.dumps(schemes)
                }
            
            except (json.JSONDecodeError, ValueError):
                # Fallback to predefined schemes
                return {
                    'statusCode': 200,
                    'body': json.dumps(FALLBACK_SCHEMES)
                }
        
        except Exception as gemini_error:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Gemini API error',
                    'details': str(gemini_error),
                    'fallback_schemes': FALLBACK_SCHEMES
                })
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Could not fetch schemes',
                'details': str(e),
                'fallback_schemes': FALLBACK_SCHEMES
            })
        }
