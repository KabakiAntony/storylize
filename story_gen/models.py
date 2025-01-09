from django.db import models


class AssetUpload(models.Model):
    uploaded_image = models.ImageField(upload_to='uploaded_images/')
    caption = models.TextField(blank=True, null=True)
    text_story = models.TextField(blank=True, null=True)
    audio_story = models.FileField(
        upload_to='audio_files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="PENDING")