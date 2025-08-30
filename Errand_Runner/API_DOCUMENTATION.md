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
A new user can sign up
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
A user logs in and gets a token to use the app.
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
Show the current user's profile.
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
Update the profile (like address, phone number, user type).
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
Create a new errand request
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
Description:
See a list of all errands in the system.
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
Description:
Update an errand (maybe the title or status).
# delete
Description:
Remove an errand
DELETE http://127.0.0.1:8000/api/errands/{id}/


6. #  Get My Errands
GET http://127.0.0.1:8000/api/my-errands/
Description:
Allows users to see their their errands and the status
The user sees only errands they created.
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
The runners sees errands that were assigned to them.
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[]
it’s returning an empty list because there are currently no errands in the database that are assigned to the authenticated user at the moment



8. # Create an Errand Item
POST http://127.0.0.1:8000/api/errands/{errand_id}/items/ (erand_id 1)

summary='Example of creating an errand item under a specific errand'
Description:
Add new items to the shopping list.
Creates a new item under a specific errand. 'This request creates a new item ("Milk") under errand ID 1.'
# Request:
Request Body (JSON):
{
    "name": "Milk", 
    "quantity": 2,
    "category": "groceries",  
    "notes": "Whole milk"
}
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
{
  "id": 2,
  "name": "Milk",
  "quantity": 2,
  "price": null,
  "category": "groceries"
}


9. # Assign Runner to Errand
PUT http://127.0.0.1:8000/api/assign-runner/1/
Description:
The user assigns a runner to an errand
# Request:
Request Body (JSON):
{
    "runner_id": 2
}
Note: You need a runner user ID. Create a runner user first:
{
    "username": "runner1",
    "password": "runnerpass123",
    "email": "runner@example.com",
    "user_type": "runner"
}
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
{
  "message": "Runner lenovo assigned to errand"
}


10. # Filter Errands by Category
GET http://127.0.0.1:8000/api/errands/category/{category}/
Test with:
GET /api/errands/category/food/
GET /api/errands/category/groceries/
GET /api/errands/category/medicine/
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[
  
    "id": 1,
    "items": [
      {
        "id": 1,
        "name": "Milk",
        "quantity": 2,
        "price": null,
        "category": "groceries"
      },
      {.............
       
    ]

]


11. # Filter Errands by Status
GET http://127.0.0.1:8000/api/errands/status/{status}/
Test with:
GET /api/errands/status/pending/
GET /api/errands/status/in_progress/
GET /api/errands/status/completed/
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[
  {
    "id": 1,
    "items": 
      {
        "id": 1,
        "name": "Milk",
        "quantity": 2,
        "price": null,
        "category": "groceries"
      },
    ......................
  }
]


12. # Get/Update/Delete Specific Items
GET http://127.0.0.1:8000/api/items/{id}/
PUT http://127.0.0.1:8000/api/items/{id}/
DELETE http://127.0.0.1:8000/api/items/{id}/
# Body for PUT:
{
    "name": "Updated Item Name", (milk)
    "quantity": 5,
    "category": "updated_category" (groceries)
}
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
{
  "id": 1,
  "name": "milk",
  "quantity": 5,
  "price": null,
  "category": "groceries"
}


12. # Review System
POST http://127.0.0.1:8000/api/errands/{errand_id}/reviews/
# Request:
Request Body (JSON):
{
    "rating": 5,
    "comment": "Excellent service! Very fast delivery."
}
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
{
  "id": 1,
  "errand": 1,
  "reviewer": 4,
  "reviewer_username": "testuser2",
  "reviewee": 1,
  "reviewee_username": "lenovo",
  "rating": 5,
  "comment": "Excellent service! Very fast delivery.",
  "created_at": "2025-08-30T13:52:14.991986Z"
}

# 
GET http://127.0.0.1:8000/api/errands/{errand_id}/reviews/
# token
Auth (bearer token)
"access": (eyJhbGciOiJIUzI1NiIsInR5cCI6...)
Response (200 Created):
[
  {
    "id": 1,
    "errand": 1,
    "reviewer": 4,
    "reviewer_username": "testuser2",
    "reviewee": 1,
    "reviewee_username": "lenovo",
    "rating": 5,
    "comment": "Excellent service! Very fast delivery.",
    "created_at": "2025-08-30T13:52:14.991986Z"
  }
]


13. # Test Error Scenarios
Try accessing without token**
GET http://localhost:8000/api/errands/
Response:
Should return 401 Unauthorized



