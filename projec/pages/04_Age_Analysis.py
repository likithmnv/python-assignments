
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Age Analysis")
st.caption("Analyze the relationship between age and credit risk.")
df = add_common_filters(df, "p4")

a,b,c,d=st.columns(4)
a.metric("Average Age",f"{df.AGE.mean():.1f}")
b.metric("Youngest",f"{df.AGE.min():.1f}")
c.metric("Oldest",f"{df.AGE.max():.1f}")
g=df.groupby("AGE_GROUP",observed=False)["TARGET"].mean().mul(100)
d.metric("Highest Risk Age Group",str(g.idxmax()) if len(g) else "—")
st.plotly_chart(px.histogram(df,x="AGE",nbins=50,title="Age Distribution"),use_container_width=True)
st.plotly_chart(px.bar(df["AGE_GROUP"].value_counts(sort=False).reset_index(),x="AGE_GROUP",y="count",title="Applications by Age Group"),use_container_width=True)
x=df.groupby("AGE_GROUP",observed=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
st.plotly_chart(px.bar(x,x="AGE_GROUP",y="Default Rate %",title="Default Rate by Age Group"),use_container_width=True)
st.plotly_chart(px.scatter(df.sample(min(15000,len(df)),random_state=42),x="AGE",y="AMT_CREDIT",color="TARGET",title="Credit Amount by Age"),use_container_width=True)
