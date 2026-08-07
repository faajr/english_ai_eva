import os
import json
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_openrouter_client():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None, "OPENROUTER_API_KEY not found in environment / Streamlit Secrets."
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        return client, None
    except Exception as e:
        return None, str(e)


def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None, "GROQ_API_KEY not found in environment / Streamlit Secrets."
    try:
        client = Groq(api_key=api_key)
        return client, None
    except Exception as e:
        return None, str(e)


def evaluate_writing(text: str):
    """
    Evaluates English writing using OpenRouter (Gemini model).
    """
    client, err = get_openrouter_client()
    if not client:
        return {"error": f"OpenRouter API key is not configured properly. Details: {err}"}

    prompt = f"""
    You are an expert English language evaluator. Evaluate the following text written by an English learner.
    Provide scores from 0 to 100 for Grammar, Vocabulary, Coherence, and an Overall score.
    Also provide constructive feedback.
    
    Text to evaluate:
    "{text}"
    
    Return the result EXACTLY in the following JSON format without any markdown blocks or extra text:
    {{
        "grammar_score": <number>,
        "vocabulary_score": <number>,
        "coherence_score": <number>,
        "overall_score": <number>,
        "feedback": "<string>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.5-pro",
            messages=[{"role": "user", "content": prompt}],
        )

        result_text = response.choices[0].message.content.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith("```"):
            result_text = result_text[3:-3].strip()

        data = json.loads(result_text)
        return data
    except Exception as e:
        return {"error": str(e)}


def speech_to_text(audio_file_path: str):
    """
    Transcribes audio to text using Groq Whisper (free, fast, cloud-compatible).
    """
    groq_client, err = get_groq_client()
    if not groq_client:
        return {"error": f"Groq API key tidak dikonfigurasi. Details: {err}"}

    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                response_format="text",
                language="en",   # Force English transcription
            )
        return {"transcript": transcription}
    except Exception as e:
        return {"error": str(e)}


def evaluate_speaking(transcript: str):
    """
    Evaluates English speaking (from transcript) using OpenRouter (Gemini model).
    """
    client, err = get_openrouter_client()
    if not client:
        return {"error": f"OpenRouter API key is not configured properly. Details: {err}"}

    prompt = f"""
    You are an expert English language evaluator. Evaluate the following speaking transcript from an English learner.
    Provide scores from 0 to 100 for Grammar, Vocabulary, Fluency, and an Overall score.
    Note that spoken English may have filler words, self-corrections, etc. Adjust your expectations accordingly.
    Also provide constructive feedback.
    
    Transcript to evaluate:
    "{transcript}"
    
    Return the result EXACTLY in the following JSON format without any markdown blocks or extra text:
    {{
        "grammar_score": <number>,
        "vocabulary_score": <number>,
        "fluency_score": <number>,
        "overall_score": <number>,
        "feedback": "<string>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.5-pro",
            messages=[{"role": "user", "content": prompt}],
        )

        result_text = response.choices[0].message.content.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith("```"):
            result_text = result_text[3:-3].strip()

        data = json.loads(result_text)
        return data
    except Exception as e:
        return {"error": str(e)}
