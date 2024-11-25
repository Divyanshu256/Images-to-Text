import streamlit as st
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
from gtts import gTTS
import PIL.Image
import os

# Function to convert text to Markdown format
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Streamlit app layout
def main(model):
    st.title("Gemini 1.5 Flash - Image Analysis and Text Generation")
    
    # File uploader for images
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_container_width=True)
        
        # Load the image for processing
        img = PIL.Image.open(uploaded_file)
        
        try:
            # Generate content using the Gemini model
            response = model.generate_content(img)
            generated_text = response.text
            
            # Display the generated text
            st.write("Generated Text:")
            st.write(generated_text)
            
            # Convert generated text to speech
            tts = gTTS(generated_text)
            tts.save('output.mp3')
            st.audio('output.mp3', format='audio/mp3', start_time=0)
        except Exception as e:
            st.error(f"Error generating content: {e}")
        
if __name__ == "__main__":
    # Load API key from environment variable (for security)
    fetched_api_key = os.getenv("API_KEY")  # Replace with your actual environment variable or key
    genai.configure(api_key=fetched_api_key)
    
    try:
        # Load the Gemini model (update to the new version)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Run the Streamlit app
        main(model)
        
    except Exception as e:
        st.error(f"Error initializing model: {e}")
