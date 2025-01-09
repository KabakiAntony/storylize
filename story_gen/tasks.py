import os
from PIL import Image
from celery import shared_task, chain
from transformers import (
    AutoProcessor,
    AutoModelForImageTextToText,
    AutoTokenizer,
    AutoModelForCausalLM
    )
import outetts
from storylize.settings import MEDIA_ROOT


@shared_task(name="generate caption")
def generate_caption(image_name):
    processor = AutoProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-large")
    model = AutoModelForImageTextToText.from_pretrained(
        "Salesforce/blip-image-captioning-large")

    image_path = os.path.join(MEDIA_ROOT, image_name)
    image = Image.open(image_path)

    inputs = processor(images=image, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50, min_length=10)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption


@shared_task(name="generate text story")
def generate_text_story(caption):
    tokenizer = AutoTokenizer.from_pretrained("distilbert/distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilbert/distilgpt2")

    input_text = caption
    inputs = tokenizer(input_text, return_tensors="pt")
    output = model.generate(
        **inputs,  max_length=350, min_length=150, top_k=40,
        repetition_penalty=1.1,  top_p=0.9, temperature=0.6,
        do_sample=True)
    story = tokenizer.decode(output[0], skip_special_tokens=True)
    return story


@shared_task
def generate_audio_story(text_story):
    model_config = outetts.HFModelConfig_v1(
        model_path="OuteAI/OuteTTS-0.2-500M",
        language="en",
    )
    interface = outetts.InterfaceHF(model_version="0.2", cfg=model_config)

    speaker = interface.load_default_speaker(name="male_1")
    output = interface.generate(
        text=text_story,
        temperature=0.1,
        repetition_penalty=1.1,
        max_length=4096,
        speaker=speaker,
    )

    output_path = "output.wav"
    output.save(output_path)
    
    # Return the path to the saved file
    return output_path


def process_image(image_name):
    task_chain = chain(
        generate_caption.s(image_name),
        generate_text_story.s(),
        generate_audio_story.s(),
    )
    task_chain.apply_async()
