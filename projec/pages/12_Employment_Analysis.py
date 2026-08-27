
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Employment Analysis")
st.caption("Understand employment history and income type.")
df = add_common_filters(df, "p12")

a,b,c,d=st.columns(4)
a.metric("Average Employment Years",f"{df.EMPLOYMENT_YEARS.mean():.1f}")
a2=df.OCCUPATION_TYPE.mode().iloc[0] if "OCCUPATION_TYPE" in df and df.OCCUPATION_TYPE.notna().any() else "—"
b.metric("Most Common Occupation",a2)
b2=df.NAME_INCOME_TYPE.mode().iloc[0] if "NAME_INCOME_TYPE" in df else "—"
c.metric("Most Common Income Type",b2)
if "OCCUPATION_TYPE" in df:
    r=df.groupby("OCCUPATION_TYPE")["TARGET"].mean()
    d.metric("Highest Risk Occupation",str(r.idxmax()) if len(r) else "—")
st.plotly_chart(px.histogram(df,x="EMPLOYMENT_YEARS",nbins=50,title="Employment Years Distribution"),use_container_width=True)
st.plotly_chart(px.scatter(df.sample(min(15000,len(df)),random_state=42),x="EMPLOYMENT_YEARS",y="TARGET",title="Employment Years vs Default"),use_container_width=True)
for col,title in [("NAME_INCOME_TYPE","Applications by Income Type"),("OCCUPATION_TYPE","Applications by Occupation"),("ORGANIZATION_TYPE","Default Rate by Organization Type")]:
    if col in df:
        if col=="ORGANIZATION_TYPE":
            x=df.groupby(col)["TARGET"].mean().mul(100).sort_values(ascending=False).head(30).reset_index(name="Default Rate %")
            st.plotly_chart(px.bar(x,x=col,y="Default Rate %",title=title),use_container_width=True)
        else:
            x=df[col].value_counts().head(30).reset_index()
            st.plotly_chart(px.bar(x,x=col,y="count",title=title),use_container_width=True)
if "NAME_INCOME_TYPE" in df:
    x=df.groupby("NAME_INCOME_TYPE")["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
    st.plotly_chart(px.bar(x,x="NAME_INCOME_TYPE",y="Default Rate %",title="Default Rate by Income Type"),use_container_width=True)
