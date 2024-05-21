import cv2
import matplotlib.pyplot as plt
import gradio as gr
import numpy as np
import streamlit as st
import tempfile
import os

def apply_gaussian_blur(image, radius):
    # Apply Gaussian blur with the specified radius
    blurred = cv2.GaussianBlur(image, (radius * 2 + 1, radius * 2 + 1), 0)
    return blurred

def process_image(image):
    # Convert the image to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get image dimensions
    height, width, _ = image_rgb.shape

    # Apply Gaussian blur for A, AA, and AAA standards
    blurred_a = apply_gaussian_blur(image_rgb, 10)
    blurred_aa = apply_gaussian_blur(image_rgb, 20)
    blurred_aaa = apply_gaussian_blur(image_rgb, 35)

    # Plot images
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    axs[0].imshow(image_rgb)
    axs[0].set_title('Original Image\n{}x{}'.format(width, height))
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

    # Save plot to a file
    tmpdir = tempfile.mkdtemp()
    tmpfile = os.path.join(tmpdir, 'visual_clarity_output.png')
    fig.savefig(tmpfile)
    plt.close(fig)

    return tmpfile, blurred_a, blurred_aa, blurred_aaa

def process_input(input):
    if isinstance(input, np.ndarray):
        return process_image(input)
    else:
        return "Please upload an image"

# Create Gradio interface
interface = gr.Interface(
    fn=process_input,
    inputs=gr.inputs.Image(label="Upload an image"),
    outputs=[
        gr.outputs.Image(label="Visual Clarity Check Output (Image)"),
        gr.outputs.File(label="Download Blurred Image (Level A)"),
        gr.outputs.File(label="Download Blurred Image (Level AA)"),
        gr.outputs.File(label="Download Blurred Image (Level AAA)")
    ],
    title="Visual Clarity Check"
)
# Create Streamlit app
def app():
    st.title("Visual Clarity Check")
    st.markdown("Upload an image to check its visual clarity.")

    with st.spinner('Loading...'):
        gr.Interface(fn=process_input, inputs=gr.inputs.Image(label="Upload an image"), outputs="text").launch(share=True)

if __name__ == "__main__":
    app()
