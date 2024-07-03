from termcolor import colored as cl
from yahoo_fin.stock_info import get_data
import pandas
import datetime



def backtest(value, high, low, type, df, reverse=True, printing=False, graphs=False):
    # Check type
    type = type.lower()
    if type not in ["w", "d"]:
        return 0

    # Filter period that have enough data to calculate Donchian Channel
    wkmax = max(high, low)
    stock_sl = df.loc[df.index > (df.index[0] + datetime.timedelta(days=(wkmax*7)))]

    stock_sl.loc[:,["cash"]] = 0.0
    stock_sl.loc[:,["stock value"]] = 0.0
    stock_sl.loc[:,["total value"]] = 0.0
    stock_sl.loc[:,["gain"]] = 0.0
    stock_sl.loc[:,["drawdown"]] = 0.0
    stock_sl.loc[:,["shares"]] = 0

    # Change index for numeric instead of date - because it works better for indexing in loops
    stock_sl.loc[:,["date"]] = stock_sl.index
    stock_sl.reset_index(drop=True, inplace=True)

    stock_sl.at[0,"cash"] = value
    max_value = value
    reversed_text = ", R" if reverse else ", N"
    scenario = str(high) + str(type) + ' high, ' + str(low) + str(type) + ' low' + reversed_text

    logs = cl('BACKTEST INVESTMENT, Conditions: ' + scenario + '\n\n', color = 'blue', attrs = ['bold'])

    for index in range(1, len(stock_sl)):
        last_index = index - 1
        # Check reverse parameter
        ## Normal parameter would be: if passing minimum low, buy, if passing maximum high, sell
        if reverse:
            buy_criteria = stock_sl.at[index, "high"] >= stock_sl.at[index, f"{high}{type}-high"]
            sell_criteria = stock_sl.at[index, "low"] <= stock_sl.at[index, f"{low}{type}-low"]
        else:
            buy_criteria = stock_sl.at[index, "low"] <= stock_sl.at[index, f"{low}{type}-low"]
            sell_criteria = stock_sl.at[index, "high"] >= stock_sl.at[index, f"{high}{type}-high"]


        # Se não investido, checa critério de entrada
        if stock_sl.at[last_index, "shares"] == 0 and buy_criteria:
            # COMPRA
            stock_price = stock_sl.at[index, "low"]
            stock_sl.at[index, "shares"] = int(stock_sl.at[last_index, "cash"] / stock_price)
            stock_sl.at[index, "stock value"] = stock_sl.at[index,"shares"] * stock_price
            stock_sl.at[index, "cash"] = stock_sl.at[last_index, "cash"] - stock_sl.at[index,"stock value"]
            logs += cl('BUY: ', color = 'green', attrs = ['bold']) + f'{stock_sl.at[index, "shares"]} Shares are bought at ${stock_price:.2f} on {str(stock_sl.at[index, "date"])[:10]}'
            totalvalue = stock_sl.at[index, "cash"] + stock_sl.at[index, "stock value"]
            logs += f"TOTAL VALUE: ${totalvalue:.0f}\n"
        # Se investido, checa critério de saída
        elif stock_sl.at[last_index, "shares"] > 0 and sell_criteria:
            # VENDE
            stock_price = stock_sl.at[index, "high"]
            stock_sl.at[index, "cash"] = stock_sl.at[last_index, "cash"] + stock_sl.at[last_index, "shares"] * stock_price
            stock_sl.at[index, "shares"] = 0
            stock_sl.at[index, "stock value"] = 0.0
            logs += cl('SELL: ', color = 'red', attrs = ['bold']) + f'{stock_sl.at[last_index, "shares"]} Shares are sold at ${stock_price:.2f} on {str(stock_sl.at[index, "date"])[:10]}'
            totalvalue = stock_sl.at[index, "cash"] + stock_sl.at[index, "stock value"]
            logs += f"TOTAL VALUE: ${totalvalue:.0f}\n"

        # Atualiza o valor do patrimônio, caso não comprou nem vendeu
        else:
            stock_sl.at[index, "cash"] = stock_sl.at[index - 1, "cash"]
            stock_sl.at[index, "shares"] = stock_sl.at[index - 1, "shares"]

            # Atualiza stock value
            stock_price = stock_sl.at[index, "close"]
            stock_sl.at[index, "stock value"] = stock_sl.at[index, "shares"] * stock_price
        
        stock_sl.at[index, "total value"] = stock_sl.at[index, "cash"] + stock_sl.at[index, "stock value"]
        stock_sl.at[index, "gain"] = stock_sl.at[index, "total value"] / value - 1

        # Calcula Drawdown
        max_value = stock_sl.at[index, "total value"] if stock_sl.at[index, "total value"] > max_value else max_value
        current_min = stock_sl.at[index, "total value"]
        stock_sl.at[index, "drawdown"] = (max_value - current_min) / max_value
        
    # Calcula EARNING, ROI anualizado e total
    roi = stock_sl.at[len(stock_sl) - 1, "gain"]
    time_of_investment = stock_sl.at[len(stock_sl) - 1, "date"] - stock_sl.at[0, "date"]
    time_of_investment = time_of_investment.total_seconds()/(60*60*24*365)

    earning = stock_sl.at[len(stock_sl) - 1, "total value"] - value
    
    roi = earning / value
    if roi >= 0:
        roi_annualized = (pow(roi, 1.0 / time_of_investment) - 1) * 100
        roi = (roi - 1) * 100
    else:
        roi = roi * 100
        roi_annualized = roi
    
    logs += f"\nEARNING: ${earning:,.0f} ; ROI: {roi_annualized:.0f}% (annual), {roi:.0f}% (total)\n"

    # Calcula Drawdown
    drawdown = stock_sl["drawdown"].max()
    drawdown = int(drawdown * 1000) / 10
    buyhold = (stock_sl.at[len(stock_sl) - 1, "close"] - stock_sl.at[1, "open"]) / stock_sl.at[1, "open"]
    if buyhold >= 0:
        buyhold_annualized = (pow(buyhold, 1.0 / time_of_investment) - 1) * 100
        buyhold = (buyhold - 1) * 100
    else:
        buyhold = buyhold * 100
        buyhold_annualized = buyhold
    logs += f"DRAWDOWN: {drawdown:.0f}% ; BUY & HOLD ROI: {buyhold_annualized:.0f}% (annual), {buyhold:.0f}% (total)\n\n\n"

    if printing:
        print(logs)
    
    summary = {
        "Stock": stock_sl.at[0, "ticker"],
        "Scenario": scenario,
        "ROI Annual": roi_annualized,
        "Drawdown": drawdown,
        "B&H ROI Annual": buyhold_annualized
    }

    return summary


def get_stockdata(ticker):
    start_date = "20/03/1994"
    end_date = "20/03/2024"
    stock = get_data(ticker=ticker, start_date=start_date, end_date=end_date, index_as_date = True, interval="1d")
    stock = stock.dropna()
    return stock

def calculate_limits(df, type):
    # Check type
    type = type.lower()
    if type not in ["w", "d"]:
        return 0
    
    # Period in weeks (w) or days (d)
    conditions_high = []
    conditions_low = []
    multiplier = 7 if type == "w" else 1
    for i in range (5,66,5):
        conditions_high.append(i)
        conditions_low.append(i)
        df[str(i) + str(type) + "-high"] = df["high"].rolling(window=(str(i*multiplier) + 'D')).max()
        df[str(i) + str(type) + "-low"] = df["low"].rolling(window=(str(i*multiplier) + 'D')).min()

    return df