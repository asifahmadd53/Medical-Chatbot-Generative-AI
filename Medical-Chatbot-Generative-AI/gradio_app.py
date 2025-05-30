# if you don't use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# VoiceBot UI with Gradio
import os
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs
system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    try:
        # Transcribe audio
        if audio_filepath:
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )
        else:
            speech_to_text_output = "No audio provided"
        
        # Handle the image input - FIXED: Use the correct vision model
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + " Patient says: " + speech_to_text_output,
                encoded_image=encode_image(image_filepath),
                model="meta-llama/llama-4-scout-17b-16e-instruct"  # Use the vision-capable model
            )
        else:
            doctor_response = "No image provided for me to analyze. Please provide an image along with your audio description for a complete medical assessment."
        
        # Generate speech - FIXED: Remove the output_filepath parameter
        text_to_speech_with_elevenlabs(doctor_response)
        
        # Return the generated audio file path
        output_audio_path = "elevenlabs_output.mp3"  # This is the file created by the function
        
        return speech_to_text_output, doctor_response, output_audio_path
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return "Error in processing", error_message, None

# Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Speak to the Doctor"),
        gr.Image(type="filepath", label="Upload Medical Image (optional)")
    ],
    outputs=[
        gr.Textbox(label="What you said (Speech to Text)"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Response", autoplay=False)
    ],
    title="🩺 AI Doctor with Vision and Voice",
    description="Speak to the AI doctor and optionally provide a medical image for analysis. The doctor will provide professional medical insights based on your description and image.",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    iface.launch(debug=True, share=False)