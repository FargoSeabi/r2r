from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import TrainingModule, UserTrainingProgress
from .serializers import TrainingModuleSerializer, UserTrainingProgressSerializer


class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.filter(is_active=True)
    serializer_class = TrainingModuleSerializer
    
    def get_queryset(self):
        queryset = TrainingModule.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('difficulty', 'duration')
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get available training categories"""
        categories = TrainingModule.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get training statistics"""
        stats = {
            'total_modules': TrainingModule.objects.filter(is_active=True).count(),
            'categories': list(TrainingModule.objects.filter(is_active=True).values_list('category', flat=True).distinct()),
            'difficulty_distribution': dict(
                TrainingModule.objects.filter(is_active=True)
                .values('difficulty')
                .annotate(count=Count('id'))
                .values_list('difficulty', 'count')
            )
        }
        return Response(stats)


class UserTrainingProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserTrainingProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserTrainingProgress.objects.filter(user=self.request.user).order_by('-started_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get user training dashboard data"""
        user_progress = UserTrainingProgress.objects.filter(user=request.user)
        
        stats = {
            'total_modules_started': user_progress.count(),
            'completed_modules': user_progress.filter(completed=True).count(),
            'in_progress_modules': user_progress.filter(completed=False).count(),
            'average_progress': user_progress.aggregate(avg_progress=Avg('progress'))['avg_progress'] or 0,
            'recent_activity': UserTrainingProgressSerializer(
                user_progress.order_by('-started_at')[:5], many=True
            ).data
        }
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update training progress"""
        try:
            progress_record = self.get_object()
            new_progress = request.data.get('progress', progress_record.progress)
            
            progress_record.progress = min(100, max(0, new_progress))
            
            if progress_record.progress == 100 and not progress_record.completed:
                progress_record.completed = True
                progress_record.completed_at = timezone.now()
            
            progress_record.save()
            
            serializer = self.get_serializer(progress_record)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def start_module(self, request):
        """Start a new training module"""
        try:
            module_id = request.data.get('module_id')
            module = TrainingModule.objects.get(id=module_id, is_active=True)
            
            # Check if user already started this module
            progress, created = UserTrainingProgress.objects.get_or_create(
                user=request.user,
                module=module,
                defaults={'progress': 0}
            )
            
            serializer = self.get_serializer(progress)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            
        except TrainingModule.DoesNotExist:
            return Response({'error': 'Training module not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)