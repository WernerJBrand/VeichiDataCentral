from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vfds', views.VFDModelViewSet)
router.register(r'errors', views.ErrorCodeViewSet)
router.register(r'manuals', views.ManualViewSet)
router.register(r'faqs', views.FAQViewSet)

urlpatterns = [
    # Public Front-End
    path('', views.index, name='index'),
    
    # API
    path('api/', include(router.urls)),
]
