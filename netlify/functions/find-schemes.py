git add .
git commit -m "Add comprehensive support types dropdown for business scheme recommendations"
git pushimport json
import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY is not set in environment variables")
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")

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

# Predefined list of support types for Business & Entrepreneurship
SUPPORT_TYPES = [
    # Financial Support
    "Financial Assistance",
    "Loan Subsidy",
    "Grant Funding",
    "Venture Capital",
    
    # Training & Skill Development
    "Business Training",
    "Entrepreneurship Mentorship",
    "Skill Development Program",
    "Technical Training",
    
    # Infrastructure & Resources
    "Workspace Provision",
    "Equipment Support",
    "Technology Access",
    "Digital Infrastructure",
    
    # Marketing & Networking
    "Market Linkage",
    "Export Promotion",
    "Networking Opportunities",
    "Business Expo Support",
    
    # Regulatory & Compliance
    "Legal Consultation",
    "Compliance Guidance",
    "Patent & IPR Support",
    "Registration Assistance",
    
    # Social Impact
    "Women Entrepreneur Support",
    "Minority Business Support",
    "Rural Entrepreneurship",
    "Startup Ecosystem Support"
]

def generate_scheme_prompt(user_data):
    """Generate a comprehensive prompt for Gemini to find relevant government schemes."""
    language = user_data.get('language', 'en')
    
    # Log the incoming user data for debugging
    logger.info(f"Generating prompt for language: {language}")
    logger.info(f"User Data: {json.dumps(user_data, indent=2)}")
    
    # Check if any business details are present
    business_details = {
        'businessStatus': user_data.get('businessStatus'),
        'businessType': user_data.get('businessType'),
        'investmentRange': user_data.get('investmentRange'),
        'businessSector': user_data.get('businessSector'),
        'previousExperience': user_data.get('previousExperience'),
        'supportType': user_data.get('supportType', [])
    }
    
    # Remove None or empty values
    business_details = {k: v for k, v in business_details.items() if v}
    
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
        
        {f'''
        व्यवसाय और उद्यमिता विवरण:
        - व्यवसाय की स्थिति: {business_details.get('businessStatus', 'निर्दिष्ट नहीं')}
        - व्यवसाय का प्रकार: {business_details.get('businessType', 'निर्दिष्ट नहीं')}
        - निवेश श्रेणी: {business_details.get('investmentRange', 'निर्दिष्ट नहीं')}
        - व्यवसाय क्षेत्र: {business_details.get('businessSector', 'निर्दिष्ट नहीं')}
        - पिछला अनुभव: {business_details.get('previousExperience', 'निर्दिष्ट नहीं')}
        - आवश्यक समर्थन प्रकार: {', '.join(business_details.get('supportType', [])) or 'कोई नहीं'}
        ''' if business_details else ''}
        
        कृपया इस प्रोफ़ाइल के अनुरूप सरकारी योजनाओं की एक JSON सूची प्रदान करें। प्रत्येक योजना में शामिल होना चाहिए:
        - name: योजना का नाम
        - description: योजना का संक्षिप्त विवरण
        - eligibility: विशिष्ट पात्रता मानदंड
        - applicationProcess: योजना के लिए आवेदन कैसे करें
        - businessRelevance: व्यवसाय के लिए प्रासंगिकता का स्तर (उच्च/मध्यम/निम्न)
        
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
        
        {f'''
        Business & Entrepreneurship Details:
        - Business Status: {business_details.get('businessStatus', 'Not specified')}
        - Business Type: {business_details.get('businessType', 'Not specified')}
        - Investment Range: {business_details.get('investmentRange', 'Not specified')}
        - Business Sector: {business_details.get('businessSector', 'Not specified')}
        - Previous Experience: {business_details.get('previousExperience', 'Not specified')}
        - Support Types Required: {', '.join(business_details.get('supportType', [])) or 'None'}
        ''' if business_details else ''}
        
        Please provide a JSON list of government schemes that match this profile. Each scheme should include:
        - name: Scheme name
        - description: Brief description of the scheme
        - eligibility: Specific eligibility criteria
        - applicationProcess: How to apply for the scheme
        - businessRelevance: Level of relevance for the business (high/medium/low)
        
        Return ONLY a valid JSON array. Do not include any additional text or explanation.
        """
    
    return prompt

def handler(event, context):
    """
    Netlify serverless function handler for finding government schemes
    """
    # Add CORS headers to allow cross-origin requests
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }

    # Handle preflight OPTIONS request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'Successful preflight call.'})
        }

    # Parse the incoming request body
    try:
        user_data = json.loads(event.get('body', '{}'))
        logger.info(f"Received user data: {json.dumps(user_data, indent=2)}")
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Failed to parse request body: {e}")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({
                'error': 'Invalid request',
                'message': 'Could not parse the request data',
                'details': str(e)
            })
        }
    
    # Get client IP (use Netlify's header for IP)
    client_ip = event.get('headers', {}).get('x-forwarded-for', '127.0.0.1').split(',')[0].strip()
    
    # Check daily query limit
    if not check_daily_query_limit(client_ip):
        logger.warning(f"Daily query limit exceeded for IP: {client_ip}")
        return {
            'statusCode': 429,
            'headers': cors_headers,
            'body': json.dumps({
                'error': 'Rate limit exceeded',
                'message': 'You have reached the maximum of 4 queries per day. Please try again tomorrow.',
                'limit_reached': True
            })
        }
    
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
                return {
                    'statusCode': 200,
                    'headers': cors_headers,
                    'body': json.dumps(schemes)
                }
            
            except (json.JSONDecodeError, ValueError) as parse_error:
                logger.warning(f"Failed to parse Gemini response: {parse_error}")
                logger.warning(f"Raw Gemini response: {response.text}")
                
                # Fallback to predefined schemes
                return {
                    'statusCode': 200,
                    'headers': cors_headers,
                    'body': json.dumps(FALLBACK_SCHEMES)
                }
        
        except Exception as gemini_error:
            logger.error(f"Gemini API error: {gemini_error}")
            return {
                'statusCode': 500,
                'headers': cors_headers,
                'body': json.dumps({
                    'error': 'Gemini API error',
                    'details': str(gemini_error),
                    'fallback_schemes': FALLBACK_SCHEMES
                })
            }
    
    except Exception as e:
        logger.error(f"Unexpected error in find-schemes: {e}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({
                'error': 'Could not fetch schemes',
                'details': str(e),
                'fallback_schemes': FALLBACK_SCHEMES
            })
        }
