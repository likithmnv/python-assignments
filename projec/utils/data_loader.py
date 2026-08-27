
import os
import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "application_train.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    if "DAYS_BIRTH" in df:
        df["AGE"] = df["DAYS_BIRTH"].abs() / 365.25

    if "DAYS_EMPLOYED" in df:
        # Home Credit uses 365243 as a special value for some records.
        employed = df["DAYS_EMPLOYED"].copy()
        employed = employed.mask(employed >= 365000, np.nan)
        df["EMPLOYMENT_YEARS"] = employed.abs() / 365.25

    if {"AMT_CREDIT", "AMT_INCOME_TOTAL"}.issubset(df.columns):
        df["CREDIT_INCOME_RATIO"] = (
            df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"].replace(0, np.nan)
        )

    if {"AMT_ANNUITY", "AMT_INCOME_TOTAL"}.issubset(df.columns):
        df["ANNUITY_INCOME_RATIO"] = (
            df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"].replace(0, np.nan)
        )

    if {"AMT_CREDIT", "AMT_GOODS_PRICE"}.issubset(df.columns):
        df["CREDIT_GOODS_RATIO"] = (
            df["AMT_CREDIT"] / df["AMT_GOODS_PRICE"].replace(0, np.nan)
        )

    ext = [c for c in ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"] if c in df]
    if ext:
        df["AVERAGE_EXTERNAL_SCORE"] = df[ext].mean(axis=1)

    if "AGE" in df:
        bins = [0,25,30,35,40,45,50,55,60,float("inf")]
        labels = ["18–25","26–30","31–35","36–40","41–45","46–50","51–55","56–60","61+"]
        df["AGE_GROUP"] = pd.cut(df["AGE"], bins=bins, labels=labels, right=True)

    if "AMT_INCOME_TOTAL" in df:
        bins = [-np.inf,50000,100000,150000,200000,300000,500000,np.inf]
        labels = ["Below 50K","50K–100K","100K–150K","150K–200K","200K–300K","300K–500K","Above 500K"]
        df["INCOME_GROUP"] = pd.cut(df["AMT_INCOME_TOTAL"], bins=bins, labels=labels)

    if "AMT_CREDIT" in df:
        bins = [-np.inf,100000,300000,500000,700000,1000000,np.inf]
        labels = ["Below 100K","100K–300K","300K–500K","500K–700K","700K–1M","Above 1M"]
        df["CREDIT_GROUP"] = pd.cut(df["AMT_CREDIT"], bins=bins, labels=labels)

    if "CREDIT_INCOME_RATIO" in df:
        bins = [-np.inf,2,4,6,np.inf]
        labels = ["Low (<2)","Moderate (2–4)","High (4–6)","Very High (>6)"]
        df["CREDIT_INCOME_RISK"] = pd.cut(df["CREDIT_INCOME_RATIO"], bins=bins, labels=labels)

    if "ANNUITY_INCOME_RATIO" in df:
        q = df["ANNUITY_INCOME_RATIO"].quantile([0.25, 0.5, 0.75]).tolist()
        if len(set(q)) == 3:
            df["ANNUITY_BURDEN_GROUP"] = pd.cut(
                df["ANNUITY_INCOME_RATIO"],
                bins=[-np.inf, *q, np.inf],
                labels=["Low","Medium","High","Very High"]
            )

    return df

def fmt_num(x):
    return f"{x:,.0f}" if pd.notna(x) else "—"

def default_rate(data):
    if len(data) == 0 or "TARGET" not in data:
        return np.nan
    return data["TARGET"].mean() * 100

def add_common_filters(df, key_prefix="common"):
    st.sidebar.header("Filters")

    out = df.copy()

    if "TARGET" in out:
        target = st.sidebar.multiselect(
            "TARGET", sorted(out["TARGET"].dropna().unique().tolist()),
            default=sorted(out["TARGET"].dropna().unique().tolist()),
            key=f"{key_prefix}_target"
        )
        if target:
            out = out[out["TARGET"].isin(target)]

    if "CODE_GENDER" in out:
        vals = sorted(out["CODE_GENDER"].dropna().unique().tolist())
        sel = st.sidebar.multiselect("Gender", vals, default=vals, key=f"{key_prefix}_gender")
        if sel: out = out[out["CODE_GENDER"].isin(sel)]

    if "AGE" in out:
        mn, mx = float(out["AGE"].min()), float(out["AGE"].max())
        lo, hi = st.sidebar.slider("Age Range", mn, mx, (mn, mx), key=f"{key_prefix}_age")
        out = out[out["AGE"].between(lo, hi)]

    if "AMT_INCOME_TOTAL" in out:
        mn, mx = float(out["AMT_INCOME_TOTAL"].min()), float(out["AMT_INCOME_TOTAL"].max())
        lo, hi = st.sidebar.slider("Income Range", mn, mx, (mn, mx), key=f"{key_prefix}_income")
        out = out[out["AMT_INCOME_TOTAL"].between(lo, hi)]

    if "AMT_CREDIT" in out:
        mn, mx = float(out["AMT_CREDIT"].min()), float(out["AMT_CREDIT"].max())
        lo, hi = st.sidebar.slider("Credit Range", mn, mx, (mn, mx), key=f"{key_prefix}_credit")
        out = out[out["AMT_CREDIT"].between(lo, hi)]

    for col, label in [
        ("NAME_CONTRACT_TYPE","Contract Type"),
        ("NAME_INCOME_TYPE","Income Type"),
        ("NAME_EDUCATION_TYPE","Education"),
        ("NAME_FAMILY_STATUS","Family Status"),
        ("OCCUPATION_TYPE","Occupation"),
        ("NAME_HOUSING_TYPE","Housing Type"),
    ]:
        if col in out:
            vals = sorted(out[col].dropna().unique().tolist())
            if len(vals) <= 80:
                sel = st.sidebar.multiselect(label, vals, default=[], key=f"{key_prefix}_{col}")
                if sel: out = out[out[col].isin(sel)]

    for col, label in [("FLAG_OWN_CAR","Car Ownership"),("FLAG_OWN_REALTY","Property Ownership")]:
        if col in out:
            vals = sorted(out[col].dropna().unique().tolist())
            sel = st.sidebar.multiselect(label, vals, default=[], key=f"{key_prefix}_{col}")
            if sel: out = out[out[col].isin(sel)]

    return out
