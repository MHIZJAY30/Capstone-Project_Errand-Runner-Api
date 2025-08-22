from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import ErrandRequest, ErrandItem
from .serializers import ErrandRequestSerializer, ErrandItemSerializer, ErrandRequestCreateSerializer

# Create your views here.
class ErrandRequestListCreateView(generics.ListCreateAPIView):
    queryset = ErrandRequest.objects.all().select_related('user', 'runner')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ErrandRequestCreateSerializer
        return ErrandRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ErrandRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ErrandRequest.objects.all().select_related('user', 'runner')
    serializer_class = ErrandRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def assign_runner(request, errand_id):
    try:
        errand = ErrandRequest.objects.get(id=errand_id)
        runner_id = request.data.get('runner_id')
        
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

