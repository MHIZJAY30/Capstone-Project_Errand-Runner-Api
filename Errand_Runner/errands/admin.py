from django.contrib import admin
from .models import ErrandRequest, ErrandItem

# Register your models here.
@admin.register(ErrandRequest)
class ErrandRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'description')

@admin.register(ErrandItem)
class ErrandItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'errand', 'quantity', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'notes')
