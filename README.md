# vendiq

vendiq is a Python library for vending machine analytics.  
It turns raw vending data into clear operational decisions around stocking, service frequency, and machine performance.

This project is built for real world vending operations, not generic retail analytics.

## Purpose

vendiq answers four questions:

What should be stocked  
How much should be stocked  
When machines should be serviced  
Which machines or products are underperforming  

The library is designed to support analysts, operators, and route managers with reproducible, data driven outputs.

## Core Concepts

vendiq is built around a canonical pandas DataFrame that represents vending activity at the machine and SKU level.

All metrics, forecasts, and recommendations are derived from this structure.

## Features

Sales analytics  
Inventory health metrics  
Machine performance metrics  
Par level recommendations  
SKU optimization signals  
Route and service prioritization  

Outputs are returned as clean pandas DataFrames suitable for Excel, Power BI, or downstream automation.

## Project Structure

vendiq/
    data/
        Data loading and validation
    metrics/
        Sales, inventory, and service metrics
    forecasting/
        Baseline and par level forecasting
    optimization/
        SKU and route level recommendations
    reports/
        Summary tables and executive outputs
    utils/
        Shared helpers and statistical utilities

## Example Usage

```python
import vendiq as vq

simulator = vq.monte_carlo.AssetSimulator(
    average_daily_sales=4.74,
    days_between_visits=2,
    lead_time_days=2,
    par_level=21,
    number_of_simulations=10_000
)

results = simulator.run()

```

## Example Output

```
{
    "Stockout_Probability": 0.237,
    "Product_at_Service": 0.763,
    "Avg_Demand": 14,
    "P95_Demand": 18,
    "Effective_Inventory": 11
}

```
