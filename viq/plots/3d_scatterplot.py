import plotly.graph_objects as go



class Scatter3DPlot:
    def __init__(self, x, y, z, c=None, asset_id=None, customer_name=None,opacity=0.2):
        self.x = x
        self.y = y
        self.z = z
        self.c = c
        self.asset_id = asset_id
        self.customer_name = customer_name
        self.opacity = opacity
        

    def figure(self):
        fig = go.Figure(
            data=[
                go.Scatter3d(
                    x=self.x,
                    y=self.y,
                    z=self.z,
                    mode="markers",
                    opacity=self.opacity,
                    marker=dict(color=self.c) if self.c is not None else None,
                    hovertext= self.asset_id.astype(str) + " | " + self.customer_name.astype(str),
                    hoverinfo="text"
                )
            ]
        )

        fig.update_layout(
            scene=dict(
                xaxis_title=self.x.name,
                yaxis_title=self.y.name,
                zaxis_title=self.z.name,
            )
        )

        return fig

    def show(self):
        self.figure().show()


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_excel("/Users/andrewleacock1/Downloads/scat.xlsx")
    

    Scatter3DPlot(
        x=df["Avg Qty Sold per Visit"],
        y=df["Visit Count"],
        z=df["Avg Outs per Visit"],
        c=df["Number Spoiled"],
        asset_id=df["Asset ID"],
        customer_name=df["Branch Name"], # Customer Name
        opacity=0.5
    ).show()


    