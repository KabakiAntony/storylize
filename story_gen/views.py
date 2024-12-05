from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import AssetUpload


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            # generate_caption(img_obj.uploaded_image.url)
            return render(
                request, 'story_gen/result.html', {"img_obj": img_obj})
    else:
        form = ImageUploadForm()
    return render(request, 'story_gen/upload_form.html', {"form": form})


def generate_caption(url):
    """
    this is going to be a celery task calling the 
    inference api to generate a caption for the 
    uploaded image
    """
    pass