# Errand Runner API Documentation

Return to [README.md](README.md) for setup instructions and overview.

## Base URL
`http://localhost:http://127.0.0.1:80008000/api/`

## Authentication
All endpoints require JWT authentication. Include token in headers:
`Authorization: Bearer <your_token>`

---

# User Authentication Endpoints

1. # Register User
POST http://127.0.0.1:8000/api/auth/register/

Description:
Creates a new user account with a username, email, and password.
# Request:
Request Body - json
{
    "username": "testuser2",
    "password": "testpass123",
    "email": "test2@example.com",
    "full_name": "Test User2",
    "phone": "1234567890",
    "user_type": "requester"
}
# Response:
json
{
  "user": {
  "id": 1,
  "username": "testuser",
  "email": "mary@example.com"
  }
}


2. # Login User
POST http://127.0.0.1:8000/api/auth/login/
Description:
Logs in a user and returns a JWT token for authentication.
# Request:
Request Body - json
{
  "username": "testuser",
  "password": "securepassword123",
}
Response:

json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
  "user_id": 4,
  "username": "testuser2"
}
*Save the access token* from response for next requests.


3. # Refresh Access Token
POST http://127.0.0.1:8000/api/auth/token/refresh/
Description:
Used to refresh the access token when it expires, using the refresh token.
# Request:
Request Body (JSON):
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}
Response (200 OK):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}

4. # User Profile (Retrieve & Update)
GET http://127.0.0.1:8000/api/auth/profile/
Description:
Retrieves the currently logged-in user’s profile details.
Response (200 OK):
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
# Endpoint (PUT/PATCH):
PUT http://127.0.0.1:8000/api/auth/profile/
Description:
Allows users to update their account details.
# Request:
Request Body (JSON):
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "newemail@example.com"
}
Response (200 OK):
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}


5. # Create Errand(Core Feature)
# a. Create a New Errand/Task
POST http://127.0.0.1:8000/api/errands/
Description:
Allows users to update their errand details.
# Request:
Request Body (JSON):
{
    "title": "Grocery Shopping",
    "description": "Buy milk, eggs, and bread"
}
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
{
  "title": "Grocery Shopping",
  "description": "Buy milk, eggs, and bread",
  "status": "pending"
}

# b. List All Errands/Tasks
GET http://127.0.0.1:8000/api/errands/
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[
  {
    "id": 1,
    "items": [],
    "reviews": [],
    "runner_username": null,
    "title": "Grocery Shopping",
    "description": "Buy milk, eggs, and bread",
    "pickup_location": "",
    "dropoff_location": "",
    "status": "pending",
    "created_at": "2025-08-29T21:27:54.729504Z",
    "updated_at": "2025-08-29T21:27:54.729573Z",
    "deadline": null,
    "runner_confirmed": false,
    "user": 4,
    "runner": null
  }
]

# c. Update/Delete an Errand
PUT    http://127.0.0.1:8000/api/errands/
DELETE http://127.0.0.1:8000/api/errands/{id}/


6. #  Get My Errands
GET http://127.0.0.1:8000/api/my-errands/
Description:
Allows users to see their their errands and the status
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[
  {
    "id": 1,
    "title": "Buy groceries",
    "status": "pending"
  },
  {
    "id": 2,
    "title": "Pick up laundry",
    "status": "completed"
  }
]

7. #  Get Assigned Errands(Runner)
GET http://127.0.0.1:8000/api/assigned-to-me/
Description:
Allows runners to see their their errands and the status
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[]
it’s returning an empty list because there are currently no errands in the database that are assigned to the authenticated user at the moment






**Request 2: Login**
POST http://localhost:8000/api/auth/login/
Body (JSON):
{
"username": "testuser",
"password": "testpass123"
}

text

**Save the access token** from response for next requests.

### Step 4: Test Errand Operations
**Request 3: Create Errand** (add Authorization header with token)
POST http://localhost:8000/api/errands/
Headers: Authorization: Bearer <your_token>
Body:
{
"title": "Test Errand",
"description": "This is a test errand"
}

text

**Request 4: Get All Errands**
GET http://localhost:8000/api/errands/
Headers: Authorization: Bearer <your_token>

text

### Step 5: Test Error Scenarios
**Request 5: Try accessing without token**
GET http://localhost:8000/api/errands/
// Should return 401 Unauthorized

text

**Request 6: Try invalid errand ID**
GET http://localhost:8000/api/errands/9999/
Headers: Authorization: Bearer <your_token>
// Should return 404 Not Found

text

---

## 🛡️ 3. Enhanced Error Handling

### Update your views with proper error handling:

