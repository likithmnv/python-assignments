
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Credit Amount Analysis")
st.caption("Analyze the amount of credit requested.")
df = add_common_filters(df, "p7")

a,b,c,d,e=st.columns(5)
for box,label,val in [(a,"Total Credit",df.AMT_CREDIT.sum()),(b,"Average Credit",df.AMT_CREDIT.mean()),(c,"Median Credit",df.AMT_CREDIT.median()),(d,"Maximum Credit",df.AMT_CREDIT.max()),(e,"Minimum Credit",df.AMT_CREDIT.min())]:
    box.metric(label,f"{val:,.0f}")
st.plotly_chart(px.histogram(df,x="AMT_CREDIT",nbins=60,title="Credit Amount Distribution"),use_container_width=True)
st.plotly_chart(px.box(df,x="TARGET",y="AMT_CREDIT",title="Credit Amount by TARGET"),use_container_width=True)
x=df.groupby("CREDIT_GROUP",observed=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
st.plotly_chart(px.bar(x,x="CREDIT_GROUP",y="Default Rate %",title="Default Rate by Credit Range"),use_container_width=True)
for col in ["CODE_GENDER","NAME_INCOME_TYPE","NAME_EDUCATION_TYPE","NAME_CONTRACT_TYPE"]:
    if col in df:
        x=df.groupby(col)["AMT_CREDIT"].mean().reset_index()
        st.plotly_chart(px.bar(x,x=col,y="AMT_CREDIT",title=f"Average Credit by {col}"),use_container_width=True)
