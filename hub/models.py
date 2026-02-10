from django.db import models
from django.contrib.auth.models import User
from .utils import extract_text_from_pdf, get_ai_tags

class VFDModel(models.Model):
    series_name = models.CharField(max_length=100, help_text="e.g. AC310, AC10")
    power_rating = models.CharField(max_length=100, help_text="e.g. 0.75kW - 75kW")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.series_name} ({self.power_rating})"

class ErrorCode(models.Model):
    vfd_model = models.ForeignKey(VFDModel, on_delete=models.CASCADE, related_name='error_codes')
    code = models.CharField(max_length=50, help_text="e.g. E-01")
    name = models.CharField(max_length=200, help_text="e.g. Overcurrent")
    description = models.TextField()
    troubleshooting_steps = models.TextField()
    firmware_version = models.CharField(max_length=50, blank=True, help_text="Related Firmware Version")

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.vfd_model.series_name})"

class Manual(models.Model):
    vfd_model = models.ForeignKey(VFDModel, on_delete=models.CASCADE, related_name='manuals')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='manuals/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_text = models.TextField(blank=True, help_text="Extracted text from PDF for search.")
    tags = models.CharField(max_length=500, blank=True, help_text="AI generated tags.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.file:
            from django.db import transaction
            # Schedule OCR to run AFTER the transaction is committed.
            # This prevents the long-running OCR process from holding the SQLite database lock.
            transaction.on_commit(self._perform_ocr_extraction)

    def _perform_ocr_extraction(self):
        """
        Helper method to perform blocking OCR and update the record without locking the DB for too long.
        """
        try:
            if hasattr(self.file, 'path'):
                file_source = self.file.path
            else:
                return

            text = extract_text_from_pdf(file_source)
            tags = get_ai_tags(text)
            
            # Use .update() to avoid re-triggering save() and to keep the DB interaction brief.
            Manual.objects.filter(pk=self.pk).update(content_text=text, tags=tags)
            
            # Auto-generate FAQs extraction removed as per requirements.


        except Exception as e:
            print(f"Error processing PDF in background task: {e}")

    def __str__(self):
        return self.title

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Installation', 'Installation'),
        ('Troubleshooting', 'Troubleshooting'),
        ('Programming', 'Programming'),
    ]
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    tags = models.CharField(max_length=200, help_text="Comma-separated tags e.g. installation, wiring")
    related_vfd = models.ForeignKey(VFDModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')

    def __str__(self):
        return self.question

class Question(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    related_vfd = models.ForeignKey(VFDModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.user.username}"
