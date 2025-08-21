from django.urls import path
from . import views 

urlpatterns = [
    path('errands/', views.ErrandListCreateView.as_view(), name='errand-list'),
    path('errands/<int:pk>/', views.ErrandDetailView.as_view(), name='errand-detail'),
    path('errands/category/<str:category>/', views.ErrandCategoryView.as_view(), name='errand-category'),
    path('errands/status/<str:status>/', views.ErrandStatusView.as_view(), name='errand-status'),
    path('my-errands/', views.MyErrandsView.as_view(), name='my-errands'),
    path('assigned-to-me/', views.AssignedToMeView.as_view(), name='assigned-to-me'),
    path('assign-runner/<int:errand_id>/', views.assign_runner, name='assign-runner'),
    path('errands/<int:errand_id>/items/', views.ErrandItemListCreateView.as_view(), name='errand-items'),
    path('items/<int:pk>/', views.ErrandItemDetailView.as_view(), name='item-detail'),
]