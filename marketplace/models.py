from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
from villages.models import Village


class Entrepreneur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    location = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='entrepreneurs', null=True, blank=True)
    specialties = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    families_supported = models.PositiveIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        ordering = ['-created_at']


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('handcrafts', 'Handcrafts'),
        ('food', 'Food'),
        ('textiles', 'Textiles'),
        ('experiences', 'Experiences'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.URLField()
    entrepreneur = models.ForeignKey(Entrepreneur, on_delete=models.CASCADE, related_name='products')
    is_experience = models.BooleanField(default=False)
    duration = models.PositiveIntegerField(null=True, blank=True)  # for experiences, in minutes
    availability = models.PositiveIntegerField(null=True, blank=True)  # stock count
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.entrepreneur.name}"

    class Meta:
        ordering = ['-created_at']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.product.name}"

    class Meta:
        ordering = ['-created_at']