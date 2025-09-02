import requests

# URL of the login page
login_url = "http://localhost:8000/users/login/"

# Test credentials for driver user
payload = {
    "username": "7026746330",
    "password": "Agr@9876"
}

# Start a session to persist cookies
session = requests.Session()

# Get the login page to get CSRF token
response = session.get(login_url)
if response.status_code != 200:
    print(f"Failed to load login page: {response.status_code}")
    exit(1)

# Extract CSRF token from cookies or page content
csrf_token = session.cookies.get('csrftoken')
if not csrf_token:
    print("CSRF token not found in cookies")
    exit(1)

# Add CSRF token to payload
payload['csrfmiddlewaretoken'] = csrf_token

# Headers including Referer for CSRF protection
headers = {
    "Referer": login_url
}

# Post login data
login_response = session.post(login_url, data=payload, headers=headers)

if login_response.url == login_url:
    print("Login failed: check credentials")
else:
    print("Login successful")

# Optionally, access a protected page to verify login
protected_url = "http://localhost:8000/tracking/live/"
protected_response = session.get(protected_url)
if protected_response.status_code == 200:
    print("Access to protected page successful")
else:
    print(f"Failed to access protected page: {protected_response.status_code}")
