from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vfds', views.VFDModelViewSet)
router.register(r'errors', views.ErrorCodeViewSet)
router.register(r'manuals', views.ManualViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    # Public Front-End
    path('', views.index, name='index'),
    path('errors/', views.error_list, name='error_list'),
    path('manuals/', views.manual_list, name='manual_list'),
    path('faqs/', views.faq_list, name='faq_list'),
    
    # Forum
    path('questions/', views.question_list, name='question_list'),
    path('questions/ask/', views.ask_question, name='ask_question'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    
    # API
    path('api/', include(router.urls)),
]
