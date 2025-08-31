from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


class Village(models.Model):
    CATEGORY_CHOICES = [
        ('crafts', 'Crafts'),
        ('music', 'Music'),
        ('food', 'Food'),
        ('rituals', 'Rituals'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.URLField()
    vr_images = ArrayField(models.URLField(), blank=True, default=list)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    visit_count = models.PositiveIntegerField(default=0)
    experience_duration = models.PositiveIntegerField()  # in minutes
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.region}, {self.country}"

    class Meta:
        ordering = ['-created_at']


class AIStory(models.Model):
    CATEGORY_CHOICES = [
        ('historical', 'Historical'),
        ('cultural', 'Cultural'),
        ('personal', 'Personal'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='ai_stories')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    personalized_for = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.village.name}"

    class Meta:
        ordering = ['-generated_at']