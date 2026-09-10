from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(
    title="Customer Churn & LTV Prediction API",
    version="1.0.0"
)


class CustomerData(BaseModel):
    tenure: float
    monthly_charges: float
    total_charges: float


def predict_customer(customer):

    if customer.tenure < 12 and customer.monthly_charges > 70:
        probability = 0.80
        prediction = "Yes"

    elif customer.tenure < 24 and customer.monthly_charges > 60:
        probability = 0.60
        prediction = "Yes"

    else:
        probability = 0.20
        prediction = "No"

    return {
        "churn_prediction": prediction,
        "churn_probability": probability
    }


# Single customer
@app.post("/predict")
def predict_churn(customer: CustomerData):

    return predict_customer(customer)


# Batch customers
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


@app.get("/")
def home():

    return {
        "message": "Customer Churn & LTV API is running",
        "status": "success"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }