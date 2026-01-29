import pandas as pd
import plotly.graph_objects as go


def plot_simulation_timeseries(csv_path):
    df = pd.read_csv(csv_path)
    df = df.sort_values("simulation_id")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["simulation_id"],
            y=df["days_to_3_outs"],
            mode="lines",
            name="Days to 3 Outs"
        )
    )

    fig.update_layout(
        title="Monte Carlo Simulation – Days to 3 Outs",
        xaxis_title="Simulation Run",
        yaxis_title="Days to 3 Outs",
        hovermode="x unified"
    )

    fig.show()


if __name__ == "__main__":
    plot_simulation_timeseries(
        "machine_time_to_3_outs_simulations.csv"
    )
