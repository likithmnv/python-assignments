
import pandas as pd

def basic_kpis(df):
    return {
        "Total Applications": len(df),
        "Default Customers": int((df["TARGET"] == 1).sum()) if "TARGET" in df else 0,
        "Non-Default Customers": int((df["TARGET"] == 0).sum()) if "TARGET" in df else 0,
        "Default Rate %": df["TARGET"].mean() * 100 if "TARGET" in df else 0,
        "Average Income": df["AMT_INCOME_TOTAL"].mean() if "AMT_INCOME_TOTAL" in df else 0,
        "Average Credit": df["AMT_CREDIT"].mean() if "AMT_CREDIT" in df else 0,
        "Average Annuity": df["AMT_ANNUITY"].mean() if "AMT_ANNUITY" in df else 0,
        "Average Age": df["AGE"].mean() if "AGE" in df else 0,
    }
