from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ErrandRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    runner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='errands_assigned')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pickup_location = models.CharField(max_length=255, blank=True)
    dropoff_location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True) 
    runner_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.status}"

class ErrandItem(models.Model):
    CATEGORY_CHOICES = (('Groceries', 'Groceries'), ('Documents', 'Documents'), ('Packages', 'Packages'), ('Other', 'Other'),)
    errand = models.ForeignKey(ErrandRequest, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')


    def __str__(self):
        return f"{self.name} x{self.quantity} {self.errand.title} {self.category}"


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    errand = models.ForeignKey(ErrandRequest, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['errand', 'reviewer']  
    
    def __str__(self):
        return f"{self.rating} stars for {self.reviewee.username} by {self.reviewer.username}"

