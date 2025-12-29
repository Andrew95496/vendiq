import pandas as pd
import plotly.express as px

df = pd.read_excel("/Users/drewski/Downloads/timeseries.xlsx")

df["Sale Time"] = pd.to_datetime(df["Sale Time"])
df["Quantity"] = pd.to_numeric(df["Quantity"])

# derive day-level fields
df["Date"] = df["Sale Time"]
df["Day_of_Week"] = df["Sale Time"].dt.day_name().sort_values()





# ---------- DAILY TOTALS ----------
daily_totals = (
    df.groupby("Date", as_index=False)["Quantity"]
    .sum()
)

fig_daily = px.bar(
    daily_totals,
    x="Date",
    y="Quantity",
    title="Total Quantity Sold Per Day"
)
fig_daily.show()




# ---------- DAY-OF-WEEK PATTERN ----------
dow_totals = (
    df.groupby("Day_of_Week", as_index=False)["Quantity"]
    .sum()
)

fig_dow = px.bar(
    dow_totals,
    x="Day_of_Week",
    y="Quantity",
    title="Total Quantity Sold by Day of Week"
)
fig_dow.show()







# ---------- WEEK-OVER-WEEK TREND (7-day rolling) ----------
df["Sale Time"] = pd.to_datetime(df["Sale Time"])
df["Quantity"] = pd.to_numeric(df["Quantity"])

# aggregate to daily using Sale Time ONLY
df["Sale Time"] = pd.to_datetime(df["Sale Time"])
df["Quantity"] = pd.to_numeric(df["Quantity"])

# create an explicit daily column
df["Day"] = df["Sale Time"].dt.floor("D")

# daily aggregation
daily_totals = (
    df
    .groupby("Day", as_index=False)["Quantity"]
    .sum()
)

# rolling 7-day average (no cutoff)
daily_totals["Rolling_7_Day"] = (
    daily_totals["Quantity"]
    .rolling(window=7, min_periods=1)
    .mean()
)

fig = px.line(
    daily_totals,
    x="Day",
    y=["Quantity", "Rolling_7_Day"],
    title="Daily Sales with Rolling 7-Day Average"
)

fig.show()
