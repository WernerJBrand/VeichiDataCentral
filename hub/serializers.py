from rest_framework import serializers
from .models import VFDModel, ErrorCode, Manual, FAQ, Question, Answer

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

class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = '__all__'
