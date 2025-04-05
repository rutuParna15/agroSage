from flask import request, jsonify, Blueprint
from tensorflow.keras.models import load_model
import numpy as np
import requests
import h5py
import pickle
import tensorflow as tf

import os
from groq import Groq
from dotenv import load_dotenv

controllers = Blueprint('controllers', __name__)

# model = load_model("./model/crop_recommendation_model.h5")
# model = load_model(r"C:\Users\Rutuparna\Desktop\flask-server\app\model\crop_model.h5")
model = tf.keras.models.load_model(r"C:\Users\Rutuparna\Desktop\flask-server\app\model\crop_model_.h5")
scaler = pickle.load(open(r"C:\Users\Rutuparna\Desktop\flask-server\app\model\scaler.pkl", "rb"))
label_encoder = pickle.load(open(r"C:\Users\Rutuparna\Desktop\flask-server\app\model\label_encoder.pkl", "rb"))

# def make_prediction(data):
#     data = request.get_json()

#     # Extract features from request
#     features = [
#         data["N"], data["P"], data["K"],
#         data["temperature"], data["humidity"],
#         data["ph"], data["rainfall"]
#     ]
#     input_data = np.array([features])

#     # Scale the input
#     input_scaled = scaler.transform(input_data)

#     # Make prediction
#     prediction = model.predict(input_scaled)
#     predicted_index = np.argmax(prediction)
#     predicted_crop = label_encoder.inverse_transform([predicted_index])[0]

#     return jsonify({"recommended_crop": predicted_crop})

def get_nasa_yearly_avg(lat: float, lon: float):
    """
    Fetch yearly average temperature, humidity, and rainfall from NASA POWER.
    """
    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
        "parameters": "T2M,RH2M,PRECTOTCORR",
        "community": "ag",
        "longitude": lon,
        "latitude": lat,
        "format": "json"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "properties" not in data or "parameter" not in data["properties"]:
            return {"error": "Unexpected response format from NASA POWER"}

        params_data = data["properties"]["parameter"]
        temp_avg = sum(params_data["T2M"].values()) / 12
        humidity_avg = sum(params_data["RH2M"].values()) / 12
        rainfall_total_mm = sum(params_data["PRECTOTCORR"].values()) * 25.4  # Convert inches to mm
        
        return {
            "temperature": round(temp_avg, 2),
            "humidity": round(humidity_avg, 2),
            "rainfall": round(rainfall_total_mm, 2)
        }
    return {"error": f"Failed to fetch NASA weather data: {response.status_code}"}

def make_prediction():
    """Process input, fetch NASA data, and predict the best crop."""
    data = request.get_json()
    lat, lon = float(data["latitude"]), float(data["longitude"])
    weather_data = get_nasa_yearly_avg(lat, lon)
    
    if "error" in weather_data:
        return jsonify({"error": weather_data["error"]}), 400
    
    features = [
        data["N"], data["P"], data["K"],
        weather_data["temperature"], weather_data["humidity"],
        data["ph"], weather_data["rainfall"]
    ]
    input_data = np.array([features])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    predicted_index = np.argmax(prediction)
    predicted_crop = label_encoder.inverse_transform([predicted_index])[0]
    
    return jsonify({
        "recommended_crop": predicted_crop,
        # "weather_data": weather_data,
        # "features": features
    })