from django.conf import settings
from django.db import models

# Create your models here.
class ErrandRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_errands')
    runner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_errands')
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
    CATEGORY_CHOICES = (('grocery', 'Grocery'), ('document', 'Document'), ('package', 'Package'), ('other', 'Other'),)
    errand = models.ForeignKey(ErrandRequest, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')


    def __str__(self):
        return f"{self.name} x{self.quantity} {self.errand.title} {self.category}"


