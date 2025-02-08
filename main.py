# Import necessary libraries
import os
import gradio as gr
import webbrowser
from threading import Timer
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# System prompt
system_prompt = """You are a professional doctor. Your goal is to provide medical insights based on the given image and patient input.
If the image contains any medical concerns, describe them clearly and suggest possible causes along with basic remedies.
If you are unsure about a condition, encourage seeking medical advice instead of giving vague responses like ‘I am unsure’ or ‘Contact a doctor.’

⚠ *Restrictions:*
- If a user asks about *non-medical topics*, politely refuse by saying: "I am a doctor and can only answer medical-related questions."
- Do *not* add numbers, special characters, or markdown formatting in your response.
- Always provide responses as if you are speaking directly to a patient.
- Start your response immediately without unnecessary disclaimers.

💡 *Response Style:*
- Do not say "In the image, I see..." Instead, phrase it as:
  "With what I see, I think you have..."
- Keep responses *concise (max 2 sentences)* and *empathetic* while remaining professional.
"""

# Process user input
def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Generate voice output
    voice_of_doctor = text_to_speech_with_elevenlabs(
        input_text=doctor_response, 
        output_filepath="final.mp3"
    ) 

    return speech_to_text_output, doctor_response, "final.mp3"

# Create an improved Gradio interface
with gr.Blocks(title="AI Doctor with Vision & Voice") as demo:
    gr.Markdown("## 🏥 AI Doctor with Vision & Voice")
    gr.Markdown("Upload an image, speak your symptoms, and receive a professional medical response.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak Your Symptoms")
            image_input = gr.Image(type="filepath", label="🖼️ Upload Medical Image (Optional)")
            submit_button = gr.Button("Analyze 🩺")

        with gr.Column():
            speech_text_output = gr.Textbox(label="📝 Speech to Text")
            doctor_response_output = gr.Textbox(label="💡 Doctor's Response")
            voice_output = gr.Audio(label="🔊 Doctor's Voice Response ")

    submit_button.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_text_output, doctor_response_output, voice_output]
    )

    # Add developer credit with LinkedIn profile
    gr.Markdown(
        "👨‍💻 **Developed by [Dellesh Karthik Saradhi](https://www.linkedin.com/in/delleshkarthiksaradhi/)**"
    )

# Function to open the browser automatically
def open_browser():
    webbrowser.open("http://127.0.0.1:7860")

# Run the app and open it in the browser automatically
if __name__ == "__main__":
    Timer(1, open_browser).start()
    demo.launch(share=False)
