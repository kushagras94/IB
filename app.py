import os
import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Load the Hugging Face API token from the environment variables
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def generate_image(prompt):
    # Ensure the API token is available
    if not HUGGINGFACE_API_TOKEN:
        st.error("Hugging Face API token not found. Please set the HUGGINGFACE_API_TOKEN environment variable.")
        return None

    # API call to Hugging Face
    headers = {
        'Authorization': f'Bearer {HUGGINGFACE_API_TOKEN}',
    }
    json_data = {
        'inputs': prompt,
    }
    response = requests.post(
        'https://api-inference.huggingface.co/models/your-model-name',
        headers=headers,
        json=json_data
    )
    
    # Return the image content if successful
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        st.error(f"Failed to generate image. Status code: {response.status_code}")
        return None

st.title('Hugging Face Image Generator')

# Prompt input
prompt = st.text_input("Enter a prompt for the image generator:")

# Generate button
if st.button('Generate Image'):
    if prompt:
        st.write(f"Generating image for: '{prompt}'")
        image = generate_image(prompt)
        
        if image:
            st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.error("Please enter a prompt.")
