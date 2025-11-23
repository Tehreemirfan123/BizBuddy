import os
import joblib
import numpy as np
import pandas as pd

# Get absolute path to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load models using absolute paths
profit_model_path = os.path.join(PROJECT_ROOT, "Models_Files", "profit_model.pkl")
failure_model_path = os.path.join(PROJECT_ROOT, "Models_Files", "failure_model.pkl")
encoder_path = os.path.join(PROJECT_ROOT, "Models_Files", "encoder.pkl")

profit_model = joblib.load(profit_model_path)
failure_model = joblib.load(failure_model_path)
encoder = joblib.load(encoder_path)

# Load dataset 
_dataset_path = os.path.join(PROJECT_ROOT, "Dataset_Generation", "micro_business_dataset_500.csv")
try:
    _df_cached = pd.read_csv(_dataset_path)
except Exception:
    _df_cached = None 

# Prepare input
def prepare_input(sample, encoder):
    import pandas as pd
    import numpy as np

    # Create dataframe with zeros for all encoded features
    input_df = pd.DataFrame(columns=encoder.get_feature_names_out())
    input_df.loc[0] = 0

    # Numeric features
    numeric_cols = ["Startup_Cost_PKR", "Cost_per_Unit", "Price_per_Unit"]
    for col in numeric_cols:
        input_df[col] = sample[col]

    # Encode categorical features
    cat_features = encoder.transform([[sample["Business"], sample["City"], sample["Product/Service"], sample["Marketing_Channel"]]])
    cat_cols = encoder.get_feature_names_out()
    for i, col in enumerate(cat_cols):
        input_df[col] = cat_features[0][i]

    return input_df

def predict_business_idea(user_budget: float, city: str = None, top_n: int = 5):
    """
    Returns a list of suggested business types formatted for Streamlit display.
    Each suggestion is a multi-line string with percentage for failure risk.
    """
    if _df_cached is None:
        return []

    df = _df_cached.copy()
    df["Est_Monthly_Profit"] = (df["Price_per_Unit"] - df["Cost_per_Unit"]) * 30

    if city and city in df["City"].unique():
        df_city = df[df["City"] == city]
        if len(df_city) >= 5:
            df = df_city

    agg = df.groupby("Business").agg(
        Avg_Startup=("Startup_Cost_PKR", "mean"),
        Avg_Monthly_Profit=("Est_Monthly_Profit", "mean"),
        Avg_Failure_Risk=("Failure_Risk", "mean"),
        Count=("Business", "count")
    ).reset_index()

    budget_limit = max(0, user_budget) * 1.1
    candidates = agg[(agg["Avg_Startup"] <= budget_limit) & (agg["Count"] >= 3)].copy()

    if candidates.empty:
        candidates = agg[(agg["Avg_Startup"] <= max(1, user_budget) * 2)].copy()

    candidates["score"] = candidates["Avg_Monthly_Profit"] - (candidates["Avg_Failure_Risk"] * candidates["Avg_Startup"])
    candidates = candidates.sort_values(by="score", ascending=False)

    suggestions = []
    for _, row in candidates.head(top_n).iterrows():
        suggestion_text = (
            f"**Business:** {row['Business']}  \n"
            f"**Avg Startup:** {int(round(row['Avg_Startup']))} PKR  \n"
            f"**Estimated Monthly Profit:** {int(round(row['Avg_Monthly_Profit']))} PKR  \n"
            f"**Avg Failure Risk:** {int(round(row['Avg_Failure_Risk'] * 100))}%"
        )
        suggestions.append(suggestion_text)

    return suggestions


def predict_profit(sample, profit_model, encoder):
    input_df = prepare_input(sample, encoder)
    return profit_model.predict(input_df)[0]

def predict_failure(sample, failure_model, encoder):
    input_df = prepare_input(sample, encoder)
    return failure_model.predict(input_df)[0]
