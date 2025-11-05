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

### This step is vital to accessing the API as it is only authorized for 'Admins'
### since it checks if the user logged in has a role of 'admin' AND is an Admin 
### specifically in Django or 'is_superuser' is True
### See: api/permissions/IsRideUserAdmin
6. Change superuser's role
    In terminal:
        - 'python manage.py runserver'
    In web:
        - Visit admin page (http://127.0.0.1:8000/admin/)
        - Login with your superuser credentials
        - Click on Users on the API section on the left side of the browser.
        - Click on your superuser username.
        - Change role to admin

7. Uncomment # RideEvent._meta.get_field('created').editable = True from admin.py in order to test 'rides over 1 hour' for the report instantly without waiting
since auto_now_add=True is implemented in models which is a Django feature

# API USAGE
### For API endpoints, refer to the Postman collection below for easy guidance.
### It is recommended to use the Postman collection for testing the API in full.
### The Postman collection is easy to use since it is a top-down approach in
### making requests starting with 'api/login/' to fetch an access token
### in order to make authorized requests in the API endpoints.
### If an API endpoint being tested responds with an 'invalid token', 
### just make a request in 'api/refresh/' endpoint and retest.
### The postman collection automatically sets the access_token(Bearer Token)
### and the refresh token for fetching a new access token.
### Also: non-admin users that are 'logged in' will only get 'Unauthorized'
### responses in ALL endpoints(as required)


# POSTMAN COLLECTION #
[Download Ride API Postman Collection](https://raw.githubusercontent.com/lanceallendavis/ride-api/refs/heads/main/postman/Ride.postman_collection.json)

### Postman usage
1. Open Postman
2. Import [Ride API Collection](https://raw.githubusercontent.com/lanceallendavis/ride-api/refs/heads/main/postman/Ride.postman_collection.json)
3. Import [Ride API Environment](https://raw.githubusercontent.com/lanceallendavis/ride-api/refs/heads/main/postman/Ride.postman_collection.json)
4. Set Environment to Ride API
5. Ensure that "{{base_url}}" is set to "http://127.0.0.1:8000/api"


# BONUS QUERY: REPORT
1. From the project's root directory, run 'python api/scripts/export_monthly.py'
2. Check below, there should be a file called 'driver_trips_over_1_hour.xlsx
### Note: it is an excel sheet
### The raw query is also there



# CODE NOTES 

### AbstractUser is utilized to extend Django's User model for authentication
### and customization as required in the assessment(such as phone number)

### DRF's simple JWT is utilitzed for Access Tokens and Refresh Tokens for 
### simple standard authentication.
### The endpoints 'api/login/' and 'api/refresh/' are only views since there
### is no other use for these endpoints other than requesting for tokens,
### therefore unnecessary to wrap it in a Viewset

### For views, ReadOnlyModelViewsets are used as it is to prevent undesired/accidental/invalid requests other than 'GET' in BASE api urls such as 'api/users/'.
### Also added comments/notes in endpoints(viewsets).

### Default SQLite over MySQL/PostgreSQL for ease of access/use/testing for the assessment
### Containerizing into a Docker image/volume also adds an additional step for setup


# CHALLENGES FACED #
### The distance between pick up point and gps location point was difficult,
### could be best optimized with GeoDjango(used by Grab/Uber), performance wise.
### Willing to be exposed more in this feature by Django I haven't utilized yet.

