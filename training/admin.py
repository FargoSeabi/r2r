from django.contrib import admin
from .models import TrainingModule, UserTrainingProgress


@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration', 'is_active']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(UserTrainingProgress)
class UserTrainingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'progress', 'completed', 'started_at']
    list_filter = ['completed', 'module__category', 'module__difficulty']
    search_fields = ['user__username', 'module__title']
    readonly_fields = ['id', 'started_at']