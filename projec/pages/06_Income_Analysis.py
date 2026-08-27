
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Income Analysis")
st.caption("Understand income and its relationship with credit risk.")
df = add_common_filters(df, "p6")

a,b,c,d,e=st.columns(5)
a.metric("Total Income",f"{df.AMT_INCOME_TOTAL.sum():,.0f}")
b.metric("Average Income",f"{df.AMT_INCOME_TOTAL.mean():,.0f}")
c.metric("Median Income",f"{df.AMT_INCOME_TOTAL.median():,.0f}")
d.metric("Maximum Income",f"{df.AMT_INCOME_TOTAL.max():,.0f}")
e.metric("Avg Income of Defaulters",f"{df.loc[df.TARGET==1,'AMT_INCOME_TOTAL'].mean():,.0f}")
st.plotly_chart(px.histogram(df,x="AMT_INCOME_TOTAL",nbins=60,title="Income Distribution"),use_container_width=True)
x=df.groupby("INCOME_GROUP",observed=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
st.plotly_chart(px.bar(x,x="INCOME_GROUP",y="Default Rate %",title="Default Rate by Income Group"),use_container_width=True)
st.plotly_chart(px.scatter(df.sample(min(15000,len(df)),random_state=42),x="AMT_INCOME_TOTAL",y="AMT_CREDIT",color="TARGET",title="Income vs Credit"),use_container_width=True)
if "NAME_EDUCATION_TYPE" in df:
    st.plotly_chart(px.box(df.sample(min(20000,len(df)),random_state=1),x="NAME_EDUCATION_TYPE",y="AMT_INCOME_TOTAL",title="Income by Education"),use_container_width=True)
