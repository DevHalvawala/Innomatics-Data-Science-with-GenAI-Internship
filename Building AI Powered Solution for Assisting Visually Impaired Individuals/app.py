import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import pytesseract
import os
import time

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyA1BJNBrkyLrGiLJoSlN40e1gUmscmwduhjb") #PASTE YOUR OWN API

# Streamlit App
st.title("AI-Powered Assistive Tool")

project_description = """
# Project Description

This AI-Powered Assistive Tool uses advanced image processing and text-to-speech technologies to enhance accessibility for individuals with visual impairments.

### Key Features:
1. **Real-Time Scene Understanding**:
   - The tool leverages Google's Gemini model to generate textual descriptions of uploaded images. This allows users to understand the context and content of images through natural language descriptions.

2. **Text-to-Speech Conversion for Visual Content**:
   - This feature extracts text from images using OCR (Optical Character Recognition). The extracted text is then converted to audible speech, providing an efficient way for users to access written content from images.

The application is powered by Google's **Generative AI**, **Tesseract OCR**, and **Google Text-to-Speech (gTTS)** libraries, ensuring accurate content analysis and seamless user experience.

### How to Use:
- **Step 1**: Upload an image (in PNG, JPG, or JPEG format).
- **Step 2**: Choose one of the functionalities:
    - **Real-Time Scene Understanding**: Get a description of the scene in the image.
    - **Text-to-Speech Conversion**: Extract and read out the text from the image.
- **Step 3**: Listen to the generated audio output for a more accessible experience.
"""

st.sidebar.markdown(project_description)

st.subheader("Choose an Option")

# Select mode
option = st.radio(
    "Select one of the functionalities:",
    ("Real-Time Scene Understanding", "Text-to-Speech Conversion for Visual Content"),
)

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Upload Image
uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    # Load the uploaded image using PIL
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

    # Progress bar setup
    progress_bar = st.progress(0)

    if option == "Real-Time Scene Understanding":
        st.header("Real-Time Scene Understanding")

        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            # Define the prompt to guide the image analysis
            prompt = "Describe the scene in this image."

            # Update progress bar (Stage 1: Preparing the request)
            progress_bar.progress(30)

            # Generate content using the model
            response = model.generate_content([image, prompt])

            # Update progress bar (Stage 2: Processing the response)
            progress_bar.progress(60)

            # Display the response
            if hasattr(response, "text") and response.text:
                st.write("**Scene Description:**")
                scene_description = response.text
                st.write(scene_description)

                # Clean the description by removing unwanted characters like asterisks and markdown symbols
                cleaned_description = scene_description.replace("**", "").replace("\n", " ").replace("*","")

                # Convert the cleaned scene description to speech
                st.subheader("Audible Scene Description:")
                tts = gTTS(cleaned_description, lang="en")
                tts.save("scene_description.mp3")

                # Update progress bar (Stage 3: Preparing audio)
                progress_bar.progress(90)

                audio_file = open("scene_description.mp3", "rb")
                st.audio(audio_file.read(), format="audio/mp3")
            else:
                st.error("No description generated. Please try again.")
        except Exception as e:
            st.error(f"Error generating scene description: {str(e)}")

        # Final progress completion
        progress_bar.progress(100)

    elif option == "Text-to-Speech Conversion for Visual Content":
        st.header("Text-to-Speech Conversion")
        
        # OCR to extract text
        st.subheader("Extracted Text:")

        # Update progress bar (Stage 1: OCR extraction)
        progress_bar.progress(30)

        extracted_text = pytesseract.image_to_string(image, config="--psm 3")  # Page segmentation mode 3: Fully automatic page segmentation.
        st.write(extracted_text)

        # Clean the extracted text (removing unwanted newlines)
        cleaned_text = extracted_text.replace("\n", " ").strip()

        if cleaned_text:
            st.subheader("Audible Speech Output:")
            tts = gTTS(cleaned_text, lang="en")
            tts.save("temp_audio.mp3")

            # Update progress bar (Stage 2: Generating speech)
            progress_bar.progress(60)

            audio_file = open("temp_audio.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
        else:
            st.error("No text detected in the image.")

        # Final progress completion
        progress_bar.progress(100)

    # Cleanup temporary files
    if os.path.exists("scene_description.mp3"):
        os.remove("scene_description.mp3")
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

