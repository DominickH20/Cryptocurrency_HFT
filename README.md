# Cryptocurrency HFT

## Data Collection
Price data is collected through the Coinbase public API approximately every second. We collect the level 2 order book aggregated into the top 50 bids and asks. The data is exported to CSV for ease of access and can be found [here](./data).
<img src="./figures/Timedelta_Quality.png" width="500" height="500" align = "middle">

## Data Analysis
<p align="center">
  <img src="./figures/Price_Level_Order_Size.png" width="500" height="500" align = "middle"/>
</p>

<img src="./figures/Price_Jump_Order_Book.gif" width="500" height="500" align = "middle">

Clustering of time series subsequences

## Model Development
LSTMs on each cluster identified in the prior step

## Trading Strategy Implementation
TBD
