from django.urls import path
from . import views 


urlpatterns = [
    # Errand endpoints
    path('errands/', views.ErrandRequestListCreateView.as_view(), name='errand-list'),
    path('errands/<int:pk>/', views.ErrandDetailView.as_view(), name='errand-detail'),
    path('errands/category/<str:category>/', views.ErrandCategoryView.as_view(), name='errand-category'),
    path('errands/status/<str:status>/', views.ErrandStatusView.as_view(), name='errand-status'),
    path('my-errands/', views.MyErrandsView.as_view(), name='my-errands'),
    path('assigned-to-me/', views.AssignedToMeView.as_view(), name='assigned-to-me'),
    path('assign-runner/<int:errand_id>/', views.assign_runner, name='assign-runner'),
    
    # ErrandItem endpoints
    path('errands/<int:errand_id>/items/', views.ErrandItemCreateView.as_view(), name='errand-items'),
    path('items/<int:pk>/', views.ErrandItemDetailView.as_view(), name='item-detail'),
    
    # Review endpoints
    path('errands/<int:errand_id>/reviews/', views.ReviewListCreateView.as_view(), name='errand-reviews'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('users/<int:user_id>/reviews/', views.UserReviewsView.as_view(), name='user-reviews'),
    
    # Test endpoints
    path('test/', views.test_api, name='test-api'),
    path('test-simple/', views.test_simple, name='test-simple'),
]