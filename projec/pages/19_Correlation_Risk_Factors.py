
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Correlation & Risk Factor Analysis")
st.caption("Identify numerical relationships associated with loan default.")
df = add_common_filters(df, "p19")

num_cols=[c for c in ["TARGET","AMT_INCOME_TOTAL","AMT_CREDIT","AMT_ANNUITY","AMT_GOODS_PRICE","DAYS_BIRTH","DAYS_EMPLOYED","EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3","CNT_CHILDREN","CNT_FAM_MEMBERS","AGE","EMPLOYMENT_YEARS","CREDIT_INCOME_RATIO","ANNUITY_INCOME_RATIO","CREDIT_GOODS_RATIO","AVERAGE_EXTERNAL_SCORE"] if c in df]
corr=df[num_cols].corr(numeric_only=True)
st.plotly_chart(px.imshow(corr,text_auto=".2f",aspect="auto",title="Correlation Heatmap"),use_container_width=True)
target_corr=corr["TARGET"].drop("TARGET").sort_values()
st.plotly_chart(px.bar(target_corr.reset_index().rename(columns={"index":"Feature","TARGET":"Correlation"}),x="Correlation",y="Feature",orientation="h",title="Correlation with TARGET"),use_container_width=True)
st.subheader("Potential Risk Indicators")
risk = [
    ("Low External Credit Score","Compare low vs high external-score groups."),
    ("High Credit-to-Income Ratio","Higher loan amount relative to income may indicate greater burden."),
    ("High Annuity-to-Income Ratio","Higher payment burden relative to income can be a risk indicator."),
    ("Occupation / Income Type","Compare default rates across categories."),
    ("Age","Check age groups against observed default rates."),
    ("Regional Rating","Compare default rates by regional rating."),
    ("Employment History","Check employment duration and income stability."),
]
for name,desc in risk:
    st.markdown(f"**{name}** — {desc}")
