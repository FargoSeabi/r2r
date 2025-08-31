from rest_framework import serializers
from .models import Village, AIStory


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'


class AIStorySerializer(serializers.ModelSerializer):
    village_name = serializers.CharField(source='village.name', read_only=True)
    
    class Meta:
        model = AIStory
        fields = '__all__'