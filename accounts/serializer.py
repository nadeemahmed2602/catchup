# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser,Image,Interest

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    image=ImageSerializer(many=True)
    interest=InterestSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
