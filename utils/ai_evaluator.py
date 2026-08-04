import os
import json
from google import genai
from google.genai import types
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import whisper

@st.cache_resource
def load_whisper_model():
    # Load the base whisper model (you can change to 'tiny' for speed or 'small' for better accuracy)
    return whisper.load_model("base")

def get_openrouter_client():
    api_key = st.session_state.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None, "API key is empty."
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
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
        
        # Parse JSON
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
    Transcribes audio to text using Local Whisper model.
    """
    try:
        model = load_whisper_model()
        result = model.transcribe(audio_file_path)
        return {"transcript": result["text"]}
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
        
        # Parse JSON
        result_text = response.choices[0].message.content.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith("```"):
            result_text = result_text[3:-3].strip()
            
        data = json.loads(result_text)
        return data
    except Exception as e:
        return {"error": str(e)}
