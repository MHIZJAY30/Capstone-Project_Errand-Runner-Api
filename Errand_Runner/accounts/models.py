from django.conf import settings
from django.db import models

# Create your models here.
class Profile(models.Model):
    USER_TYPES = (
        ('requester', 'Requester'),
        ('runner', 'Runner'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='requester')
    bio = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  
    is_available = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

