
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Executive Overview")
st.caption("Overall picture of applicants and credit risk.")
df = add_common_filters(df, "p1")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Applications", f"{len(df):,}")
c2.metric("Default Customers", f"{(df.TARGET==1).sum():,}")
c3.metric("Default Rate", f"{df.TARGET.mean()*100:.2f}%")
c4.metric("Average Income", f"{df.AMT_INCOME_TOTAL.mean():,.0f}")
c5,c6,c7,c8 = st.columns(4)
c5.metric("Non-Default Customers", f"{(df.TARGET==0).sum():,}")
c6.metric("Average Credit", f"{df.AMT_CREDIT.mean():,.0f}")
c7.metric("Average Annuity", f"{df.AMT_ANNUITY.mean():,.0f}")
c8.metric("Average Age", f"{df.AGE.mean():.1f}")
col1,col2 = st.columns(2)
with col1:
    x=df.TARGET.map({0:"Non-Default",1:"Default"}).value_counts().reset_index()
    x.columns=["Status","Customers"]
    st.plotly_chart(px.bar(x,x="Status",y="Customers",title="Default vs Non-Default"),use_container_width=True)
with col2:
    if "CODE_GENDER" in df:
        st.plotly_chart(px.bar(df["CODE_GENDER"].value_counts().reset_index(),x="CODE_GENDER",y="count",title="Applications by Gender"),use_container_width=True)
col1,col2 = st.columns(2)
with col1:
    st.plotly_chart(px.histogram(df,x="AMT_INCOME_TOTAL",nbins=50,title="Income Distribution"),use_container_width=True)
with col2:
    st.plotly_chart(px.histogram(df,x="AMT_CREDIT",nbins=50,title="Credit Amount Distribution"),use_container_width=True)
st.dataframe(df.head(100),use_container_width=True)
