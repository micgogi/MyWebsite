import pandas as pd
import talib
import csv
import requests
import json

import yfinance as yf


def download_csv(url, filename="downloaded.csv"):
    """Downloads a CSV file from the given URL and saves it with the specified filename."""

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        with open(filename, "wb") as csv_file:
            csv_file.write(response.content)

        print(f"Downloaded CSV file to: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading CSV file: {e}")
def lambda_handler():
    symbol = 'ZOMATO.NS'
    first_colmn_data = []
    # pullt the data from nse https://archives.nseindia.com/content/equities/EQUITY_L.csv

    csv_file_path = "./downloaded.csv"
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) > 0:
                first_colmn_data.append(row[0] + '.NS')

    # print(first_colmn_data)
    # stocksSymbols = ','.join(first_colmn_data)
    # print(stocksSymbols)
    # Fetch historical data
    stock_dict = {}
    stock_size = 1
    for stock in first_colmn_data:
        try:
            data = yf.download(stock, period="max")
            print(stock)

            print(f"total stock scanned:{stock_size}")

            if data is None:
                print("not found data %s", data)
            current_price = data["Close"].iloc[-1]
            all_time_high = data["Close"].max()
            # print("cuuent")
            # print(current_price)
            # print("ATH")
            # print(all_time_high)
            stock_size = stock_size + 1
            if current_price >= all_time_high:
                print("price is high")
                print(f"{stock} is breaking high")
                stock_dict[stock] = current_price
            # if current_price > all_time_high:
            #     return f"{stocks} is breaking its all-time high! Current price: {current_price:.2f}"
            # else:
            #     return (f"{ticker_symbol} is not breaking its all-time high. "
            #             f"Current price: {current_price:.2f}, All-time high: {all_time_high:.2f}")

        except:
            print("no data found")


        # tickers = pd.read_html('https://ournifty.com/stock-list-in-nse-fo-futures-and-options.html#:~:text=NSE%20F%26O%20Stock%20List%3A%20%20%20%20SL,%20%201000%20%2052%20more%20rows%20')[0]

        # Calculate RSI for a 14-day period
        # period = 14
        #
        # data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        # print(data)
        # Check if RSI crosses a threshold
        # if len(data) < 2:
        #     print("The DataFrame has fewer than 2 rows.")
        # else:
        #
        #     second_last_row = data.iloc[-2]
        #     last_row = data.iloc[-1]
        # print(stock)

        # if last_row['RSI'] > 60:
        #     stock_dict[stock] = last_row['RSI']
            # message = f"{stock} crossed RSI 40 in the last trading session."
            # You can send this message via AWS SNS or another notification method
            # print(message)
            # print(second_last_row)
    print(stock_dict)
    for key, value in stock_dict.items():
        print(f"{key}: {value}")
    return {
        'statusCode': 200,
        'body': 'Function executed successfully!'
    }


def main():
    # Call the temp method here

    data_csv_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    download_csv(data_csv_url)
    lambda_handler()


if __name__ == "__main__":
    main()
