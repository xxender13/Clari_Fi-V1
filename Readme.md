# Clari-Fi: Product Image Analysis Tool

This project is designed to analyze product images by evaluating clarity, color contrast, and text formatting using Azure's OCR capabilities and custom contrast calculations. The app provides an in-depth analysis of text clarity, contrast ratios, and text case classification.

## Features

- **Clarity Level Detection**: Assesses the clarity of the uploaded image and classifies it as Clarity Level A, AA, or AAA.
- **Contrast Calculation**: Calculates the Advanced Perceptual Contrast Algorithm (APCA) contrast ratio between the text and background colors.
- **Text Case Classification**: Uses OCR to detect and classify text as Uppercase, Lowercase, or Mixture.

## Evaluation Rubric

| Criterion                | Description                                        |
|--------------------------|----------------------------------------------------|
| **Clarity Level A**      | Gaussian Blur with 35px radius                     |
| **Clarity Level AA**     | Gaussian Blur with 20px radius                     |
| **Clarity Level AAA**    | Gaussian Blur with 10px radius                     |
| **Text Classification**  | Uppercase, Lowercase, or Mixed                     |
| **APCA Contrast Level**  | Custom APCA contrast calculation between text and background |

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Azure Cognitive Services with Computer Vision API enabled
- Environment variables for `AZURE_SUBSCRIPTION_KEY` and `AZURE_ENDPOINT`

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/xxender13/Clari_Fi-V1.git
    cd Clari_Fi-V1
    ```

2. **Set up environment variables**:
    - Create a `.env` file with your Azure credentials:
      ```plaintext
      AZURE_SUBSCRIPTION_KEY="your_subscription_key"
      AZURE_ENDPOINT="your_endpoint_url"
      ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Streamlit app**:
    ```sh
    streamlit run Clari_fi_final.py
    ```

2. **Upload an image**:
    - Use the "Choose an image" button to upload a product image in JPG, JPEG, or PNG format.

3. **View the analysis**:
    - The app will display clarity level, contrast evaluation, and text classification details.

## Evaluation Process

### Clarity Level Detection

The app assesses image clarity by analyzing variance in pixel sharpness:
- **Clarity Level A**: 35px Gaussian blur radius
- **Clarity Level AA**: 20px Gaussian blur radius
- **Clarity Level AAA**: 10px Gaussian blur radius

### Contrast Evaluation

APCA contrast ratios between text and background colors are calculated, providing insights into readability:
- **High Contrast**: Values are optimized for readability.
- **Low Contrast**: Suggests potential readability issues.

### Text Case Classification

Using OCR, the app classifies text as:
- **Uppercase**
- **Lowercase**
- **Mixed**

The app also calculates the percentage of each case type in the detected text.

## Example Output

The application provides the following insights:
- **Clarity Level**: Displays the clarity level of the uploaded image.
- **Contrast Ratios**: Presents the APCA contrast ratios between text and background.
- **Text Classification**: Summarizes text case classification results.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## Contact

For questions or feedback, please contact **harshilsharma808@gmail.com**.
