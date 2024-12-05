from django import forms
from .models import AssetUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = AssetUpload
        fields = ['uploaded_image']
