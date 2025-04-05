from flask import Blueprint, request, jsonify
from .controllers import make_prediction
from .views import home


routes = Blueprint('main', __name__)

# routes.route('/resources', methods=['GET','POST'])(getResults)

routes.route('/', methods=['GET','POST'])(home)

# routes.route('/main', methods=['GET','POST'])(main)

# routes.route('/main', methods=['GET','POST'])(postQuery)

# @routes.route('/predict', methods=['POST'])
# def predict():
#     """
#     Receives JSON data, passes it to make_prediction, and returns JSON response.
#     """
#     data = request.get_json()  # Get JSON data from request
#     if not data:
#         return jsonify({"error": "Invalid JSON input"}), 400
#     return make_prediction(data) 

routes.route("/predict", methods=["POST"])(make_prediction)
