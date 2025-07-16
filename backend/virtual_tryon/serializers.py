from rest_framework import serializers
from .models import TryOnSession, ClothingItem

class TryOnSessionSerializer(serializers.ModelSerializer):
    original_photo_url = serializers.SerializerMethodField()
    result_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TryOnSession
        fields = [
            'id', 'selected_clothing', 'created_at', 
            'processed_at', 'status', 'original_photo_url', 
            'result_photo_url'
        ]
    
    def get_original_photo_url(self, obj):
        if obj.original_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.original_photo.url)
        return None
    
    def get_result_photo_url(self, obj):
        if obj.result_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.result_photo.url)
        return None

class ClothingItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ClothingItem
        fields = ['id', 'name', 'type', 'price', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
