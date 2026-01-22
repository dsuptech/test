import sys
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def explain_image(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    inputs = processor(image, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python explain_image.py <image_path>")
    else:
        explain_image(sys.argv[1])
