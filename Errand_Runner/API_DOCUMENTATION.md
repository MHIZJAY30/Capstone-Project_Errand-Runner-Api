# Errand Runner API Documentation

Return to [README.md](README.md) for setup instructions and overview.

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints require JWT authentication. Include token in headers:
`Authorization: Bearer <your_token>`

---

## 📋 User Authentication Endpoints

### Register User
**POST** `/auth/register/`

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "address": "123 Main St, City",
  "user_type": "requester"
}
Response:

json
{
  "message": "User created successfully"
}
Login User
POST /auth/login/

Request:

json
{
  "username": "johndoe",
  "password": "securepassword123"
}
Response:

json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "johndoe"
}
Get/Update Profile
GET/PUT /auth/profile/

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

**In `errands/views.py`:**
```python
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

class ErrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    # ... existing code ...
    
    def get_object(self):
        try:
            errand = super().get_object()
            # Check permissions
            if self.request.user not in [errand.requester, errand.runner] and not self.request.user.is_staff:
                raise PermissionDenied("You don't have permission to access this errand")
            return errand
        except Http404:
            raise Http404("Errand not found")
        except Exception as e:
            raise APIException("Error retrieving errand")

    def update(self, request, *args, **kwargs):
        try:
            errand = self.get_object()
            if request.user != errand.requester:
                return Response(
                    {"error": "Only the requester can update this errand"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": "Validation error", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def assign_runner(request, errand_id):
    try:
        errand = ErrandRequest.objects.get(id=errand_id)
        
        # Check permissions
        if request.user != errand.requester:
            return Response(
                {"error": "Only the requester can assign a runner"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check errand status
        if errand.status != 'pending':
            return Response(
                {"error": f"Cannot assign runner to errand with status: {errand.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        runner_id = request.data.get('runner_id')
        if not runner_id:
            return Response(
                {"error": "runner_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # ... rest of your logic ...
        
    except ErrandRequest.DoesNotExist:
        return Response(
            {"error": "Errand not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Runner not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
🔐 4. Custom Permissions
Create errands/permissions.py:

python
from rest_framework import permissions

class IsRequester(permissions.BasePermission):
    """Only allow the requester to modify their errand"""
    def has_object_permission(self, request, view, obj):
        return obj.requester == request.user

class IsParticipant(permissions.BasePermission):
    """Only allow participants (requester or runner) to access"""
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.requester, obj.runner]

class IsRunner(permissions.BasePermission):
    """Only allow the runner to perform action"""
    def has_object_permission(self, request, view, obj):
        return obj.runner == request.user

class IsCompletedErrand(permissions.BasePermission):
    """Only allow actions on completed errands"""
    def has_object_permission(self, request, view, obj):
        return obj.status == 'completed'
Use in your views:

python
from .permissions import IsRequester, IsParticipant

class ErrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    # ... rest of code ...

class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipant, IsCompletedErrand]
    # ... rest of code ...
