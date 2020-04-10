# Cryptocurrency HFT

## Data Collection
Price data is collected through the Coinbase public API approximately every second. We collect the level 2 order book aggregated into the top 50 bids and asks. The data is exported to CSV for ease of access and can be found [here](./data).
![alt text](./figures/Timedelta_Quality.png)
![test image size](./figures/Timedelta_Quality.png){:class="img-responsive"}
![test image size](./figures/Timedelta_Quality.png){:height="50%" width="50%"}
![test image size](./figures/Timedelta_Quality.png){:height="700px" width="400px"}

## Data Analysis
Clustering of time series subsequences

## Model Development
LSTMs on each cluster identified in the prior step

## Trading Strategy Implementation
TBD
