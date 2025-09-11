from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Customer, Ticket, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model"""
    
    list_display = (
        'full_name', 
        'email', 
        'phone', 
        'age', 
        'gender', 
        'ticket_count',
        'total_spent',
        'created_at'
    )
    list_filter = (
        'gender', 
        'created_at', 
        'age'
    )
    search_fields = (
        'first_name', 
        'last_name', 
        'email', 
        'phone'
    )
    readonly_fields = (
        'id', 
        'created_at', 
        'updated_at',
        'ticket_count',
        'total_spent'
    )
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Demographics', {
            'fields': ('age', 'gender')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('ticket_count', 'total_spent'),
            'classes': ('collapse',)
        })
    )
    
    def ticket_count(self, obj):
        """Display number of tickets purchased by customer"""
        count = obj.tickets.count()
        if count > 0:
            url = reverse('admin:myapp_ticket_changelist') + f'?customer__id__exact={obj.id}'
            return format_html('<a href="{}">{} tickets</a>', url, count)
        return '0 tickets'
    ticket_count.short_description = 'Tickets'
    
    def total_spent(self, obj):
        """Calculate total amount spent by customer"""
        total = sum(order.amount for order in obj.orders.filter(status=Order.Status.PAID))
        return f'R{total:.2f}'
    total_spent.short_description = 'Total Spent'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tickets', 'orders')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin interface for Ticket model"""
    
    list_display = (
        'short_id',
        'customer_link', 
        'ticket_type', 
        'price', 
        'status',
        'is_valid_display',
        'purchase_date',
        'used_date'
    )
    list_filter = (
        'ticket_type', 
        'status', 
        'purchase_date',
        'used_date'
    )
    search_fields = (
        'customer__first_name', 
        'customer__last_name', 
        'customer__email',
        'id'
    )
    readonly_fields = (
        'id', 
        'purchase_date',
        'is_valid_display',
        'used_date'
    )
    raw_id_fields = ('customer',)
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('customer', 'ticket_type', 'price', 'status')
        }),
        ('Validity', {
            'fields': ('valid_until', 'is_valid_display')
        }),
        ('Usage Tracking', {
            'fields': ('purchase_date', 'used_date'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_used', 'mark_as_cancelled']
    
    def short_id(self, obj):
        """Display shortened ticket ID"""
        return str(obj.id)[:8] + '...'
    short_id.short_description = 'Ticket ID'
    
    def customer_link(self, obj):
        """Link to customer admin page"""
        url = reverse('admin:myapp_customer_change', args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>', url, obj.customer.full_name)
    customer_link.short_description = 'Customer'
    
    def is_valid_display(self, obj):
        """Display ticket validity with color coding"""
        if obj.is_valid:
            return format_html('<span style="color: green;">✓ Valid</span>')
        else:
            return format_html('<span style="color: red;">✗ Invalid</span>')
    is_valid_display.short_description = 'Valid'
    
    def mark_as_used(self, request, queryset):
        """Admin action to mark tickets as used"""
        updated = 0
        for ticket in queryset:
            if ticket.status == Ticket.Status.ACTIVE:
                ticket.mark_as_used()
                updated += 1
        self.message_user(request, f'{updated} tickets marked as used.')
    mark_as_used.short_description = 'Mark selected tickets as used'
    
    def mark_as_cancelled(self, request, queryset):
        """Admin action to cancel tickets"""
        updated = queryset.update(status=Ticket.Status.CANCELLED)
        self.message_user(request, f'{updated} tickets cancelled.')
    mark_as_cancelled.short_description = 'Cancel selected tickets'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""
    
    list_display = (
        'short_id',
        'customer_or_email',
        'amount',
        'status',
        'payment_method',
        'ticket_count_display',
        'created_at',
        'paid_at'
    )
    list_filter = (
        'status', 
        'payment_method',
        'created_at',
        'paid_at'
    )
    search_fields = (
        'user_email',
        'customer__first_name',
        'customer__last_name', 
        'customer__email',
        'id',
        'pf_payment_id'
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'ticket_count_display',
        'calculated_total'
    )
    raw_id_fields = ('customer',)
    filter_horizontal = ('tickets',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'user_email', 'amount', 'status', 'payment_method')
        }),
        ('Tickets', {
            'fields': ('tickets', 'ticket_count_display', 'calculated_total')
        }),
        ('PayFast Information', {
            'fields': ('pf_payment_id', 'pf_signature'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'refund_reason'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_paid', 'mark_as_cancelled', 'mark_as_refunded']
    
    def short_id(self, obj):
        """Display shortened order ID"""
        return str(obj.id)[:8] + '...'
    short_id.short_description = 'Order ID'
    
    def customer_or_email(self, obj):
        """Display customer name or email"""
        if obj.customer:
            url = reverse('admin:myapp_customer_change', args=[obj.customer.id])
            return format_html('<a href="{}">{}</a>', url, obj.customer.full_name)
        return obj.user_email
    customer_or_email.short_description = 'Customer'
    
    def ticket_count_display(self, obj):
        """Display number of tickets in order"""
        count = obj.ticket_count
        if count > 0:
            return f'{count} tickets'
        return 'No tickets'
    ticket_count_display.short_description = 'Tickets'
    
    def calculated_total(self, obj):
        """Display calculated total from tickets"""
        total = obj.calculate_total()
        if total != obj.amount:
            return format_html(
                'R{:.2f} <span style="color: orange;">(differs from order amount)</span>', 
                total
            )
        return f'R{total:.2f}'
    calculated_total.short_description = 'Calculated Total'
    
    def mark_as_paid(self, request, queryset):
        """Admin action to mark orders as paid"""
        updated = 0
        for order in queryset:
            if order.status == Order.Status.PENDING:
                order.mark_as_paid()
                updated += 1
        self.message_user(request, f'{updated} orders marked as paid.')
    mark_as_paid.short_description = 'Mark selected orders as paid'
    
    def mark_as_cancelled(self, request, queryset):
        """Admin action to cancel orders"""
        updated = queryset.filter(status=Order.Status.PENDING).update(
            status=Order.Status.CANCELLED
        )
        self.message_user(request, f'{updated} orders cancelled.')
    mark_as_cancelled.short_description = 'Cancel selected orders'
    
    def mark_as_refunded(self, request, queryset):
        """Admin action to mark orders as refunded"""
        updated = 0
        for order in queryset:
            if order.can_be_refunded():
                order.status = Order.Status.REFUNDED
                order.save()
                updated += 1
        self.message_user(request, f'{updated} orders marked as refunded.')
    mark_as_refunded.short_description = 'Mark selected orders as refunded'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer').prefetch_related('tickets')


# Customize admin site header and title
admin.site.site_header = 'Roots to Realities Admin'
admin.site.site_title = 'R2R Admin'
admin.site.index_title = 'VR Experience Management'
