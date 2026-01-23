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
 # -----------------------------
    # CONFIG
    # -----------------------------
    DAYS_PER_MONTH = 30
    DAYS_BETWEEN_VISITS = 3
    LEAD_TIME_DAYS = 2
    SIMS = 10_000

    # -----------------------------
    # LOAD DATA (YOUR PATHS)
    # -----------------------------
    df_main = pd.read_excel(
        "/Users/andrewleacock1/Downloads/276.xlsx"
    )

    df_par = pd.read_excel(
        "/Users/andrewleacock1/Downloads/276_par.xlsx"
    )


    # -----------------------------
    # DETECT MONTH COLUMNS
    # -----------------------------
    month_columns = get_month_columns(df_main)

    # -----------------------------
    # PAR LOOKUP
    # Presence in df_par == in machine
    # -----------------------------
    if "Vending Par Level" in df_par.columns:
        par_col = "Vending Par Level"
    elif "MM Par" in df_par.columns:
        par_col = "MM Par"
    else:
        raise ValueError(
            "Par file must contain either 'Vending Par Level' or 'MM Par'"
        )

    par_lookup = (
        df_par
        .set_index("Item Name")[par_col]
    )

    # -----------------------------
    # RUN SIMS (ONLY ITEMS IN MACHINE)
    # -----------------------------
    results = []

    for _, row in df_main.iterrows():

        item_name = row["Item Name"]

        # NOT IN PAR FILE -> NOT IN MACHINE
        if item_name not in par_lookup:
            continue

        avg_daily_sales = compute_avg_daily_sales_after_first_sale(
            row=row,
            month_columns=month_columns,
            days_per_month=DAYS_PER_MONTH
        )

        if avg_daily_sales <= 0:
            continue

        mc = ItemRestockingMonteCarlo(
            item_name=item_name,
            average_daily_sales=avg_daily_sales,
            days_between_visits=DAYS_BETWEEN_VISITS,
            lead_time_days=LEAD_TIME_DAYS,
            par_level=int(par_lookup[item_name]),
            number_of_simulations=SIMS
        )

        results.append(mc.sim())

    # -----------------------------
    # OUTPUT
    # -----------------------------
    display_results(results)


```
