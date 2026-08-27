
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Annuity Burden Analysis")
st.caption("Understand repayment burden relative to income.")
df = add_common_filters(df, "p10")

st.metric("Average Annuity/Income Ratio",f"{df.ANNUITY_INCOME_RATIO.mean():.4f}")
st.plotly_chart(px.histogram(df,x="ANNUITY_INCOME_RATIO",nbins=60,title="Annuity-to-Income Distribution"),use_container_width=True)
x=df.groupby("ANNUITY_BURDEN_GROUP",observed=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
st.plotly_chart(px.bar(x,x="ANNUITY_BURDEN_GROUP",y="Default Rate %",title="Default Rate by Repayment Burden"),use_container_width=True)
for col in ["CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE"]:
    if col in df:
        x=df.groupby(col)["ANNUITY_INCOME_RATIO"].mean().reset_index()
        st.plotly_chart(px.bar(x,x=col,y="ANNUITY_INCOME_RATIO",title=f"Burden Ratio by {col}"),use_container_width=True)
