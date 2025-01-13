import requests
import json

def test_find_schemes(profile):
    """
    Test the find-schemes endpoint with different user profiles
    """
    url = 'http://localhost:5000/find-schemes'
    
    try:
        response = requests.post(url, json=profile)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        schemes = response.json()
        
        print(f"\nTest Profile: {json.dumps(profile, indent=2)}")
        print(f"Number of Schemes Found: {len(schemes)}")
        
        for scheme in schemes:
            print("\nScheme Details:")
            print(f"Name: {scheme.get('name', 'N/A')}")
            print(f"Description: {scheme.get('description', 'N/A')}")
            print(f"Eligibility: {scheme.get('eligibility', 'N/A')}")
            print(f"Application Process: {scheme.get('applicationProcess', 'N/A')}")
        
        return schemes
    
    except requests.exceptions.RequestException as e:
        print(f"Error testing profile: {e}")
        return None

def main():
    # Test profiles with different scenarios
    test_profiles = [
        # Young professional
        {
            "age": "25",
            "gender": "Female",
            "socialCategory": "General",
            "employmentStatus": "Employed",
            "bplCardStatus": "No",
            "disabilityStatus": "No",
            "educationLevel": "Graduate",
            "state": "Maharashtra",
            "district": "Pune",
            "language": "en"
        },
        # Low-income individual
        {
            "age": "40",
            "gender": "Male",
            "socialCategory": "SC",
            "employmentStatus": "Unemployed",
            "bplCardStatus": "Yes",
            "disabilityStatus": "No",
            "educationLevel": "High School",
            "state": "Bihar",
            "district": "Patna",
            "language": "hi"
        },
        # Person with disability
        {
            "age": "35",
            "gender": "Female",
            "socialCategory": "General",
            "employmentStatus": "Self-Employed",
            "bplCardStatus": "No",
            "disabilityStatus": "Yes",
            "educationLevel": "Diploma",
            "state": "Karnataka",
            "district": "Bangalore",
            "language": "en"
        }
    ]

    for profile in test_profiles:
        test_find_schemes(profile)
        print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    main()
