import plotly.express as px
import pandas as pd


df = pd.read_excel("/Users/andrewleacock1/Downloads/scat.xlsx")

fig = px.box(df, x=df['Branch Name'], y=df["Avg Qty Sold per Visit"], points="outliers", hover_data=["Asset ID"])
fig.show()