# models.py
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    """Model to store customer information from ticket form"""
    
    class Gender(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"
        NON_BINARY = "non_binary", "Non-binary"
        OTHER = "other", "Other"
        PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer not to say"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    gender = models.CharField(
        max_length=20, 
        choices=Gender.choices, 
        default=Gender.PREFER_NOT_TO_SAY
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Ticket(models.Model):
    """Model to represent individual VR experience tickets"""
    
    class TicketType(models.TextChoices):
        STANDARD = "standard", "Standard VR Experience"
        PREMIUM = "premium", "Premium VR Experience"
        GROUP = "group", "Group VR Experience"
    
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        USED = "used", "Used"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(
        max_length=20, 
        choices=TicketType.choices, 
        default=TicketType.STANDARD
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=35.00)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ACTIVE
    )
    purchase_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    used_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-purchase_date']
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
    
    def __str__(self):
        return f"Ticket {self.id} - {self.customer.full_name} ({self.status})"
    
    @property
    def is_valid(self):
        """Check if ticket is still valid"""
        if self.status != self.Status.ACTIVE:
            return False
        if self.valid_until and timezone.now() > self.valid_until:
            return False
        return True
    
    def mark_as_used(self):
        """Mark ticket as used"""
        self.status = self.Status.USED
        self.used_date = timezone.now()
        self.save()


class Order(models.Model):
    """Enhanced Order model for payment tracking"""
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"
    
    class PaymentMethod(models.TextChoices):
        PAYFAST = "payfast", "PayFast"
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        EFT = "eft", "EFT"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='orders',
        null=True, 
        blank=True
    )
    tickets = models.ManyToManyField(Ticket, related_name='orders', blank=True)
    
    # Legacy field for backward compatibility
    user_email = models.EmailField()
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Rands
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.PAYFAST
    )
    
    # PayFast specific fields
    pf_payment_id = models.CharField(max_length=64, blank=True)
    pf_signature = models.CharField(max_length=64, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Additional fields
    notes = models.TextField(blank=True)
    refund_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        customer_name = self.customer.full_name if self.customer else self.user_email
        return f"Order {self.id} - {customer_name} - R{self.amount} ({self.status})"
    
    @property
    def ticket_count(self):
        """Return number of tickets in this order"""
        return self.tickets.count()
    
    def mark_as_paid(self):
        """Mark order as paid and set paid timestamp"""
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.save()
    
    def calculate_total(self):
        """Calculate total amount based on tickets"""
        return sum(ticket.price for ticket in self.tickets.all())
    
    def can_be_refunded(self):
        """Check if order can be refunded"""
        return self.status == self.Status.PAID and not self.tickets.filter(status=Ticket.Status.USED).exists()
