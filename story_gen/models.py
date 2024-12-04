from django.db import models


class AssetUpload(models.Model):
    uploaded_image = models.ImageField(upload_to='uploaded_images/')
    image_caption = models.CharField(max_length=300, blank=True, null=True)
    story_text = models.TextField(blank=True, null=True)
    story_audio = models.FileField(
        upload_to='audio_files', blank=True, null=True)

