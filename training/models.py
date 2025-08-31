from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


class TrainingModule(models.Model):
    CATEGORY_CHOICES = [
        ('digital-literacy', 'Digital Literacy'),
        ('ecommerce', 'E-commerce'),
        ('marketing', 'Marketing'),
        ('ubuntu-principles', 'Ubuntu Principles'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration = models.PositiveIntegerField()  # in minutes
    video_url = models.URLField(blank=True)
    material_urls = ArrayField(models.URLField(), blank=True, default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.category}"

    class Meta:
        ordering = ['-created_at']


class UserTrainingProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='training_progress')
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='user_progress')
    progress = models.PositiveIntegerField(default=0)  # percentage 0-100
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.module.title} - {self.progress}%"

    class Meta:
        ordering = ['-started_at']
        unique_together = ['user', 'module']