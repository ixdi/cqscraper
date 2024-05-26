import requests
from PIL import Image
from io import BytesIO
import os
import fitz  # PyMuPDF
import validators


def process_image(image_url: str) -> str:
    """Fetches an image, converts it to PNG, and saves it as a thumbnail."""
    print(f"Processing image from {image_url}")
    if not validators.url(image_url):
        return ""

    response = requests.get(image_url)
    image_content = ""
    try:
        image_content = BytesIO(response.content)
    except Exception as e:
        print(f"Failed to process image {image_url}: {e}")

    image = Image.open(image_content)
    thumbnail = image.copy()
    thumbnail.thumbnail((100, 100))  # Adjust thumbnail size as needed

    os.makedirs("images", exist_ok=True)
    image_path = os.path.join(
        "images", f"{os.path.basename(image_url).split('.')[0]}.png"
    )
    thumbnail.save(image_path, format="PNG")

    return image_path


def extract_pdf_info(pdf_url: str) -> dict:
    """Extracts information from a PDF, especially the UN Number."""
    if not validators.url(pdf_url):
        return {}

    response = requests.get(pdf_url)
    pdf_content = BytesIO(response.content)
    document = fitz.open(stream=pdf_content, filetype="pdf")

    info = {}
    for page in document:
        text = page.get_text()
        if "14.1" in text:
            # Assuming UN Number follows "14.1" in the text
            un_number = text.split("14.1")[1].split(":")[1]
            info["UN Number"] = un_number
            break

    return info
