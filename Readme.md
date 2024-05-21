# Description:
This code is a web application that allows users to upload an image or video file and perform visual clarity checks on it. The application applies different levels of Gaussian blurring (Level A, Level AA, and Level AAA) to simulate the challenges of viewing visual elements on a mobile device.
The application has two main functionalities:

### Image Processing:

The user uploads an image file.
The application converts the image to RGB format and applies Gaussian blurring at three different levels (10px, 20px, and 35px radius).
The original image and the blurred versions are displayed side by side, showing the effect of blurring on visual clarity.
The processed image is saved as a PNG file.


### Video Processing:

The user uploads a video file.
The application reads the video frames, applies Gaussian blurring at three different levels (10px, 20px, and 35px radius) to each frame.
Three separate video files are generated, one for each level of blurring (Level A, Level AA, and Level AAA).
The user can download these blurred video files.



### The application is built using several libraries:

OpenCV: For image and video processing operations, including Gaussian blurring.
Matplotlib: For plotting and visualizing the original and blurred images.
Gradio: For creating the user interface and handling file inputs and outputs.
Streamlit: For hosting the Gradio interface in a web application.

The application is designed to help developers and designers assess the visual clarity and perceptibility of graphical elements in mobile applications and websites by simulating real-world mobile viewing conditions.