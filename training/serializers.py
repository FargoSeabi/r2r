from rest_framework import serializers
from .models import TrainingModule, UserTrainingProgress


class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingModule
        fields = '__all__'


class UserTrainingProgressSerializer(serializers.ModelSerializer):
    module = TrainingModuleSerializer(read_only=True)
    module_id = serializers.UUIDField(write_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserTrainingProgress
        fields = '__all__'
        read_only_fields = ['user']