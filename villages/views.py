from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Village, AIStory
from .serializers import VillageSerializer, AIStorySerializer
import openai
from django.conf import settings


class VillageViewSet(viewsets.ModelViewSet):
    queryset = Village.objects.filter(is_active=True)
    serializer_class = VillageSerializer
    
    def get_queryset(self):
        queryset = Village.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        country = self.request.query_params.get('country')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if country:
            queryset = queryset.filter(country=country)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(region__icontains=search)
            )
        
        return queryset.order_by('-rating', '-visit_count')
    
    @action(detail=True, methods=['post'])
    def visit(self, request, pk=None):
        """Track village visit"""
        village = self.get_object()
        village.visit_count += 1
        village.save()
        return Response({'message': 'Visit recorded', 'visit_count': village.visit_count})


class AIStoryViewSet(viewsets.ModelViewSet):
    queryset = AIStory.objects.all()
    serializer_class = AIStorySerializer
    
    def get_queryset(self):
        queryset = AIStory.objects.all()
        village_id = self.request.query_params.get('village_id')
        category = self.request.query_params.get('category')
        
        if village_id:
            queryset = queryset.filter(village_id=village_id)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('-generated_at')
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
    
    @action(detail=False, methods=['post'])
    def generate_story(self, request):
        """Generate AI story for a village"""
        village_id = request.data.get('village_id')
        interests = request.data.get('interests', [])
        category = request.data.get('category', 'cultural')
        
        try:
            village = Village.objects.get(id=village_id)
        except Village.DoesNotExist:
            return Response({'error': 'Village not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate story using OpenAI
        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            prompt = f"""
            Create a {category} story about {village.name} in {village.region}, {village.country}.
            The village is known for {village.category} and {village.description}.
            
            User interests: {', '.join(interests) if interests else 'general cultural exploration'}
            
            Write an engaging 200-300 word story that captures the essence of this South African tribal village,
            incorporating traditional elements, cultural practices, and the village's specialties.
            Focus on authentic cultural details and Ubuntu principles.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a cultural storyteller specializing in South African tribal heritage and traditions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            story_content = response.choices[0].message.content
            
            # Save the story
            story = AIStory.objects.create(
                village=village,
                user=request.user if request.user.is_authenticated else None,
                title=f"Tales from {village.name}",
                content=story_content,
                category=category,
                personalized_for=interests
            )
            
            serializer = AIStorySerializer(story)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)