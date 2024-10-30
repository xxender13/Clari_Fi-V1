import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import cv2
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import os
from dotenv import load_dotenv
load_dotenv()  # This loads environment variables from a .env file


# Set up Azure Computer Vision
subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# APCA contrast calculation functions
def linearize(val):
    return (val / 255.0) ** 2.4


def clamp_luminance(luminance):
    blkThrs = 0.022
    blkClmp = 1.414
    if luminance > blkThrs:
        return luminance
    return ((blkThrs - luminance) ** blkClmp) + luminance


def get_luminance(color):
    red, green, blue = color
    y = 0.2126 * linearize(red) + 0.7152 * linearize(green) + 0.0722 * linearize(blue)
    return clamp_luminance(y)


def get_contrast(background, foreground):
    deltaYmin = 0.0005
    scale = 1.14
    background_luminance = get_luminance(background)
    foreground_luminance = get_luminance(foreground)
    if abs(background_luminance - foreground_luminance) < deltaYmin:
        return 0.0
    if background_luminance > foreground_luminance:
        return (background_luminance ** 0.56 - foreground_luminance ** 0.57) * scale
    return (background_luminance ** 0.65 - foreground_luminance ** 0.62) * scale


def get_apca_contrast(background, foreground):
    contrast = get_contrast(background, foreground)
    if abs(contrast) < 0.1:
        return "contrast too low"
    if contrast > 0:
        return (contrast - 0.027) * 100
    else:
        return (contrast + 0.027) * 100


def analyze_image_with_azure(image_path):
    with open(image_path, "rb") as image_stream:
        read_response = computervision_client.read_in_stream(image_stream, raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)

    text_results = []
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                for word in line.words:
                    text_results.append((word.text, word.bounding_box))

    return text_results


def get_average_color(image, bounding_box):
    x1, y1, x2, y2, x3, y3, x4, y4 = bounding_box
    x, y, w, h = int(x1), int(y1), int(x3 - x1), int(y3 - y1)

    # Define a small padding around the text to average color
    padding = 3
    text_area = image[y + padding: y + h - padding, x + padding: x + w - padding]

    mean_color = cv2.mean(text_area)[:3]  # Get the mean color (BGR)
    return (int(mean_color[2]), int(mean_color[1]), int(mean_color[0]))  # Convert to RGB


def analyze_image(image):
    image_path = 'temp_image.jpg'
    image.save(image_path)
    text_results = analyze_image_with_azure(image_path)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

    results = []
    text_case_counts = {"Uppercase": 0, "Lowercase": 0, "Mixture": 0}
    for text, bounding_box in text_results:
        text_color = get_average_color(image_rgb, bounding_box)

        # Adjust background area dynamically
        x1, y1, x2, y2, x3, y3, x4, y4 = bounding_box
        x, y, w, h = int(x1), int(y1), int(x3 - x1), int(y3 - y1)

        padding = 5
        background_area = image_rgb[max(y - padding, 0):y, x:x + w]
        if background_area.size == 0:
            background_area = image_rgb[y + h:min(y + h + padding, image_rgb.shape[0]), x:x + w]

        mean_red = np.mean(background_area[:, :, 0])
        mean_green = np.mean(background_area[:, :, 1])
        mean_blue = np.mean(background_area[:, :, 2])
        background_color = (int(mean_red), int(mean_green), int(mean_blue))

        contrast_ratio = get_apca_contrast(background_color, text_color)

        text_case = classify_text(text)
        text_case_counts[text_case] += 1

        results.append((text, text_case, text_color, background_color, contrast_ratio))

    total_texts = sum(text_case_counts.values())
    text_case_percentages = {k: (v / total_texts) * 100 for k, v in text_case_counts.items()}

    return results, text_case_percentages


def determine_clarity_level(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    if variance < 100:
        return "Clarity Level A"
    elif variance < 500:
        return "Clarity Level AA"
    else:
        return "Clarity Level AAA"


def classify_text(text):
    if text.isupper():
        return "Uppercase"
    elif text.islower():
        return "Lowercase"
    else:
        return "Mixture"


def detect_objects(image_path):
    with open(image_path, "rb") as image_file:
        return computervision_client.detect_objects_in_stream(image_file).objects


st.title("Product Image Analysis")

st.markdown("""
### Evaluation Rubric

| Criterion               | Description                                      |
|-------------------------|--------------------------------------------------|
| **Clarity Level AAA**     | Gaussian Blur with 10px radius                   |
| **Clarity Level AA**    | Gaussian Blur with 20px radius                   |
| **Clarity Level A**   | Gaussian Blur with 35px radius                   |
| **Text Classification** | Uppercase, Lowercase, or Mixture of both         |
""")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        image_path = "uploaded_image.jpg"
        image.save(image_path)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        clarity_level = determine_clarity_level(image)
        st.write(f"Determined Clarity Level: {clarity_level}")

        objects = detect_objects(image_path)

        with open(image_path, "rb") as image_file:
            ocr_results = computervision_client.read_in_stream(image_file, raw=True)
        operation_id = ocr_results.headers["Operation-Location"].split("/")[-1]

        while True:
            ocr_results = computervision_client.get_read_result(operation_id)
            if ocr_results.status not in ['notStarted', 'running']:
                break

        text_boxes = []
        all_text = ""
        if ocr_results.status == OperationStatusCodes.succeeded:
            for text_result in ocr_results.analyze_result.read_results:
                for line in text_result.lines:
                    all_text += " " + line.text
                    bbox = line.bounding_box
                    text_boxes.append((bbox[0], bbox[1], bbox[4], bbox[5]))

        text_classification = classify_text(all_text)

        draw = ImageDraw.Draw(image)
        for obj in objects:
            rect = obj.rectangle
            try:
                draw.rectangle((rect.x, rect.y, rect.x + rect.w, rect.y + rect.h), outline="red", width=3)
            except Exception as e:
                st.write(f"Error drawing object rectangle: {e}")

        for box in text_boxes:
            try:
                draw.rectangle(box, outline="blue", width=2)
            except Exception as e:
                st.write(f"Error drawing text rectangle: {e}")

        st.image(image, caption='Annotated Product Image', use_column_width=True)
        st.write(f"Text Classification: {text_classification}")

        results, text_case_percentages = analyze_image(image)

        for word, text_case, text_color, background_color, contrast_ratio in results:
            st.write(f"**Word:** {word}")
            st.write(f"**Text Case:** {text_case}")
            st.write(f"**Text Color:** {text_color}")
            st.write(f"**Background Color:** {background_color}")
            st.write(f"**APCA Contrast Ratio:** {contrast_ratio}")
            st.write("---")

        st.write("### Text Case Percentages")
        st.write(f"**Uppercase:** {text_case_percentages['Uppercase']:.2f}%")
        st.write(f"**Lowercase:** {text_case_percentages['Lowercase']:.2f}%")
        st.write(f"**Mixture:** {text_case_percentages['Mixture']:.2f}%")

    except Exception as e:
        st.error(f"An error occurred: {e}")

