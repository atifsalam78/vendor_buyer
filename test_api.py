import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test vendor registration
def test_vendor_registration():
    url = f"{BASE_URL}/register/vendor"
    data = {
        "email": "vendor@example.com",
        "password": "securepassword123",
        "business_name": "Test Vendor Inc.",
        "year_of_establishment": 2010,
        "business_category": "Plumbing & Sanitary",
        "business_type": "Manufacturer",
        "address": "123 Vendor St, Vendor City",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "postal_code": "90001",
        "ntn": "123456789",
        "mobile_number": "+11234567890",
        "landline_number": "+11234567891",
        "website": "https://testvendor.com",
        "gender": "Male"
    }
    
    response = requests.post(url, json=data)
    print("Vendor Registration Response:", response.json())

# Test buyer registration
def test_buyer_registration():
    url = f"{BASE_URL}/register/buyer"
    data = {
        "email": "buyer@example.com",
        "password": "securepassword456",
        "name": "John Buyer",
        "company_name": "Test Buyer Corp",
        "designation": "Manager / Sr. Manager",
        "address": "456 Buyer Ave, Buyer City",
        "country": "United States",
        "state": "New York",
        "city": "New York",
        "mobile_number": "+19876543210",
        "website": "https://testbuyer.com",
        "gender": "Female"
    }
    
    response = requests.post(url, json=data)
    print("Buyer Registration Response:", response.json())

if __name__ == "__main__":
    test_vendor_registration()
    test_buyer_registration()