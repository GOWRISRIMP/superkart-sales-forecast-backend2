import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows HTML/JS on GitHub Pages to connect

# Locate and load the trained model relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Update filename if your model has a different name (e.g., model.joblib or model.pkl)
MODEL_PATH = os.path.join(BASE_DIR, "superkart_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "SuperKart Sales Forecast API is live"})

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    try:
        data = request.get_json()

        # Extract parameters sent from frontend
        product_weight = float(data.get("Product_Weight", 0))
        product_sugar = data.get("Product_Sugar_Content")
        product_area = float(data.get("Product_Allocated_Area", 0))
        product_mrp = float(data.get("Product_MRP", 0))
        store_size = data.get("Store_Size")
        store_city = data.get("Store_Location_City_Type")
        store_type = data.get("Store_Type")
        store_age = float(data.get("Store_Age_Years", 0))
        product_category = data.get("Product_Type_Category")

        # Feature Transformation
        product_area_log = np.log1p(product_area)

        # Create DataFrame matching training format
        input_df = pd.DataFrame([{
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar,
            "Product_Allocated_Area": product_area_log,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_city,
            "Store_Type": store_type,
            "Store_Age_Years": store_age,
            "Product_Type_Category": product_category
        }])

        prediction = model.predict(input_df)[0]
        return jsonify({"Predicted_Sales": round(float(prediction), 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
