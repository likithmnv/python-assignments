
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Customer Demographic Analysis")
st.caption("Understand applicant demographic characteristics.")
df = add_common_filters(df, "p3")

a,b,c,d,e=st.columns(5)
a.metric("Customers",f"{len(df):,}")
b.metric("Average Age",f"{df.AGE.mean():.1f}")
b2 = (df.CODE_GENDER=="M").sum() if "CODE_GENDER" in df else 0
c.metric("Male Customers",f"{b2:,}")
d.metric("Female Customers",f"{(df.CODE_GENDER=="F").sum():,}" if "CODE_GENDER" in df else "0")
e.metric("Average Family Size",f"{df.CNT_FAM_MEMBERS.mean():.2f}" if "CNT_FAM_MEMBERS" in df else "—")
for col,title in [("CODE_GENDER","Customers by Gender"),("AGE_GROUP","Customers by Age Group"),("NAME_FAMILY_STATUS","Customers by Family Status"),("NAME_EDUCATION_TYPE","Customers by Education"),("NAME_HOUSING_TYPE","Customers by Housing Type")]:
    if col in df:
        st.plotly_chart(px.bar(df[col].value_counts(dropna=False).reset_index(),x=col,y="count",title=title),use_container_width=True)
if "NAME_EDUCATION_TYPE" in df:
    st.plotly_chart(px.bar(df.groupby("NAME_EDUCATION_TYPE")["TARGET"].mean().mul(100).reset_index(name="Default Rate %"),x="NAME_EDUCATION_TYPE",y="Default Rate %",title="Default Rate by Demographic Group"),use_container_width=True)
