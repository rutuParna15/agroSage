from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint("main", __name__)

VALID_USERNAME = "user123"
VALID_PASSWORD = "pass1234"

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username != VALID_USERNAME or password != VALID_PASSWORD:
            error = "Invalid Credentials"
        else:
            return redirect(url_for("main.dashboard"))
    return render_template("login.html", error=error)

@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@main.route('/predict', methods=['POST'])
def predict():
    name = request.form.get("name")
    phone = request.form.get("phone")
    state = request.form.get("state")
    print(name, phone, state)  # Just for debugging
    return render_template("predict.html")
