
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Default / Target Analysis")
st.caption("Analyze TARGET and default patterns.")
df = add_common_filters(df, "p2")

a,b,c,d=st.columns(4)
a.metric("TARGET = 0", f"{(df.TARGET==0).sum():,}")
b.metric("TARGET = 1", f"{(df.TARGET==1).sum():,}")
c.metric("Default Rate", f"{df.TARGET.mean()*100:.2f}%")
d.metric("Non-Default Rate", f"{(1-df.TARGET.mean())*100:.2f}%")
col1,col2=st.columns(2)
with col1:
    x=df.TARGET.map({0:"Non-Default",1:"Default"}).value_counts().reset_index()
    x.columns=["Status","Customers"]
    st.plotly_chart(px.bar(x,x="Status",y="Customers"),use_container_width=True)
with col2:
    x=df.TARGET.map({0:"Non-Default",1:"Default"}).value_counts().reset_index()
    x.columns=["Status","Customers"]
    st.plotly_chart(px.pie(x,names="Status",values="Customers",hole=.45),use_container_width=True)
for col,title in [("CODE_GENDER","Default Rate by Gender"),("NAME_INCOME_TYPE","Default Rate by Income Type"),("NAME_EDUCATION_TYPE","Default Rate by Education"),("NAME_CONTRACT_TYPE","Default Rate by Contract Type")]:
    if col in df:
        st.plotly_chart(px.bar(df.groupby(col)["TARGET"].mean().mul(100).reset_index(name="Default Rate %"),x=col,y="Default Rate %",title=title),use_container_width=True)
