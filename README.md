# CODE-AI

A modular AI-powered coding assistant with text and audio input, powered by Groq and Whisper, built using Streamlit.

## Features
- Chat with LLMs (Groq API)
- Audio transcription (OpenAI Whisper)
- Modular Python codebase for easy maintenance

## Project Structure
```
.
├── project.py         # Streamlit UI entry point
├── groq_api.py        # Groq completions logic
├── audio_utils.py     # Audio transcription logic
├── chat_utils.py      # Chat history/session logic
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Code-LLM-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run project.py
   ```

## Usage
- Enter your Groq API key in the sidebar.
- Choose text or audio input.
- Submit your query and get coding help!

## Notes
- Requires Python 3.8+
- For audio, Whisper's 'base' model is used for CPU compatibility.

---
MIT License 