
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("Missing Value Analysis")
st.caption("Understand data quality before modeling.")
df = add_common_filters(df, "p18")

miss=df.isna().sum()
pct=df.isna().mean().mul(100)
a,b,c,d,e=st.columns(5)
a.metric("Total Rows",f"{len(df):,}")
b.metric("Total Columns",f"{df.shape[1]:,}")
c.metric("Total Missing Values",f"{int(miss.sum()):,}")
d.metric("Columns with Missing Values",f"{(miss>0).sum():,}")
e.metric("Columns >50% Missing",f"{(pct>50).sum():,}")
m=pd.DataFrame({"Column":miss.index,"Missing Count":miss.values,"Missing %":pct.values,"Data Type":df.dtypes.astype(str).values}).sort_values("Missing Count",ascending=False)
st.plotly_chart(px.bar(m.head(20),x="Missing Count",y="Column",orientation="h",title="Top 20 Columns with Missing Values"),use_container_width=True)
st.plotly_chart(px.bar(m.sort_values("Missing %",ascending=False).head(30),x="Missing %",y="Column",orientation="h",title="Missing Percentage by Column"),use_container_width=True)
st.dataframe(m,use_container_width=True)
st.info("Treatment options should be chosen column-by-column: drop, mean/median, mode, Unknown, or a missing indicator. Avoid blindly filling all columns the same way.")
