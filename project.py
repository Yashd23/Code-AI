import os
import warnings
import logging
import streamlit as st
from groq_api import groq_completions
from audio_utils import transcribe_audio
from chat_utils import store_message, get_history

# Configure logging
logging.basicConfig(level=logging.INFO)

# Suppress FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def main():
    st.title("CODE-AI")
    model_options = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "gemma2-9b-it",
        "qwen/qwen3-32b"
    ]
    selected_model = st.selectbox("Select Model", model_options)
    with st.popover("API Key Setup"):
        api_key = st.text_input("Enter your GROQ API Key", type="password")
        try:
            if api_key:
                # Use groq_completions for API key validation with a simple test string
                completion = groq_completions(
                    user_content="Test",
                    model=selected_model,
                    api_key=api_key,
                    temperature=0.5,
                    max_tokens=5,
                    top_p=1
                )
                result = ""
                for chunk in completion:
                    result += chunk or ""
                if api_key.startswith('gsk-'):
                    st.warning("Please enter your Groq API key!", icon='⚠')
                else:
                    st.success("API Key is valid!")
            else:
                st.warning("Please enter and validate your API Key in the sidebar.")
        except Exception:
            st.error("Server is unreachable")

    selected_input = st.selectbox("Select Input", ["Text", "Audio"])

    # Single chat history (no sessions)
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_content = ""
    if selected_input == "Text":
        user_content = st.text_input("How can I help you today?", key="query_input")
    else:
        content = st.audio_input(label="Record your message")
        if content:
            st.audio(content, format="audio/wav")
            # Save audio bytes to a file in the current directory
            audio_filename = os.path.abspath("audio_input.wav")
            try:
                with open(audio_filename, "wb") as f:
                    f.write(content.getvalue())
                file_size = os.path.getsize(audio_filename)
                logging.info(f"Audio file saved at {audio_filename} ({file_size} bytes)")
                if file_size == 0:
                    st.warning("Audio file is empty. Please record again.")
                else:
                    transcription_result = transcribe_audio(audio_filename)
                    if transcription_result:
                        st.write("Transcribed Text:")
                        st.write(transcription_result)
                        user_content = transcription_result
                    else:
                        st.warning("Could not transcribe the audio. Please try again.")
            except Exception as e:
                st.error(f"Error saving or transcribing audio: {e}")
            finally:
                # Clean up the audio file after use
                if os.path.exists(audio_filename):
                    try:
                        os.remove(audio_filename)
                        logging.info(f"Deleted temporary audio file: {audio_filename}")
                    except Exception as e:
                        logging.warning(f"Could not delete audio file: {e}")

    def store_message(role, content):
        st.session_state['chat_history'].append({"role": role, "content": content})

    def get_history():
        return st.session_state['chat_history']

    if st.button("Submit"):
        if not user_content:
            st.warning("Please enter your query to proceed.")
            return
        if not api_key:
            st.warning("Please enter and validate your API Key in the sidebar.")
            return
        # Store user message
        store_message("user", user_content)
        # Retrieve last 5 messages for context
        history = get_history()[-5:]
        context = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        answer = groq_completions(context, selected_model, api_key)
        if answer:
            st.success("Response generated successfully!")
            answer_str = "".join(answer) if not isinstance(answer, str) else answer
            # Store assistant message
            store_message("assistant", answer_str)
            st.markdown(f"```bash\n{answer_str}\n```", unsafe_allow_html=True)
        else:
            st.error("Failed to generate a response. Please try again.")

    if st.button("Clear"):
        st.session_state['chat_history'] = []
        # Do not rerun or exit, just clear

if __name__ == "__main__":
    main()