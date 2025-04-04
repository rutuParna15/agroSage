from flask import Blueprint
from .controllers import make_prediction
from .views import home, postQuery
import request
import jsonify

routes = Blueprint('main', __name__)

# routes.route('/resources', methods=['GET','POST'])(getResults)

routes.route('/', methods=['GET','POST'])(home)

# routes.route('/main', methods=['GET','POST'])(main)

routes.route('/main', methods=['GET','POST'])(postQuery)

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = data.get("input")
        
        if input_data is None:
            return jsonify({"error": "No input data provided"}), 400

        prediction = make_prediction(input_data)
        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500