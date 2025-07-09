import logging
import streamlit as st
from groq import Groq

def groq_completions(
    user_content,
    model,
    api_key,
    temperature=0.5,
    top_p=1,
    max_tokens=1024
):
    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI-powered coding assistant here to help with programming challenges.\n"
                        "You can assist with various tasks, including:\n\n"
                        "- **Debugging Code**\n"
                        "- **Explaining Concepts**\n"
                        "- **Code Suggestions**\n"
                        "- **Optimization Tips**\n"
                        "- **Learning Resources**"
                    )
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True,
            stop=None,
        )

        result = ""
        for chunk in completion:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                result += delta_content
                yield delta_content
                logging.info(f"Streamed chunk: {delta_content}")

        logging.info("Final aggregated result generated successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")
        yield "" 