from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, filters
from .models import VFDModel, ErrorCode, Manual, FAQ
from .serializers import VFDModelSerializer, ErrorCodeSerializer, ManualSerializer, FAQSerializer

# Public Front-End Views

def index(request):
    """
    Homepage view with simultaneous search for Error Codes and FAQs.
    """
    query = request.GET.get('q', '')
    error_results = []
    faq_results = []
    manual_results = []
    
    if query:
        # Search Error Codes
        error_results = ErrorCode.objects.filter(
            Q(code__icontains=query) | 
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(vfd_model__series_name__icontains=query)
        )
        
        # Search FAQs
        faq_results = FAQ.objects.filter(
            Q(question__icontains=query) | 
            Q(answer__icontains=query) | 
            Q(tags__icontains=query)
        )
        
        # Search Manuals
        manual_results = Manual.objects.filter(
            Q(title__icontains=query) |
            Q(vfd_model__series_name__icontains=query)
        )

    context = {
        'query': query,
        'error_results': error_results,
        'faq_results': faq_results,
        'manual_results': manual_results,
    }
    return render(request, 'hub/index.html', context)

# API Views

class VFDModelViewSet(viewsets.ModelViewSet):
    queryset = VFDModel.objects.all()
    serializer_class = VFDModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['series_name', 'description']

class ErrorCodeViewSet(viewsets.ModelViewSet):
    queryset = ErrorCode.objects.all()
    serializer_class = ErrorCodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'description', 'vfd_model__series_name']

class ManualViewSet(viewsets.ModelViewSet):
    queryset = Manual.objects.all()
    serializer_class = ManualSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer', 'tags']
