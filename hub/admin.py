from django.contrib import admin
from .models import VFDModel, ErrorCode, Manual, FAQ, Question, Answer

@admin.register(VFDModel)
class VFDModelAdmin(admin.ModelAdmin):
    list_display = ('series_name', 'power_rating')

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'vfd_model')
    list_filter = ('vfd_model',)
    search_fields = ('code', 'name')

@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('title', 'vfd_model', 'uploaded_at', 'has_ocr_content')
    list_filter = ('vfd_model',)
    # readonly_fields = ('content_text', 'tags') # Removed to allow manual editing

    def has_ocr_content(self, obj):
        return bool(obj.content_text)
    has_ocr_content.boolean = True
    has_ocr_content.short_description = "OCR Text?"

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'related_vfd')
    list_filter = ('category', 'related_vfd')

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['approve_questions']
    inlines = [AnswerInline]

    def approve_questions(self, request, queryset):
        queryset.update(status='approved')
    approve_questions.short_description = "Approve selected questions"
