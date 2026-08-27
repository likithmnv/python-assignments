
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Family & Children Analysis")
st.caption("Study household characteristics and credit risk.")
df = add_common_filters(df, "p13")

a,b,c,d,e=st.columns(5)
a.metric("Average Children",f"{df.CNT_CHILDREN.mean():.2f}")
b.metric("Average Family Members",f"{df.CNT_FAM_MEMBERS.mean():.2f}")
c.metric("Customers with Children",f"{(df.CNT_CHILDREN>0).sum():,}")
d.metric("Customers without Children",f"{(df.CNT_CHILDREN==0).sum():,}")
r=df.groupby("NAME_FAMILY_STATUS")["TARGET"].mean()
e.metric("Highest Risk Family Type",str(r.idxmax()) if len(r) else "—")
for col,title in [("CNT_CHILDREN","Customers by Number of Children"),("CNT_FAM_MEMBERS","Customers by Family Size"),("NAME_FAMILY_STATUS","Applications by Family Status")]:
    x=df[col].value_counts().reset_index()
    st.plotly_chart(px.bar(x,x=col,y="count",title=title),use_container_width=True)
for col,title in [("CNT_CHILDREN","Default Rate by Number of Children"),("CNT_FAM_MEMBERS","Default Rate by Family Size"),("NAME_FAMILY_STATUS","Default Rate by Family Status")]:
    x=df.groupby(col)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
    st.plotly_chart(px.bar(x,x=col,y="Default Rate %",title=title),use_container_width=True)
