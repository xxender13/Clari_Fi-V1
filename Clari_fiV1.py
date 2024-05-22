import cv2
import easyocr
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def apply_gaussian_blur(image, radius):
    return cv2.GaussianBlur(image, (radius * 2 + 1, radius * 2 + 1), 0)


def visualize_clarity(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    blurred_a = apply_gaussian_blur(image_rgb, 10)
    blurred_aa = apply_gaussian_blur(image_rgb, 20)
    blurred_aaa = apply_gaussian_blur(image_rgb, 35)

    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    axs[0].imshow(image_rgb)
    axs[0].set_title('Original Image')
    axs[0].axis('off')
    axs[1].imshow(blurred_a)
    axs[1].set_title('Blurred Image (10px radius)\nLevel A')
    axs[1].axis('off')
    axs[2].imshow(blurred_aa)
    axs[2].set_title('Blurred Image (20px radius)\nLevel AA')
    axs[2].axis('off')
    axs[3].imshow(blurred_aaa)
    axs[3].set_title('Blurred Image (35px radius)\nLevel AAA')
    axs[3].axis('off')
    st.pyplot(fig)
    plt.close(fig)

    # Determine clarity level based on Gaussian blur
    clarity_levels = ["Level A", "Level AA", "Level AAA"]
    clarity_values = [blurred_a, blurred_aa, blurred_aaa]
    clarity_diffs = [np.mean(cv2.absdiff(image_rgb, img)) for img in clarity_values]
    min_diff = min(clarity_diffs)
    clarity_index = clarity_diffs.index(min_diff)
    clarity_level = clarity_levels[clarity_index]

    return clarity_level


def calculate_color_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    contrast = l_channel.std()
    return contrast


def evaluate_contrast(image):
    color_contrast = calculate_color_contrast(image)

    if color_contrast > 70:
        contrast_level = 'AAA'
        contrast_quality = 'Good'
    elif color_contrast > 50:
        contrast_level = 'AA'
        contrast_quality = 'Good'
    elif color_contrast > 30:
        contrast_level = 'A'
        contrast_quality = 'Not Good'
    else:
        contrast_level = 'Below A'
        contrast_quality = 'Not Good'

    return contrast_level, contrast_quality


def text_classification(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    text = " ".join([res[1] for res in result])
    issues = []

    if not text:
        issues.append("No text found in the image.")
        return issues

    if any(word.isupper() for word in text.split()):
        issues.append("Text is in uppercase.")
    else:
        issues.append("No uppercase text found.")


    return issues


def main():
    st.title("Product Image Evaluation")

    st.subheader("Rubric for Evaluation Metrics")
    # Define the rubric for evaluation metrics
    rubric_data = {
        'Metric': ['Clarity Level A', 'Clarity Level AA', 'Clarity Level AAA', 'Contrast Level AAA', 'Contrast Level AA', 'Contrast Level A'],
        'Description': [
            'Gaussian Blur with 10px radius',
            'Gaussian Blur with 20px radius',
            'Gaussian Blur with 35px radius',
            'Contrast > 70 (Good)',
            'Contrast 51-70 (Good)',
            'Contrast 31-50 (Not Good)'
        ]
    }
    rubric_df = pd.DataFrame(rubric_data)
    st.table(rubric_df)

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        st.subheader("Clarity Visualization")
        clarity_level = visualize_clarity(image)
        st.write(f"Clarity Level: {clarity_level}")

        st.subheader("Contrast Evaluation")
        contrast_level, contrast_quality = evaluate_contrast(image)
        st.write(f"Contrast Level: {contrast_level}")
        st.write(f"Contrast Quality: {contrast_quality}")



        st.subheader("Text Classification")
        text_issues = text_classification(image)
        if text_issues:
            for issue in text_issues:
                st.write(issue)
        else:
            st.write("No text issues found.")


if __name__ == "__main__":
    main()
