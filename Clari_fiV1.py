import cv2
import matplotlib.pyplot as plt
import gradio as gr
import numpy as np
import streamlit as st

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
    fig.savefig('visual_clarity_output.png')
    plt.close(fig)

    return 'visual_clarity_output.png', blurred_a, blurred_aa, blurred_aaa

def process_video(input_video_path):
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter objects for each level of blurring
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_a = cv2.VideoWriter('output_a.avi', fourcc, fps, (width, height))
    out_aa = cv2.VideoWriter('output_aa.avi', fourcc, fps, (width, height))
    out_aaa = cv2.VideoWriter('output_aaa.avi', fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply Gaussian blur for A, AA, and AAA standards
        blurred_a = apply_gaussian_blur(frame, 10)
        blurred_aa = apply_gaussian_blur(frame, 20)
        blurred_aaa = apply_gaussian_blur(frame, 35)

        # Write the frames to the output video files
        out_a.write(blurred_a)
        out_aa.write(blurred_aa)
        out_aaa.write(blurred_aaa)

    # Release everything if job is finished
    cap.release()
    out_a.release()
    out_aa.release()
    out_aaa.release()

    return 'visual_clarity_output.png', 'output_a.avi', 'output_aa.avi', 'output_aaa.avi'

def process_input(input):
    if isinstance(input, np.ndarray):
        return process_image(input)
    else:
        return process_video(input.name)

# Create Gradio interface
interface = gr.Interface(
    fn=process_input,
    inputs=gr.File(label="Upload an image or video", file_types=["image", "video"]),
    outputs=[
        gr.Image(type="filepath", label="Visual Clarity Check Output (Image)"),
        gr.File(label="Download Blurred Video (Level A)"),
        gr.File(label="Download Blurred Video (Level AA)"),
        gr.File(label="Download Blurred Video (Level AAA)")
    ]
)

# Create Streamlit app
def app():
    st.title("Visual Clarity Check")
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                input_file = gr.File(label="Upload an image or video", file_types=["image", "video"])
            with gr.Column():
                output_image = gr.Image(type="filepath", label="Visual Clarity Check Output (Image)")
                output_video_a = gr.File(label="Download Blurred Video (Level A)")
                output_video_aa = gr.File(label="Download Blurred Video (Level AA)")
                output_video_aaa = gr.File(label="Download Blurred Video (Level AAA)")

        interface(
            fn=process_input,
            inputs=input_file,
            outputs=[output_image, output_video_a, output_video_aa, output_video_aaa]
        )

if __name__ == "__main__":
    app()