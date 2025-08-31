from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Avg
from .models import Entrepreneur, Product, Order
from .serializers import EntrepreneurSerializer, ProductSerializer, OrderSerializer
import stripe
from django.conf import settings


class EntrepreneurViewSet(viewsets.ModelViewSet):
    queryset = Entrepreneur.objects.filter(is_active=True)
    serializer_class = EntrepreneurSerializer
    
    def get_queryset(self):
        queryset = Entrepreneur.objects.filter(is_active=True)
        village_id = self.request.query_params.get('village_id')
        specialty = self.request.query_params.get('specialty')
        verified = self.request.query_params.get('verified')
        
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        if specialty:
            queryset = queryset.filter(specialties__icontains=specialty)
        if verified:
            queryset = queryset.filter(is_verified=verified.lower() == 'true')
        
        return queryset.order_by('-is_verified', '-monthly_income')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        entrepreneur_id = self.request.query_params.get('entrepreneur_id')
        is_experience = self.request.query_params.get('is_experience')
        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if category:
            queryset = queryset.filter(category=category)
        if entrepreneur_id:
            queryset = queryset.filter(entrepreneur_id=entrepreneur_id)
        if is_experience:
            queryset = queryset.filter(is_experience=is_experience.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.order_by('-created_at')


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        """Create Stripe payment intent for order"""
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            
            product = Product.objects.get(id=product_id, is_active=True)
            total_amount = product.price * quantity
            
            stripe.api_key = settings.STRIPE_SECRET_KEY
            
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'product_id': str(product.id),
                    'product_name': product.name,
                    'user_id': str(request.user.id),
                    'quantity': quantity
                }
            )
            
            # Create pending order
            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                total_amount=total_amount,
                stripe_payment_intent_id=payment_intent.id,
                status='pending'
            )
            
            return Response({
                'client_secret': payment_intent.client_secret,
                'order_id': order.id
            })
            
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """Confirm payment and update order status"""
        try:
            order = self.get_object()
            order.status = 'confirmed'
            order.save()
            
            # Update product availability if applicable
            if order.product.availability:
                order.product.availability -= order.quantity
                order.product.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)