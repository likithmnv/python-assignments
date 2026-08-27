
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Annuity Analysis")
st.caption("Study annual loan payment obligations.")
df = add_common_filters(df, "p8")

a,b,c,d=st.columns(4)
a.metric("Average Annuity",f"{df.AMT_ANNUITY.mean():,.0f}")
b.metric("Median Annuity",f"{df.AMT_ANNUITY.median():,.0f}")
c.metric("Maximum Annuity",f"{df.AMT_ANNUITY.max():,.0f}")
d.metric("Avg Annuity for Defaulters",f"{df.loc[df.TARGET==1,'AMT_ANNUITY'].mean():,.0f}")
st.plotly_chart(px.histogram(df,x="AMT_ANNUITY",nbins=60,title="Annuity Distribution"),use_container_width=True)
st.plotly_chart(px.scatter(df.sample(min(15000,len(df)),random_state=42),x="AMT_INCOME_TOTAL",y="AMT_ANNUITY",color="TARGET",title="Annuity vs Income"),use_container_width=True)
st.plotly_chart(px.scatter(df.sample(min(15000,len(df)),random_state=42),x="AMT_CREDIT",y="AMT_ANNUITY",color="TARGET",title="Annuity vs Credit"),use_container_width=True)
x=df.groupby("ANNUITY_BURDEN_GROUP",observed=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
st.plotly_chart(px.bar(x,x="ANNUITY_BURDEN_GROUP",y="Default Rate %",title="Default Rate by Annuity Burden"),use_container_width=True)
