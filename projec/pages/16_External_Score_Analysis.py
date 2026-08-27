
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data, add_common_filters, default_rate

df = load_data()
st.title("External Credit Score Analysis")
st.caption("Analyze external credit scores and their relationship with TARGET.")
df = add_common_filters(df, "p16")

ext=[c for c in ["EXT_SOURCE_1","EXT_SOURCE_2","EXT_SOURCE_3"] if c in df]
a,b,c,d=st.columns(4)
for box,col in zip([a,b,c],ext[:3]):
    box.metric(f"Average {col}",f"{df[col].mean():.3f}")
d.metric("Missing External Score Records",f"{df[ext].isna().any(axis=1).sum():,}" if ext else "—")
for col in ext:
    st.plotly_chart(px.histogram(df,x=col,nbins=50,title=f"{col} Distribution"),use_container_width=True)
    if "TARGET" in df:
        x=df.groupby(pd.qcut(df[col],10,duplicates="drop"))["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
        st.plotly_chart(px.line(x,x=col,y="Default Rate %",markers=True,title=f"{col} vs Default Rate"),use_container_width=True)
if len(ext)>=2:
    st.plotly_chart(px.scatter(df.sample(min(15000,len(df)),random_state=42),x=ext[0],y=ext[1],color="TARGET",title=f"{ext[0]} vs {ext[1]}"),use_container_width=True)
st.metric("Average External Score",f"{df.AVERAGE_EXTERNAL_SCORE.mean():.3f}")
