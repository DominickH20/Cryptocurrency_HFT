# Cryptocurrency HFT

## Data Collection
Price data is collected through the Coinbase public API approximately every second. We collect the level 2 order book aggregated into the top 50 bids and asks. The data is exported to CSV for ease of access and can be found [here](./data).
![alt text](./figures/Timedelta_Quality.png)
<img src="./figures/Timedelta_Quality.png" width="100" height="100">

## Data Analysis
Clustering of time series subsequences

## Model Development
LSTMs on each cluster identified in the prior step

## Trading Strategy Implementation
TBD
