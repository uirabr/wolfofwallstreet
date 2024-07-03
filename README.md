# WOLF OF WALL STREET
#### Video Demo:  https://youtu.be/eoeQBd5SF5E
#### Description:

## Wolf of Wall Street: search for strategies to beat the market

This program was born out of curiosity from an investment article called *“An Algo Trading Strategy which made +8,371%: A Python Case Study”*. This article makes a case that anyone could make more than 8000% on an algo trading strategy, considering a period of 30 years.

With this project, I intend to answer a few questions about this investment, like:

1)	Is this a legitimate strategy that could be repeated over time and with any other stock? 
2)	Is this the best strategy considering we might change parameters of investment to optimize it?
3)	How this strategy compares to simpler approaches like Buy & Hold of the actual stock, or Buy & Hold of S&P or QQQ index? 

This program explores and optimizes investment strategies based on the Donchian Channel indicator. It utilizes historical stock data to backtest various parameter combinations and identify potentially profitable trading opportunities.

**Donchian Channel indicator** is equal the average maximum or minimum of a determined past period. For instance, the Donchian Channel of 5 weeks high (5w-high) means the average of maximum prices for the last 5 weeks – this is calculated daily for all the investment period (30 years).

The program was written in a Jupiter Notebook format (.ipynb) due to its flexibility to try different approaches and to run only a small part of the code, and not the entire program as a whole. This proved to be a smart choice, as the core of the program takes 5-10 hours to run – it would not be wise to run all of it every time we need to change a small part of the code.


#### Disclaimer: This program is for educational purposes only and should not be considered financial advice. Past performance does not guarantee future results.


## Premisses

The original article makes an investment case with Apple Stock (AAPL), but, in reality, no one would know 30 years ago that this stock would be one of the best of market in this period. So:

1)	This program tests the top 20 stocks from S&P 500 in this 30-year-period (1994-2024);

2)	It varies the period of the Donchian Channel from 5 to 65 weeks, and later from 5 to 65 days;

3)	**Test it, test it, test it:** the program tests all the conditions with all the stocks to backtest the investment strategy and prove it right or wrong.

## Functionalities

>**•	Data Acquisition:** Retrieves historical stock data for a predefined list of companies using the *yahoo_fin* library. You can modify the *companies* dictionary to include other stocks or assets you're interested in.

>**•	Donchian Channel Calculation:** Calculates rolling high and low values for a specified timeframe (weeks or days) using the *calculate_limits* function. This function adds columns representing the Donchian Channels (e.g., "50w-high", "20w-low") to the stock DataFrame.

>**•	Backtesting:** Performs backtesting simulations based on user-defined parameters:
>
>1.	Initial investment amount: default of USD 100.000
>
>2.	Donchian Channel high and low thresholds (in weeks or days)
>
>3.	Buy/Sell logic (reverse or normal Donchian Channel breakout)

>**•	Performance Evaluation:** Calculates and reports key performance metrics:
>1.	Earning (total profit)
>
>2.	ROI (Return on Investment) - total and annualized
>
>3.	Maximum Drawdown
>
>4.	Buy & Hold ROI (benchmark) for comparison


## Code Structure

The code is organized into several Python functions:
1.	**get_stockdata( ):** Fetches historical stock data for a given ticker symbol using *yahoo_fin* library.
2.	**calculate_limits( ):** Calculates Donchian Channel values for the specified timeframe (weeks or days) and adds them as columns to the DataFrame.
3.	**backtest( ):** The core function that performs backtesting simulations, calculates performance metrics, and returns a summary dictionary.
4.	**tests:** Demonstrates the usage of the above functions:

    - Downloads stock data for a sample company.

    - Calculates Donchian Channels with a specific timeframe.

    - Runs backtests for various parameter combinations and timeframes (weekly/daily).

    - Creates pandas DataFrames to consolidate backtest results.


## How to Use

1.	**Install Dependencies:** Ensure you have the required libraries (*pandas, yahoo_fin, datetime, termcolor*) installed. You can install them using *pip install pandas yahoo_fin datetime termcolor*.

2.	**Modify Parameters (Optional):**

    - Update the *companies* dictionary to include stocks or assets you want to analyze.
    - Adjust backtesting parameters within the script main loop (e.g., initial investment, thresholds, timeframe).

3.	**Run the Script:**

    - Execute the main script to test the companies with all the parameters.

## Conclusions

This project began investigating a investment strategy that promised to give +8000% return over a period of 30 years, using Apple Stock.

Let’s answer the initial questions:

1)	*Is this a legitimate strategy?* **The proposed strategy is a quite a lie**, for a few reasons:

    - The Annual ROI is 19%, compared to Buy & Hold the Stock ROI of 24%. That is, **it would be easier to just buy the stock and hold it for 30 years;**

    - **There are far better returns that could be achieved with the same strategy**, only by changing the parameters to 5w-high, 5w-low or to 5d-high, 5d-low. The returns could reach 44% and 307%, respectively;

    - No one would know *a priori* that Apple would be one of the best performing stocks in this period. Its Annual ROI outperformed even big players such as Microsoft (18%), Intel (8%) or IBM (9%). **But who could know that in 1994?**


2)	*Could it be repeated with other stocks?*

    - **YES!** Our main tests were to check it, and the answer is definitely yes.

    - Optimizing the parameters for 5w-high and 5w-low, the Annual ROI is significantly higher than Buy & Hold Annual ROI: Microsoft (25,7% vs 18%), Intel (22,3% vs 7,9%), GE (20,7% vs 3,2%). **This suggests that a purely Buy & Hold Strategy is a BAD Investment Strategy** – as you could get far better returns with simple algo strategies.

    - The results are positive even for stocks that performed very poorly in the period. For instance, AIG had a -73% return in the period, but the investment strategy of this program got 24,5% Annual ROI.

    - The average Annual ROI of the 20 Top S&P Stocks was 17% - way better than S&P Buy & Hold return of 8%.

3)	*Is this the best strategy considering we might change parameters of investment to optimize it?*

    - **No, the original strategy is bad.** It roughly takes the last year average (of high and low prices), and says that we should buy if reaches the high average, and sell if it reaches the low average. What we found out is that this timeframe is too slow to answer to market changes.

    - The best optimization we got in the weeks period was 5w-high and 5w-low, and in the days period was 5d-high and 5d-low.

4)	*How this strategy compares to simpler approaches like Buy & Hold of the actual stock, or Buy & Hold of S&P or QQQ index?*

    - **The optimized strategy outperforms Buy & Hold strategies of the actual stock or S&P (8%) and QQQ index (8%).**


## Further Enhancements

- Explore different technical indicators beyond the Donchian Channel.
- Implement more sophisticated buy/sell logic (e.g., combining indicators, stop-loss orders) and using options (call/put) strategies to increase the potential gain.
- Optimize parameters using machine learning techniques (e.g., grid search, genetic algorithms).
- Visualize backtesting results: we did some initial tests of plotting with matplotlib, but the outputs were not meaningful, they did not aggregate value to the analysis. So we left this out of the final version of the program.

## Backtesting Limitations

- Backtesting relies on historical data, which may not reflect future market conditions.
- It is essential to conduct thorough research and consider your risk tolerance before making real-world investments.

## References

1. The original article used as initial reference for this project:
    - [An Algo Trading Strategy which made +8,371%: A Python Case Study](https://levelup.gitconnected.com/an-algo-trading-strategy-which-made-8-371-a-python-case-study-58ed12a492dc)

2. A comprehensive guide to get stocks information from a free database:
    - [Yahoo Finance API – A Complete Guide](https://algotrading101.com/learn/yahoo-finance-api-guide/)
    
3. List of the Top S&P companies used in this project:
    - [List of 20 Top S&P companies in 1994](https://www.finhacker.cz/top-20-sp-500-companies-by-market-cap/#1994)

