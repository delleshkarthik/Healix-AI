Healix-AI

Healix-AI is an AI-powered medical assistant that leverages voice and vision capabilities to assist users with medical inquiries. The project was originally built using Gradio and is now transitioning to Streamlit for a more interactive and user-friendly interface.

Features

Voice Recognition: Users can ask medical questions using speech.

Image Processing: AI can analyze medical images.

Natural Language Processing: Understands and responds to health-related queries.

FastAPI Backend: Manages AI model processing.

Streamlit UI: Provides an intuitive user interface for better accessibility.

Installation

1. Clone the Repository

git clone https://github.com/AIwithhassan/ai-doctor-2.0-voice-and-vision.git
cd healix-ai

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies

pip install -r requirements.txt

Running the Application

Using Streamlit

streamlit run app.py

Running the FastAPI Backend

uvicorn main:app --host 0.0.0.0 --port 8000

Converting Gradio to Streamlit

If you are migrating from Gradio to Streamlit:

Replace import gradio as gr with import streamlit as st.

Update UI components (e.g., gr.Interface -> st.button, st.text_input, etc.).

Adjust the API calls accordingly for backend interaction.

Tech Stack

Frontend: Streamlit

Backend: FastAPI

Libraries: OpenAI, SpeechRecognition, PyTorch, Hugging Face models

Contributors

[Your Name]

[Other Contributors]

License

This project is licensed under the MIT License.

