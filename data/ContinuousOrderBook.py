#relevant imports
import csv
import time
import requests
import pandas as pd

#helper functions
def flatten(l):
    return [item for sublist in l for item in sublist]

def unpack(ts, resp_json):
    seq = resp_json['sequence']
    bid = resp_json['bids']
    ask = resp_json['asks']

    return [ts, seq] + flatten(bid) + flatten(ask)

#create column names
def create_col_headers():
    col_bids = []
    col_asks = []
    for i in range(1,51):
        col_bids.append("Bid_" + str(i) + "_Price")
        col_bids.append("Bid_" + str(i) + "_Size")
        col_bids.append("Bid_" + str(i) + "_Trades")
        col_asks.append("Ask_" + str(i) + "_Price")
        col_asks.append("Ask_" + str(i) + "_Size")
        col_asks.append("Ask_" + str(i) + "_Trades")

    return ["Timestamp", "Sequence"] + col_bids + col_asks

def main():
    #initialize counters
    file_counter = 0
    dp_counter = 0

    headers = create_col_headers()

    #loop - while true, always collect
    while True:
        start = pd.Timestamp.now(tz='America/New_York')
        if dp_counter != 0 and dp_counter % 50000 == 0:
            file_counter+=1
            dp_counter = 0

        #open stream
        write_file = open('./data/BTC/BTC_Book__' + str(file_counter) + '.csv', 'a+', newline='')
        writer = csv.writer(write_file)

        if dp_counter == 0:
            #write header
            writer.writerow(headers)

        #query data from API
        resp = requests.get('https://api.pro.coinbase.com/products/BTC-USD/book?level=2')
        ts = pd.Timestamp.now(tz='America/New_York')

        #transform and output data
        data_line = unpack(ts,resp.json())
        writer.writerow(data_line)

        #close stream
        write_file.close()
        dp_counter+=1

        #wait, so that each iteration takes ~5s
        end = pd.Timestamp.now(tz='America/New_York')
        elapsed_sec = ((end-start).value)/1000000000
        time.sleep(max(0, 1 - elapsed_sec))


if __name__ == '__main__':
    main()
