from flask import request, jsonify, Blueprint
from tensorflow.keras.models import load_model
import numpy as np
import requests
import h5py
import os


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