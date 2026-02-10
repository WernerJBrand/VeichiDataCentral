from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from .models import VFDModel, ErrorCode, Manual, FAQ, Question, Answer
from .serializers import VFDModelSerializer, ErrorCodeSerializer, ManualSerializer, FAQSerializer, QuestionSerializer, AnswerSerializer
from .utils import get_rag_answer

# Public Front-End Views

def index(request):
    """
    Homepage view with simultaneous search for Error Codes, FAQs, Manuals (content), and Questions.
    Includes AI RAG Stub.
    """
    query = request.GET.get('q', '')
    error_results = []
    faq_results = []
    manual_results = []
    question_results = []
    ai_answer = ""
    
    if query:
        # Search Error Codes
        error_results = ErrorCode.objects.filter(
            Q(code__icontains=query) | 
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(vfd_model__series_name__icontains=query)
        ).distinct()
        
        # Search FAQs
        faq_results = FAQ.objects.filter(
            Q(question__icontains=query) | 
            Q(answer__icontains=query) | 
            Q(tags__icontains=query)
        ).distinct()
        
        # Search Manuals (Title + Content + Tags)
        manual_results = Manual.objects.filter(
            Q(title__icontains=query) |
            Q(vfd_model__series_name__icontains=query) |
            Q(content_text__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()

        # Search Community Questions
        question_results = Question.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(answers__content__icontains=query)
        ).distinct()

        # AI RAG Generation (Stub)
        # Gather some context from manual results to pretend we are using RAG
        context_text = ""
        for m in manual_results[:1]:
             context_text += m.content_text[:500] + "..."
        
        if query:
            ai_answer = get_rag_answer(query, context_text)

    # Smart Search Suggestions
    # If the user searches for a Series Name (e.g. "Multiflow"), suggest refined searches.
    suggestions = []
    if query:
        # Check if query matches a VFD Model
        matched_vfd = VFDModel.objects.filter(series_name__icontains=query).first()
        if matched_vfd:
            base_name = matched_vfd.series_name
            suggestions = [
                {'label': f"{base_name} Errors", 'url': f"/errors/?search={base_name}"},
                {'label': f"{base_name} Manuals", 'url': f"/manuals/?search={base_name}"},
                {'label': f"{base_name} FAQs", 'url': f"/faqs/?search={base_name}"},
                {'label': f"Ask about {base_name}", 'url': f"/questions/ask/?vfd={matched_vfd.id}"},
            ]

    context = {
        'query': query,
        'error_results': error_results,
        'faq_results': faq_results,
        'manual_results': manual_results,
        'question_results': question_results,
        'ai_answer': ai_answer,
        'suggestions': suggestions,
    }
    return render(request, 'hub/index.html', context)

def error_list(request):
    """
    List all error codes, with optional filtering.
    """
    search_query = request.GET.get('search', '')
    errors = ErrorCode.objects.all().select_related('vfd_model')
    
    if search_query:
        errors = errors.filter(
            Q(code__icontains=search_query) | 
            Q(name__icontains=search_query) |
            Q(vfd_model__series_name__icontains=search_query)
        )
        
    context = {'errors': errors, 'search_query': search_query}
    return render(request, 'hub/error_list.html', context)

def manual_list(request):
    """
    List all manuals.
    """
    search_query = request.GET.get('search', '')
    manuals = Manual.objects.all().select_related('vfd_model')
    
    if search_query:
        manuals = manuals.filter(
            Q(title__icontains=search_query) |
            Q(vfd_model__series_name__icontains=search_query) | 
            Q(tags__icontains=search_query)
        )

    context = {'manuals': manuals, 'search_query': search_query}
    return render(request, 'hub/manual_list.html', context)

def faq_list(request):
    """
    List all FAQs.
    """
    search_query = request.GET.get('search', '')
    faqs = FAQ.objects.all().select_related('related_vfd')
    
    if search_query:
        faqs = faqs.filter(
            Q(question__icontains=search_query) |
            Q(answer__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(related_vfd__series_name__icontains=search_query)
        )

    context = {'faqs': faqs, 'search_query': search_query}
    return render(request, 'hub/faq_list.html', context)

# Forum / Q&A Views

def question_list(request):
    """
    Community Q&A Feed.
    Shows only approved questions for normal users.
    Staff/Admins see all (with status indicator).
    """
    if request.user.is_staff:
        questions = Question.objects.all().order_by('-created_at').select_related('user', 'related_vfd')
    else:
        questions = Question.objects.filter(status='approved').order_by('-created_at').select_related('user', 'related_vfd')
        
    return render(request, 'hub/question_list.html', {'questions': questions})

def question_detail(request, pk):
    """
    View a specific question and its answers.
    """
    question = get_object_or_404(Question, pk=pk)
    
    # Restrict access to non-approved questions for non-staff
    if question.status != 'approved' and not request.user.is_staff and question.user != request.user:
        return render(request, 'hub/base.html', {'message': "This question is pending review."}, status=403)
    
    if request.method == 'POST' and request.user.is_authenticated:
        # Handle "Approve" action by staff
        if 'approve' in request.POST and request.user.is_staff:
            question.status = 'approved'
            question.save()
            return redirect('question_detail', pk=pk)
            
        # Handle new Answer
        content = request.POST.get('content')
        if content:
            Answer.objects.create(question=question, content=content, user=request.user)
            # If staff answers a pending question, auto-approve it? 
            # User requested: "when an agent comments on it in the backend it will go live"
            if request.user.is_staff and question.status == 'pending':
                question.status = 'approved'
                question.save()
            return redirect('question_detail', pk=pk)

    return render(request, 'hub/question_detail.html', {'question': question})

@login_required
def ask_question(request):
    """
    Post a new question.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # vfd_id = request.POST.get('vfd_id') # Optional
        
        if title and content:
            Question.objects.create(title=title, content=content, user=request.user, status='pending')
            # Redirect to a success/info page or back to list with a message
            return render(request, 'hub/question_pending.html')
            
    vfds = VFDModel.objects.all()
    return render(request, 'hub/ask_question.html', {'vfds': vfds})

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content_text', 'tags']

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['question', 'answer', 'tags', 'category']

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
