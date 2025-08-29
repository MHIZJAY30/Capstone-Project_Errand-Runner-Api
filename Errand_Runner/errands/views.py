from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, APIView
from django.db import DatabaseError
from .models import ErrandRequest, ErrandItem, Review
from .serializers import ErrandRequestSerializer, ErrandRequestCreateSerializer, ErrandItemSerializer, ReviewSerializer, Review
from rest_framework.exceptions import ValidationError, PermissionDenied, APIException
from django.http import Http404, JsonResponse
from rest_framework.permissions import IsAuthenticated,  AllowAny
from .permissions import IsRequester, IsParticipant, IsCompletedErrand

# Create your views here.
class ErrandListCreateView(generics.ListCreateAPIView):
    queryset = ErrandRequest.objects.all().select_related('user', 'runner')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ErrandRequestCreateSerializer
        return ErrandRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ErrandRequestListCreateView(generics.ListCreateAPIView):
    queryset = ErrandRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ErrandRequestCreateSerializer  
        return ErrandRequestSerializer  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ErrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ErrandRequest.objects.all().select_related('user', 'runner')
    serializer_class = ErrandRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_object(self):
        try:
            errand = super().get_object()
            if self.request.user not in [errand.requester, errand.runner] and not self.request.user.is_staff:
                raise PermissionDenied("You don't have permission to access this errand")
            return errand
        except Http404:
            raise Http404("Errand not found")
        except DatabaseError as e:  
            raise APIException("Database error occurred while retrieving errand")
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


class ErrandItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ErrandItem.objects.all()
    serializer_class = ErrandItemSerializer
    permission_classes = {permissions.IsAuthenticated}

class MyErrandsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        errands = [
            {"id": 1, "title": "Buy groceries", "status": "pending"},
            {"id": 2, "title": "Pick up laundry", "status": "completed"},
        ]
        return Response(errands)

class ErrandItemCreateView(generics.CreateAPIView):
    queryset = ErrandItem.objects.all()
    serializer_class = ErrandItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        errand_id = self.request.data.get("errand")
        serializer.save(errand_id=errand_id)


class AssignedToMeView(generics.ListAPIView):
    serializer_class = ErrandRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ErrandRequest.objects.filter(runner=self.request.user)

class ErrandItemListView(generics.ListAPIView):
    serializer_class = ErrandItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        errand_id = self.kwargs['errand_id']
        return ErrandItem.objects.filter(errand_id=errand_id)
    
class ErrandCategoryView(generics.ListAPIView):
    serializer_class = ErrandRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category']
        return ErrandRequest.objects.filter(items__category__iexact=category).distinct()

class ErrandStatusView(generics.ListAPIView):
    serializer_class = ErrandRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status = self.kwargs['status']
        return ErrandRequest.objects.filter(status__iexact=status)

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant, IsCompletedErrand]

    def get_queryset(self):
        return Review.objects.filter(errand_id=self.kwargs['errand_id'])

    def perform_create(self, serializer):
        errand = ErrandRequest.objects.get(id=self.kwargs['errand_id'])
        
        if self.request.user == errand.requester:
            reviewee = errand.runner
        elif self.request.user == errand.runner:
            reviewee = errand.requester
        else:
            raise PermissionDenied("You can only review participants of this errand")
        
        if Review.objects.filter(errand=errand, reviewer=self.request.user).exists():
            raise ValidationError("You have already reviewed this errand")
        
        serializer.save(
            errand=errand,
            reviewer=self.request.user,
            reviewee=reviewee
        )

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

class UserReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(reviewee_id=user_id)


def home_view(request):
    return render(request, 'base.html')

def test_api(request):
    return JsonResponse({"message": "API is working!"})
    
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def assign_runner(request, errand_id):
    try:
        errand = ErrandRequest.objects.get(id=errand_id)
        runner_id = request.data.get('runner_id')

        if request.user != errand.requester:
            return Response(
                {"error": "Only the requester can assign a runner"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if errand.status != 'pending':
            return Response(
                {"error": f"Cannot assign runner to errand with status: {errand.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if runner_id:
            from django.contrib.auth.models import User
            runner = User.objects.get(id=runner_id)
            errand.runner = runner
            errand.status = 'in_progress'
            errand.save()
            
            return Response({"message": f"Runner {runner.username} assigned to errand"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "runner_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
    except ErrandRequest.DoesNotExist:
        return Response({"error": "Errand not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"error": "Runner not found"}, status=status.HTTP_404_NOT_FOUND)
    except DatabaseError as e:  
        return Response(
            {"error": "Database error occurred", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
    except ErrandRequest.DoesNotExist:
        raise Http404("Errand not found")
    except DatabaseError as e:  
        raise APIException("Database error occurred while creating review")
    except Exception as e:
        raise APIException("Error creating review")


@api_view(['GET'])
@permission_classes([AllowAny]) 
def test_simple(request):
    return Response({"message": "This endpoint works!"})    