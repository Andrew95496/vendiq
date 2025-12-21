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

df = vq.load("weekly_vending_report.xlsx")

machine_metrics = vq.metrics.machine_summary(df)

par_levels = vq.forecasting.par.recommend(
    df,
    service_days=7
)

sku_flags = vq.optimization.sku_cleanup(df)
