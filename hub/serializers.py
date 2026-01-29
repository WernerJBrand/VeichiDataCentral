from rest_framework import serializers
from .models import VFDModel, ErrorCode, Manual, FAQ

class VFDModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VFDModel
        fields = '__all__'

class ErrorCodeSerializer(serializers.ModelSerializer):
    vfd_series = serializers.CharField(source='vfd_model.series_name', read_only=True)
    class Meta:
        model = ErrorCode
        fields = '__all__'

class ManualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manual
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
