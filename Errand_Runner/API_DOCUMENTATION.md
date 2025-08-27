# Errand Runner API Documentation

Return to [README.md](README.md) for setup instructions and overview.

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints require JWT authentication. Include token in headers:
`Authorization: Bearer <your_token>`

---

# User Authentication Endpoints

1. # Register User
POST /api/auth/register/

Description:
Creates a new user account with a username, email, and password.

# Request:
Request Body - json
{
  "username": "testuser",
  "email": "mary@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "address": "123 Main St, City",
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
POST /api/auth/login/

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
  "user_id": 1,
  "username": "testuser"
}


3. # Get/Update Profile
GET/PUT /api/auth/profile/

Response:

json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "full_name": "John Doe",
  "phone": "+1234567890",
  "address": "123 Main St, City",
  "user_type": "requester",
  "bio": "",
  "rating": 0.0,
  "is_available": true
}
📋 Errand Endpoints
List/Create Errands
GET/POST /errands/

Create Request:

json
{
  "title": "Grocery Shopping",
  "description": "Need milk, eggs, and bread",
  "status": "pending"
}
Response:

json
{
  "id": 1,
  "title": "Grocery Shopping",
  "description": "Need milk, eggs, and bread",
  "status": "pending",
  "requester": 1,
  "runner": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "items": [],
  "reviews": []
}
Get/Update/Delete Errand
GET/PUT/DELETE /errands/{id}/

Filter Errands by Category
GET /errands/category/{category}/
Example: /errands/category/food/

Filter Errands by Status
GET /errands/status/{status}/
Example: /errands/status/completed/

Get User's Errands
GET /my-errands/

Get Assigned Errands
GET /assigned-to-me/

Assign Runner
PUT /assign-runner/{errand_id}/

Request:

json
{
  "runner_id": 2
}
Response:

json
{
  "message": "Runner username assigned to errand"
}
📋 Errand Item Endpoints
List/Create Items for Errand
GET/POST /errands/{errand_id}/items/

Create Request:

json
{
  "name": "Milk",
  "quantity": 2,
  "category": "dairy",
  "notes": "Organic whole milk"
}
Get/Update/Delete Item
GET/PUT/DELETE /items/{id}/

📋 Review Endpoints
List/Create Reviews for Errand
GET/POST /errands/{errand_id}/reviews/

Create Request:

json
{
  "rating": 5,
  "comment": "Excellent service! Delivered quickly."
}
Get User Reviews
GET /users/{user_id}/reviews/

🔐 Permission Requirements
Only authenticated users can access all endpoints

Only requester can update/delete their errands

Only participants can review completed errands

Only requester can assign runners to their errands

🚦 Status Codes
200: Success

201: Created

400: Bad Request

401: Unauthorized

403: Forbidden

404: Not Found

409: Conflict

500: Server Error

text

---

## 🧪 2. Testing Guide with Thunder Client

### Step 1: Install Thunder Client
- VS Code → Extensions → Search "Thunder Client" → Install

### Step 2: Create Collection
1. Open Thunder Client
2. Click "Collections" → "New Collection"
3. Name it "Errand Runner API"

### Step 3: Test Authentication
**Request 1: Register**
POST http://localhost:8000/api/auth/register/
Body (JSON):
{
"username": "testuser",
"email": "test@example.com",
"password": "testpass123",
"full_name": "Test User",
"phone": "1234567890",
"user_type": "requester"
}

text

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

