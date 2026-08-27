
import plotly.express as px
import pandas as pd

def target_bar(df):
    x = df["TARGET"].map({0:"Non-Default",1:"Default"}).value_counts().rename_axis("Status").reset_index(name="Customers")
    return px.bar(x, x="Status", y="Customers", title="Default vs Non-Default Customers")

def group_default_rate(df, col, title=None):
    g = df.groupby(col, dropna=False)["TARGET"].mean().mul(100).reset_index(name="Default Rate %")
    return px.bar(g, x=col, y="Default Rate %", title=title or f"Default Rate by {col}")

def distribution(df, col, title=None):
    return px.histogram(df, x=col, title=title or f"{col} Distribution")

def scatter(df, x, y, color="TARGET", title=None):
    return px.scatter(df, x=x, y=y, color=color, title=title or f"{y} vs {x}", opacity=0.45)
