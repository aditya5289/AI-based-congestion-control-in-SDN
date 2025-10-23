from flask import Flask, request, jsonify
from flask_cors import CORS
import os, pickle
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000","http://localhost:3000"]}})

MODEL_PATH = os.getenv("MODEL_PATH", "../ai/model.pkl")

def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print("Model load error:", e)
        return None

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    if not data:
        return jsonify({"error":"no input data"}), 400
    model = load_model()
    if model is None:
        return jsonify({"error":"model not available"}), 500
    # Expect features: [link_util, queue_len, bw_usage]
    features = data.get("features")
    if features is None:
        return jsonify({"error":"features missing"}), 400
    pred = model.predict([features])
    return jsonify({"prediction": int(pred[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
