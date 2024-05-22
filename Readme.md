# Product Image Evaluation

This project aims to evaluate the visual clarity, color contrast, and text formatting of product images. The evaluation process classifies images into three levels (A, AA, AAA) based on predefined metrics and provides insights into the quality of text formatting, specifically checking for uppercase text.

## Features

- **Clarity Visualization**: Applies Gaussian blur to the image to determine clarity levels.
- **Contrast Evaluation**: Calculates color contrast and classifies it into levels.
- **Text Classification**: Checks for the presence of uppercase text in the image.

## Rubric for Evaluation Metrics

| Metric          | Description                         |
|-----------------|-------------------------------------|
| Clarity Level A | Gaussian Blur with 10px radius      |
| Clarity Level AA| Gaussian Blur with 20px radius      |
| Clarity Level AAA| Gaussian Blur with 35px radius     |
| Contrast Level AAA | Contrast > 70 (Good)             |
| Contrast Level AA  | Contrast 51-70 (Good)            |
| Contrast Level A   | Contrast 31-50 (Not Good)        |

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Pip package manager

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/product-image-evaluation.git
    cd product-image-evaluation
    ```

2. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Streamlit app**:
    ```sh
    streamlit run app.py
    ```

2. **Upload an image**:
    - Click on the "Choose an image" button to upload a product image in jpg, jpeg, or png format.

3. **View the evaluation**:
    - The app will display the clarity visualization, contrast evaluation, and text classification results.

## Evaluation Process

### Clarity Visualization

The clarity of the image is visualized by applying Gaussian blur with different pixel radii:

- **Level A**: 10px radius
- **Level AA**: 20px radius
- **Level AAA**: 35px radius

The level with the smallest mean difference from the original image is selected as the clarity level.

### Contrast Evaluation

The color contrast of the image is calculated and classified into levels based on the standard deviation of the L channel in the LAB color space:

- **Level AAA**: Contrast > 70 (Good)
- **Level AA**: Contrast 51-70 (Good)
- **Level A**: Contrast 31-50 (Not Good)
- **Below A**: Contrast <= 30 (Not Good)

### Text Classification

The text extracted from the image using OCR is analyzed to check for uppercase text:

- If any word in the text is uppercase, an issue is flagged.
- If no text is found, an issue is flagged.

## Example Output

The application provides a visual and textual summary of the evaluation:

- **Clarity Visualization**: Displays the original and blurred images.
- **Clarity Level**: Indicates the clarity level based on the Gaussian blur analysis.
- **Contrast Evaluation**: Displays the contrast level and quality.
- **Text Classification**: Lists any issues found with the text formatting.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact [your-email@example.com].

