from django.contrib import admin
from .models import ErrandRequest

# Register your models here.
@admin.register(ErrandRequest)
class ErrandRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'description')
