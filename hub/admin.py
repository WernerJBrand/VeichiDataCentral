from django.contrib import admin
from .models import VFDModel, ErrorCode, Manual, FAQ

@admin.register(VFDModel)
class VFDModelAdmin(admin.ModelAdmin):
    list_display = ('series_name', 'power_rating')
    search_fields = ('series_name', 'description')

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'vfd_model', 'firmware_version')
    list_filter = ('vfd_model',)
    search_fields = ('code', 'name', 'description')

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('title', 'vfd_model', 'uploaded_at')
    list_filter = ('vfd_model',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'tags')
    search_fields = ('question', 'answer', 'tags')
