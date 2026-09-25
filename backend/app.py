
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask(__name__)

# Load the complete preprocessing and model pipeline
model_path = os.path.join(
    os.path.dirname(__file__),
    "superkart_sales_model.joblib"
)
model = joblib.load(model_path)


@superkart_api.get("/")
def home():
    return jsonify(
        {"message": "Welcome to the SuperKart Sales Prediction API"}
    )


@superkart_api.post("/v1/predict")
def predict_sales():
    try:
        data = request.get_json()

        sample = {
            "Product_Weight": data["Product_Weight"],
            "Product_Sugar_Content": data["Product_Sugar_Content"],
            "Product_Allocated_Area": data["Product_Allocated_Area"],
            "Product_Type": data["Product_Type"],
            "Product_MRP": data["Product_MRP"],
            "Store_Size": data["Store_Size"],
            "Store_Location_City_Type": data["Store_Location_City_Type"],
            "Store_Type": data["Store_Type"],
            "Store_Age": data["Store_Age"],
            "Product_Type_Category": data["Product_Type_Category"]
        }

        input_data = pd.DataFrame([sample])
        prediction = model.predict(input_data)[0]

        return jsonify(
            {"predicted_sales": round(float(prediction), 2)}
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 400


@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    try:
        file = request.files["file"]
        input_data = pd.read_csv(file)

        predictions = model.predict(input_data)

        results = {
            str(index): round(float(prediction), 2)
            for index, prediction in enumerate(predictions)
        }

        return jsonify(results)

    except Exception as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    superkart_api.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
