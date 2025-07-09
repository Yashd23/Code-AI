import os
import logging
import whisper

def transcribe_audio(filename):
    """Uses Whisper model to transcribe audio from a file."""
    try:
        logging.info(f"transcribe_audio received file: {filename}")
        if not os.path.exists(filename):
            logging.error(f"File does not exist: {filename}")
            return None
        model = whisper.load_model("base")  # Use 'base' for better CPU compatibility
        result = model.transcribe(filename)
        return result["text"]
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {e}")
        return None 