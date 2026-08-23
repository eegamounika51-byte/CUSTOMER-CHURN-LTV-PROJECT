from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib


# ==========================================
# LOAD TRAINED CHURN MODEL
# ==========================================

MODEL_PATH = "models/final_churn_model.pkl"
FEATURE_PATH = "outputs/final_feature_names.csv"

model = joblib.load(MODEL_PATH)

feature_names = pd.read_csv(FEATURE_PATH)["Feature"].tolist()


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0.0"
)


# ==========================================
# CUSTOMER INPUT
# ==========================================

class CustomerData(BaseModel):
    SeniorCitizen: int
    tenure: float
    MonthlyCharges: float
    TotalCharges: float

    gender: str
    Partner: str
    Dependents: str
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str


# ==========================================
# PREPROCESS INPUT
# Same logic used during model training
# ==========================================

def prepare_features(customer: CustomerData):

    data = pd.DataFrame([customer.model_dump()])

    data = pd.get_dummies(
        data,
        drop_first=True
    )

    data = data.reindex(
        columns=feature_names,
        fill_value=0
    )

    data = data.fillna(0)

    return data


# ==========================================
# PREDICTION FUNCTION
# ==========================================

def predict_customer(customer: CustomerData):

    features = prepare_features(customer)

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1]

    churn_prediction = "Yes" if prediction == 1 else "No"

    return {
        "churn_prediction": churn_prediction,
        "churn_probability": round(float(probability), 4)
    }


# ==========================================
# SINGLE CUSTOMER
# ==========================================

@app.post("/predict")
def predict_churn(customer: CustomerData):

    return predict_customer(customer)


# ==========================================
# BATCH CUSTOMERS
# ==========================================

@app.post("/batch_predict")
def batch_predict(customers: List[CustomerData]):

    results = []

    for customer in customers:

        prediction = predict_customer(customer)

        results.append({
            "customer": customer.model_dump(),
            "prediction": prediction
        })

    return {
        "total_customers": len(results),
        "predictions": results
    }


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Customer Churn Prediction API is running",
        "status": "success"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": "final_churn_model.pkl"
    }