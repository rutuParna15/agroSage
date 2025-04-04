from flask import Blueprint, render_template, request, jsonify
# from .controllers import ocr, search_web, web_scraping, separate_questions, search_youtube_videos, translate_text, summarize_transcript, compare_yt_summaries, createSummary
# from PIL import Image
import io

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    return render_template("landingPage.html")

@views.route('/predict', methods=['GET','POST'])
def predict():
    return render_template("predict.html")