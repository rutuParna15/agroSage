from flask import request, jsonify, Blueprint
from tensorflow.keras.models import load_model
import numpy as np
import requests
import h5py
import os
from groq import Groq


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
def jarangebot_chat_controller():
    try:
        # Get the prompt from POST request
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        # Initialize Groq client
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return jsonify({"error": "GROQ_API_KEY not set in environment."}), 500

        client = Groq(api_key=api_key)

        # Send prompt to Groq
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": """You are JarangeBot, an expert agricultural assistant for Indian farmers. Your purpose is to help farmers maximize their yields and income through sustainable practices.

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

Do not respond to non-agriculture related queries.
"""}, 
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        # Extract response
        response_text = chat_completion.choices[0].message.content
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
