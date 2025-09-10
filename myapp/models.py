# models.py
import uuid
from django.db import models
from django.utils import timezone

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Rands
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    pf_payment_id = models.CharField(max_length=64, blank=True)     # PayFast payment identifier
    pf_signature = models.CharField(max_length=64, blank=True)      # signature PayFast saw
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id} | {self.user_email} | {self.amount} | {self.status}"
