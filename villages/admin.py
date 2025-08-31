from django.contrib import admin
from .models import Village, AIStory


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'region', 'category', 'rating', 'visit_count', 'is_active']
    list_filter = ['country', 'category', 'is_active']
    search_fields = ['name', 'description', 'region']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(AIStory)
class AIStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'village', 'category', 'generated_at']
    list_filter = ['category', 'village']
    search_fields = ['title', 'content']
    readonly_fields = ['id', 'generated_at']