# API set-up guide

1. Clone the repository in a desired/empty directory
    In terminal:
        - 'git clone https://github.com/lanceallendavis/ride-api.git'
2. Go to directory, create and activate a python virtual environment.
    In terminal:
        - 'python -m venv api_env'
        - (Windows):'api_env\Scripts\activate' 
        - (macOs/Linux): 'source api_env/bin/activate'
3. Go to project directory and install modules.
    In terminal:
        - 'cd ride'
        - 'python -m pip install -r requirements.txt'

4. Run migrations
    In terminal:
        - 'python manage.py migrate'

5. Create a superuser
    In terminal:
        - 'python manage.py createsuperuser'
        - Enter username of your choice
        - Enter password of your choice

# This step is vital to accessing the API as it is only authorized for 'Admins'
# since it checks if the user logged in has a role of 'admin' AND is an Admin 
# specifically in Django or 'is_superuser' is True
6. Change superuser's role
    In terminal:
        - 'python manage.py runserver'
    In web:
        - Visit admin page (http://127.0.0.1:8000/admin/)
        - Login with your superuser credentials
        - Click on Users on the API section on the left side of the browser.
        - Click on your superuser username.
        - Change role to admin

### API USAGE ###
# For API endpoints, refer to the Postman collection for easy guidance.
# It is recommended to use the Postman collection for testing the API in full.
# The Postman collection is easy to use since it is a top-down approach in
# making requests starting with 'api/login/' to fetch an access token
# in order to make authorized requests in the API endpoints.
# If an API endpoint being tested responds with an 'invalid token', 
# just make a request in 'api/refresh/' endpoint and retest.
# The postman collection automatically sets the access_token(Bearer Token)
# and the refresh token for fetching a new access token


### POSTMAN COLLECTION """
[Download Ride API Postman Collection](https://raw.githubusercontent.com/lanceallendavis/ride-api/refs/heads/main/postman/Ride.postman_collection.json)

# Postman usage
1. Open Postman
2. Import [Ride API Collection](https://raw.githubusercontent.com/lanceallendavis/ride-api/refs/heads/main/postman/Ride.postman_collection.json)
3. Import [Ride API Environment](https://raw.githubusercontent.com/lanceallendavis/ride-api/refs/heads/main/postman/Ride.postman_collection.json)
4. Set Environment to Ride API
5. Ensure that "{{base_url}}" is set to "http://127.0.0.1:8000/api"

    

### CODE NOTES ###

# AbstractUser is utilized to extend Django's User model for authentication
# and customization as required in the assessment(such as phone number)

# DRF's simple JWT is utilitzed for Access Tokens and Refresh Tokens for 
# simple standard authentication.
# The endpoints 'api/login/' and 'api/refresh/' are only views since there
# is no other use for these endpoints other than requesting for tokens,
# therefore unnecessary to wrap it in a Viewset

# For views, ReadOnlyModelViewsets are used as it is to prevent unwanted 
# requests other than 'GET' in BASE api urls such as 'api/users/1/'.
