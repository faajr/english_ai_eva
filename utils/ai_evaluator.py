import os
import json
from google import genai
from google.genai import types
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize API Clients
try:
    # Use google-genai SDK
    gemini_client = genai.Client() # Assumes GEMINI_API_KEY is in environment
except Exception as e:
    print(f"Warning: Gemini Client not initialized. {e}")
    gemini_client = None

try:
    openai_client = OpenAI() # Assumes OPENAI_API_KEY is in environment
except Exception as e:
    print(f"Warning: OpenAI Client not initialized. {e}")
    openai_client = None


def evaluate_writing(text: str):
    """
    Evaluates English writing using Gemini.
    """
    if not gemini_client:
        return {"error": "Gemini API key is not configured properly."}
        
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
        response = gemini_client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        
        # Parse JSON
        result_text = response.text.strip()
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
    Transcribes audio to text using OpenAI Whisper API.
    """
    if not openai_client:
        return {"error": "OpenAI API key is not configured properly."}
        
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        return {"transcript": transcription}
    except Exception as e:
        return {"error": str(e)}


def evaluate_speaking(transcript: str):
    """
    Evaluates English speaking (from transcript) using Gemini.
    """
    if not gemini_client:
        return {"error": "Gemini API key is not configured properly."}
        
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
        response = gemini_client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        
        # Parse JSON
        result_text = response.text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith("```"):
            result_text = result_text[3:-3].strip()
            
        data = json.loads(result_text)
        return data
    except Exception as e:
        return {"error": str(e)}
