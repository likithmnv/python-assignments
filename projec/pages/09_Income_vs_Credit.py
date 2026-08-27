
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Income vs Credit Analysis")
st.caption("Determine whether requested loans are proportional to income.")
df = add_common_filters(df, "p9")

a,b,c=st.columns(3)
a.metric("Average Credit/Income",f"{df.CREDIT_INCOME_RATIO.mean():.2f}")
b.metric("Highest Credit/Income",f"{df.CREDIT_INCOME_RATIO.replace([float("inf")],float("nan")).max():.2f}")
high=df[df.CREDIT_INCOME_RATIO>6]
c.metric("Default Rate > 6",f"{high.TARGET.mean()*100:.2f}%" if len(high) else "—")
sample=df.sample(min(20000,len(df)),random_state=42)
st.plotly_chart(px.scatter(sample,x="AMT_INCOME_TOTAL",y="AMT_CREDIT",color="TARGET",hover_data=["CREDIT_INCOME_RATIO"],title="Income vs Credit"),use_container_width=True)
st.plotly_chart(px.histogram(df,x="CREDIT_INCOME_RATIO",nbins=60,title="Credit/Income Ratio Distribution"),use_container_width=True)
x=df.groupby("CREDIT_INCOME_RISK",observed=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
st.plotly_chart(px.bar(x,x="CREDIT_INCOME_RISK",y="Default Rate %",title="Default Rate vs Credit/Income Risk"),use_container_width=True)
