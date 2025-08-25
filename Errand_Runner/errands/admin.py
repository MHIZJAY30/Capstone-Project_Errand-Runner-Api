from django.contrib import admin
from .models import ErrandRequest, ErrandItem, Review

# Register your models here.
@admin.register(ErrandRequest)
class ErrandRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')

@admin.register(ErrandItem)
class ErrandItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'errand', 'quantity', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'notes')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('errand', 'reviewer', 'reviewee', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment',)