
import numpy as np

def safe_divide(a, b):
    return a / b.replace(0, np.nan)

def add_features(df):
    df = df.copy()
    if "DAYS_BIRTH" in df:
        df["AGE"] = df["DAYS_BIRTH"].abs() / 365.25
    if "DAYS_EMPLOYED" in df:
        employed = df["DAYS_EMPLOYED"].mask(df["DAYS_EMPLOYED"] >= 365000, np.nan)
        df["EMPLOYMENT_YEARS"] = employed.abs() / 365.25
    if {"AMT_CREDIT","AMT_INCOME_TOTAL"} <= set(df.columns):
        df["CREDIT_INCOME_RATIO"] = safe_divide(df["AMT_CREDIT"], df["AMT_INCOME_TOTAL"])
    if {"AMT_ANNUITY","AMT_INCOME_TOTAL"} <= set(df.columns):
        df["ANNUITY_INCOME_RATIO"] = safe_divide(df["AMT_ANNUITY"], df["AMT_INCOME_TOTAL"])
    if {"AMT_CREDIT","AMT_GOODS_PRICE"} <= set(df.columns):
        df["CREDIT_GOODS_RATIO"] = safe_divide(df["AMT_CREDIT"], df["AMT_GOODS_PRICE"])
    ext = [c for c in ["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"] if c in df.columns]
    if ext:
        df["AVERAGE_EXTERNAL_SCORE"] = df[ext].mean(axis=1)
    return df
