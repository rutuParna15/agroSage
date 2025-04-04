from flask import request, jsonify, Blueprint
from tensorflow.keras.models import load_model
import numpy as np
import requests
import h5py
import os
from groq import Groq
from dotenv import load_dotenv

controllers = Blueprint('controllers', __name__)

model = load_model("./model/crop_recommendation_model.h5")

def make_prediction(input_data):
    """
    Receives input_data (e.g., a list or array), preprocesses it, and returns prediction
    """
    # Make sure input is in the right shape (adjust as per your model's input)
    input_array = np.array(input_data).reshape(1, -1)

    # Predict
    prediction = model.predict(input_array)
    return prediction.tolist()


# Controller function to handle chat interaction
def agri_chat():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SARVAM_API_URL = "https://api.sarvam.ai/translate"
    SARVAM_HEADERS = {
        "Content-Type": "application/json",
        "API-Subscription-Key": "df62896e-6a3c-40a7-8103-3df5c9c00077"
    }

    try:
        # --- Input Handling ---
        data = request.json
        prompt = data.get("prompt", "")
        user_lang = data.get("lang", "en")

        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        # --- Translation to English if needed ---
        if user_lang in ["hi", "mr"]:
            payload_translate_in = {
                "input": prompt,
                "source_language_code": "auto",
                "target_language_code": "en-IN",
                "speaker_gender": "Female",
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": False,
                "output_script": "roman",
                "numerals_format": "international"
            }
            try:
                res = requests.post(SARVAM_API_URL, json=payload_translate_in, headers=SARVAM_HEADERS)
                prompt = res.json().get("output", prompt)
            except Exception as e:
                return jsonify({"error": f"Error translating to English: {str(e)}"}), 500

        # --- GROQ Response ---
        client = Groq(api_key=GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": """You are AgriAI, an expert agricultural assistant for Indian farmers. Your purpose is to help farmers maximize their yields and income through sustainable practices.

Provide guidance on:
1. Crop selection based on soil type, season, climate zone, and market demand
2. Optimizing yields using data on soil nutrients, pH, humidity, temperature, and rainfall
3. Pest and disease management with both traditional and modern approaches
4. Water management and irrigation techniques appropriate for different regions
5. Relevant government schemes and subsidies based on farm size, income, crop type, and location
6. Organic farming practices and certification processes
7. Post-harvest storage and marketing strategies
8. Weather advisories and climate-smart agriculture techniques
9. Financial planning, loans, and insurance options for farmers
10. Modern agricultural technologies appropriate for small and medium farmers

When responding to farmers:
- Be respectful and practical in your advice
- Consider the constraints of small-scale farming (1-5 acres) common in India
- Provide specific, actionable recommendations rather than general advice
- Refer to crops and practices relevant to Indian agriculture
- Consider regional differences (North, South, East, West, Central India)
- Use simple language and avoid technical jargon when possible
- Include both traditional wisdom and modern scientific approaches

Don't respond to non-agriculture related queries.
"""}, 
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        response = chat_completion.choices[0].message.content

        # --- Translate response back to user language ---
        if user_lang in ["hi", "mr"]:
            payload_translate_out = {
                "input": response,
                "source_language_code": "en-IN",
                "target_language_code": "hi-IN" if user_lang == "hi" else "mr-IN",
                "speaker_gender": "Female",
                "mode": "formal",
                "model": "mayura:v1",
                "enable_preprocessing": False,
                "output_script": "fully-native",
                "numerals_format": "international"
            }
            try:
                res = requests.post(SARVAM_API_URL, json=payload_translate_out, headers=SARVAM_HEADERS)
                response = res.json().get("translated_text", response)
            except Exception as e:
                return jsonify({"error": f"Error translating back to {user_lang}: {str(e)}"}), 500

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500