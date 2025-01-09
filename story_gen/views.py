from django.shortcuts import render
from .forms import ImageUploadForm
from .tasks import process_image


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            image_name = img_obj.uploaded_image.name
            process_image(image_name)
            return render(
                request, 'story_gen/result.html', {"img_obj": img_obj})
    else:
        form = ImageUploadForm()
    return render(request, 'story_gen/upload_form.html', {"form": form})
