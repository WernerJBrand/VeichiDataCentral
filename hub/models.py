from django.db import models

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

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    tags = models.CharField(max_length=200, help_text="Comma-separated tags e.g. installation, wiring")
    related_vfd = models.ForeignKey(VFDModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')

    def __str__(self):
        return self.question
