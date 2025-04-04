from flask import request, jsonify, Blueprint
from tensorflow.keras.models import load_model
import numpy as np
import requests
import h5py
import os


controllers = Blueprint('controllers', __name__)

# model = load_model("./model/crop_recommendation_model.h5")
model = load_model(r"C:\Users\Rutuparna\Desktop\flask-server\app\model\crop_model.h5")

def make_prediction(json_data):
    try:
        # Extract values from JSON and convert to NumPy array
        input_values = [
            json_data["N"], 
            json_data["P"], 
            json_data["K"], 
            json_data["temperature"], 
            json_data["humidity"], 
            json_data["pH"], 
            json_data["rainfall"]
        ]
        input_array = np.array(input_values).reshape(1, -1)

        # Predict using the trained model
        prediction = model.predict(input_array)

        # Convert to JSON response
        response = {
            "prediction": prediction.tolist()  # Ensure it's serializable
        }
        return jsonify(response)

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

