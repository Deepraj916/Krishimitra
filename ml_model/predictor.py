# ml_model/predictor.py
import os
import json
import re
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Priority order of Gemini models (newer 2.5/flash models first)
CANDIDATE_MODELS = [
    'gemini-2.5-flash',
    'gemini-flash-latest',
    'gemini-2.5-flash-lite',
    'gemini-pro-latest',
    'gemini-2.5-pro',
    'gemini-2.0-flash',
    'gemini-1.5-flash'
]

_active_model_name = None

def _get_genai():
    """Configure google.generativeai with API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[WARNING] GEMINI_API_KEY not found in environment variables.")
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai
    except Exception as e:
        print(f"[ERROR] Failed to configure Gemini SDK: {e}")
        return None

def _clean_json_text(raw_text):
    """Extract and parse JSON from response text even with extra markdown or commentary."""
    text = raw_text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        text = match.group(0)
    return json.loads(text)

def _generate_with_fallback(prompt_payload):
    """Try preferred candidate models in order until one succeeds."""
    global _active_model_name
    genai = _get_genai()
    if not genai:
        return None, "GEMINI_API_KEY is not configured or SDK failed to load"

    models_to_try = list(CANDIDATE_MODELS)
    if _active_model_name and _active_model_name in models_to_try:
        models_to_try.remove(_active_model_name)
        models_to_try.insert(0, _active_model_name)

    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt_payload)
            if response:
                _active_model_name = model_name
                return response, None
        except Exception as e:
            last_error = e
            err_msg = str(e)
            print(f"[INFO] Gemini model '{model_name}' attempt error: {err_msg[:120]}")
            if "404" in err_msg or "not found" in err_msg.lower() or "not supported" in err_msg.lower():
                continue
            continue

    return None, str(last_error) if last_error else "All candidate Gemini models failed"

def predict_disease(image_path):
    """
    Takes an image path and returns a detailed JSON object using Gemini AI.
    Includes robust error handling for safety filters, model fallbacks, and missing keys.
    """
    if not os.getenv("GEMINI_API_KEY"):
        return {
            "plant_name": "Unknown",
            "disease_name": "API Key Missing or Offline",
            "remedy_description": "GEMINI_API_KEY is not configured or unavailable. Please check your .env settings to enable AI disease detection.",
            "product_keyword": None,
            "fertilizer_name": None,
            "quantity_for_10_liters": None
        }

    try:
        img = Image.open(image_path)

        prompt = [
            "You are an expert agricultural botanist. Analyze this image of a plant leaf.",
            "Respond ONLY with a single valid JSON object in the following format:",
            """
            {
              "plant_name": "Name of the plant (e.g., 'Tomato', 'Potato', 'Rose')",
              "disease_name": "Name of the disease or 'Healthy'",
              "remedy_description": "A brief, one or two-sentence suggestion for treatment. If healthy, suggest a general care tip.",
              "product_keyword": "A single, generic search term for a product to treat the disease (e.g., 'fungicide', 'neem oil'). If healthy, this should be null.",
              "fertilizer_name": "Name of the recommended fertilizer or fungicide to spray (e.g., 'Neem Oil', 'Copper Fungicide'). If healthy or not needed, use null.",
              "quantity_for_10_liters": "Minimum quantity of the fertilizer to use for 10 liters of water (e.g., '5 ml', '10 grams'). If not applicable, use null."
            }
            """,
            img
        ]

        response, err = _generate_with_fallback(prompt)

        if err or not response:
            return {
                "plant_name": "N/A",
                "disease_name": "Prediction Error",
                "remedy_description": f"A technical error occurred while analyzing the image: {str(err)[:120]}. Please try again.",
                "product_keyword": None,
                "fertilizer_name": None,
                "quantity_for_10_liters": None
            }

        if hasattr(response, 'prompt_feedback') and response.prompt_feedback and getattr(response.prompt_feedback, 'block_reason', None):
            print(f"AI blocked the image. Reason: {response.prompt_feedback.block_reason}")
            return {
                "plant_name": "N/A",
                "disease_name": "Image Blocked by AI",
                "remedy_description": "The uploaded image was blocked by safety filters. Please try again with a clearer leaf photo.",
                "product_keyword": None,
                "fertilizer_name": None,
                "quantity_for_10_liters": None
            }

        if not response.text:
            return {
                "plant_name": "N/A",
                "disease_name": "Analysis Inconclusive",
                "remedy_description": "The AI could not confidently analyze this image. Please upload a clear, focused photo of the affected plant leaf.",
                "product_keyword": None,
                "fertilizer_name": None,
                "quantity_for_10_liters": None
            }

        return _clean_json_text(response.text)

    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return {
            "plant_name": "N/A",
            "disease_name": "Prediction Error",
            "remedy_description": f"A technical error occurred while analyzing the image: {str(e)[:120]}. Please try again.",
            "product_keyword": None,
            "fertilizer_name": None,
            "quantity_for_10_liters": None
        }

def get_crop_advice(question):
    """
    Takes a user's question and returns expert agricultural advice from Gemini AI.
    """
    if not os.getenv("GEMINI_API_KEY"):
        return "⚠️ **AI Advisor Offline**: GEMINI_API_KEY is not configured or could not be loaded. Please ensure a valid API key is set in `.env` to receive real-time AI agricultural advice."

    try:
        prompt = [
            "You are an expert agricultural scientist providing advice to farmers in India.",
            "Your tone should be helpful, clear, and easy to understand.",
            "Provide a practical, actionable answer to the following question.",
            "Format your answer using simple markdown (e.g., bullet points, bold text). Do not use HTML tags.",
            "---",
            f"Question: {question}"
        ]

        response, err = _generate_with_fallback(prompt)
        if err or not response:
            return f"⚠️ **AI Advisor Error**: {str(err)[:120]}. Please try again later."

        return response.text if response and response.text else "No response generated by the AI service."

    except Exception as e:
        print(f"An error occurred during crop advice generation: {e}")
        return f"Sorry, an error occurred while processing your request: {str(e)[:100]}. Please try again later."