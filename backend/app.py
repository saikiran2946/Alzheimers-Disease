from flask import Flask, request, jsonify
import joblib
import numpy as np
import tensorflow as tf
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import traceback

app = Flask(__name__)
CORS(app)

# Load the model
try:
    model = tf.keras.models.load_model("../model.h5")
    scaler = joblib.load("../scaler.pkl")
    print("✅ Model and scaler loaded successfully")
except Exception as e:
    print("❌ Error loading model/scaler:", str(e))

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Flask Backend is Running!"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Authentication failed"}), 401

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("Received Request Data:", data)  # Debugging Log

        if not data or "features" not in data:
            print("Error: Missing 'features' in request")  # Log the error
            return jsonify({"error": "Missing 'features' in request"}), 400
        
        features = data["features"]
        print("Features for Prediction:", features)  # Log the features received

        if not isinstance(features, list) or len(features) != 12:
            print("Error: Invalid input format")  # Log incorrect format
            return jsonify({"error": "Invalid input format. Expected a list of 12 numbers."}), 400

        # # Convert list to NumPy array and reshape
        # reshaped_features = np.array(features).reshape( -1)

        # # Apply scaling
        # # scaled_features = scaler.transform(reshaped_features)

        # # Make prediction
        # prediction = model.predict(reshaped_features)
        features_array = np.array(features, dtype=np.float32).reshape(1, -1)
        # Apply scaling
        scaled_features = scaler.transform(features_array)

        # Reshape for CNN input (1, 12, 1)
        cnn_input = scaled_features.reshape(1, 12, 1)

        # ANN input remains (1, 12)
        ann_input = scaled_features

        # Make prediction
        prediction = model.predict([cnn_input, ann_input])

        print("✅ Model Prediction Raw Output:", prediction)  # Debugging log

        # Convert output to label
        predicted_class = "Alzheimer's Detected" if prediction[0][0] > 0.6 else "No Alzheimer's"
        
        return jsonify({"prediction": predicted_class})

    except Exception as e:
        print(" ERROR in /predict:", str(e))
        print(traceback.format_exc())  # ✅ Print Full Error Stack Trace
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
