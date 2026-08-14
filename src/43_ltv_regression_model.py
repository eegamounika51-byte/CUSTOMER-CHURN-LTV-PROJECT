import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# LOAD LTV DATA
# ==========================================

file_path = "outputs/ltv_features.csv"

df = pd.read_csv(file_path)

print("LTV data loaded successfully!")
print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# CLEAN DATA
# ==========================================

df["ltv"] = pd.to_numeric(
    df["ltv"],
    errors="coerce"
)

df["monthly_charges"] = pd.to_numeric(
    df["monthly_charges"],
    errors="coerce"
)

df["tenure"] = pd.to_numeric(
    df["tenure"],
    errors="coerce"
)

df["total_charges"] = pd.to_numeric(
    df["total_charges"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "ltv",
        "monthly_charges",
        "tenure"
    ]
)


# ==========================================
# SELECT FEATURES
# ==========================================

features = [
    "tenure",
    "monthly_charges",
    "total_charges",
    "revenue_per_month"
]

X = df[features]

y = df["ltv"]


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==========================================
# TRAIN RANDOM FOREST REGRESSOR
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

print("\nLTV Regression Model trained successfully!")


# ==========================================
# PREDICTION
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# MODEL EVALUATION
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n==========================================")
print("LTV REGRESSION MODEL RESULTS")
print("==========================================")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 4))


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\n==========================================")
print("LTV FEATURE IMPORTANCE")
print("==========================================")

print(importance)


# ==========================================
# SAVE FEATURE IMPORTANCE
# ==========================================

importance.to_csv(
    "outputs/ltv_feature_importance.csv",
    index=False
)


# ==========================================
# SAVE TEST PREDICTIONS
# ==========================================

results = X_test.copy()

results["Actual_LTV"] = y_test.values
results["Predicted_LTV"] = predictions

results.to_csv(
    "outputs/ltv_predictions.csv",
    index=False
)


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "models/ltv_regression_model.pkl"
)

print("\nModel saved to:")
print("models/ltv_regression_model.pkl")

print("\nPredictions saved to:")
print("outputs/ltv_predictions.csv")

print("\nFeature importance saved to:")
print("outputs/ltv_feature_importance.csv")


# ==========================================
# COMPLETED
# ==========================================

print("\n==========================================")
print("STEP 43 COMPLETED SUCCESSFULLY!")
print("==========================================")