
import os
import streamlit as st
import pandas as pd
import requests

# Flask backend address
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:7860"
)

st.set_page_config(
    page_title="SuperKart Sales Prediction",
    page_icon="🛒"
)

st.title("🛒 SuperKart Sales Prediction")
st.write(
    "Enter the product and store details below to predict total sales."
)

Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027,
    format="%.3f"
)

Product_Type = st.selectbox(
    "Product Type",
    [
        "Baking Goods",
        "Breads",
        "Breakfast",
        "Canned",
        "Dairy",
        "Frozen Foods",
        "Fruits and Vegetables",
        "Hard Drinks",
        "Health and Hygiene",
        "Household",
        "Meat",
        "Others",
        "Seafood",
        "Snack Foods",
        "Soft Drinks",
        "Starchy Foods"
    ]
)

Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

Store_Type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart"
    ]
)

Store_Age = st.number_input(
    "Store Age",
    min_value=0,
    value=17
)

Product_Type_Category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type": Product_Type,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age": Store_Age,
    "Product_Type_Category": Product_Type_Category
}

if st.button("Predict Sales", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=product_data,
            timeout=30
        )

        if response.status_code == 200:
            predicted_sales = response.json()["predicted_sales"]

            st.success(
                f"Predicted Product Store Sales Total: "
                f"₹{predicted_sales:,.2f}"
            )
        else:
            st.error(
                response.json().get("error", "Prediction failed.")
            )

    except requests.RequestException:
        st.error("Unable to connect to the prediction API.")


st.divider()
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={"file": uploaded_file},
                timeout=60
            )

            if response.status_code == 200:
                results = response.json()

                results_df = pd.DataFrame(
                    results.items(),
                    columns=["Row", "Predicted Sales"]
                )

                st.success(
                    "Batch predictions completed successfully!"
                )
                st.dataframe(
                    results_df,
                    use_container_width=True
                )

            else:
                st.error(
                    response.json().get(
                        "error",
                        "Prediction failed."
                    )
                )

        except requests.RequestException:
            st.error("Unable to connect to the prediction API.")
