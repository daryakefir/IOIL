from rest_framework import serializers
from .models import Well, FallRate, WaterCutCatalog


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'

