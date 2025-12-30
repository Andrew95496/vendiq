import pandas as pd


class TimeSeriesLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        df = pd.read_excel(self.filepath)

        df["Sale Time"] = pd.to_datetime(df["Sale Time"])
        df["Quantity"] = pd.to_numeric(df["Quantity"])

        df["Date"] = df["Sale Time"]
        df["Day_of_Week"] = df["Sale Time"].dt.day_name()
        df["Day"] = df["Sale Time"].dt.floor("D")

        return df


if __name__ == "__main__":
    loader = TimeSeriesLoader("/Users/drewski/Downloads/timeseries.xlsx")
    df = loader.load()
    print(df.head())
