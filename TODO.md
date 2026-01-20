# TODO

- Make the data loader its own folder
- Loads in the excel file then runs a roling average to perdict a the average sales then pun that into the possion

```
viq/
├── analysis/
│   ├── __init__.py
│   ├── descriptive.py
│   ├── stats.py
├── load/
│   ├── __init__.py
│   ├── sales_loader.py
│   ├── timeseries_loader.py
├── simulation/
│   ├── __init__.py
│   ├── asset_paths.py
│   ├── demand_simulation.py
├── plots/
│   ├── __init__.py
│   ├── scatter.py
│   ├── time_series.py
│   ├── rolling.py
├── utils/
│   ├── __init__.py
│   ├── dates.py
├── README.md
├── requirements.txt
├── TODO.md
```