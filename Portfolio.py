"""
Portfolio.py

Author: Brian McKenna 

This file defines a Portfolio class which is meant to represent a basket portfolio of
arbritrary amounts of shares of different stocks. This class also allows a variety 
of calculations/ analytics to be performed on said portfolio. 

A Portfolio object takes multiple parameters: a dictionary of stock tickers and their shares: 
"basket", a start and end date as DateTime objects, and an index ticker to serve as a benchmark 
index.
"""
# Make necessary imports
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt 

class Portfolio:
    """A basket portfolio of select stocks, over the timeframe from start to end
    using index indx as a benchmark"""
    def __init__(self, basket, start, end, indx):
        self.sharedyct = basket
        self.start = start
        self.end = end 
        self.indx = indx

        # Creating pandas dataframe "data" which contains the daily price of the total portfolio as well 
        # as the daily total price amount of each respective stock in the portfolio
        keys = list(self.sharedyct.keys())
        data = pd.DataFrame(web.DataReader(keys[0], "yahoo", start, end)["Close"]) * self.sharedyct[keys[0]]
        data[keys[0]] = data["Close"]
        for count in range(1, len(self.sharedyct)):
            data1 = web.DataReader(keys[count], "yahoo", start, end)["Close"] * self.sharedyct[keys[count]]
            data["Close"] += data1
            data[keys[count]] = data1
        self.data = data
        

        # Creating pandas dataframes "data1" and "data2", 
        # "data1" replicates "data" but instead of closing price, it 
        # contains daily logarithmic returns of the total portfolio and each stock. "data1" also contains an
        # additional column "Weighted Return" which is the weighted average of each stocks returns relative to
        # that stock's weight in the portfolio that dat

        # data2 is a two-column dataframe with the closing price of the selected benchmark index as well as its 
        # daily returns


        data1 = self.data.copy().reset_index(drop = True)

        data2 = pd.DataFrame(web.DataReader(self.indx, "yahoo", self.start, self.end)["Close"])
        data2 = data2.reset_index(drop = True)

        data2["Index Daily Return"] = 0.0
        data1["Daily Return"] = 0.0
        for i in self.sharedyct.keys():
            data1[i + " Daily Return"] = 0.0
        data1["Weighted Return"] = 0.0


        for count in range(1, len(data1)):
            curTotal = data1.iloc[count]["Close"]
            prevTotal = data1.iloc[count - 1]["Close"]
            data1.at[count, "Daily Return"] = np.log((curTotal / prevTotal))

            curTotal2 = data2.iloc[count]["Close"]
            prevTotal2 = data2.iloc[count - 1]["Close"]
            data2.at[count, "Index Daily Return"] = np.log((curTotal2 / prevTotal2))

            for i in self.sharedyct.keys():
                curStock = data1.iloc[count][i]
                prevStock = data1.iloc[count - 1][i]
                dlyRtrn = np.log((curStock / prevStock))
                data1.at[count, i + " Daily Return"] = dlyRtrn
                weight = curStock / curTotal
                data1.at[count, "Weighted Return"] += (weight * dlyRtrn)


        lyst = list(self.sharedyct.keys())
        lyst.append("Close")
        data1 = data1.drop(columns = lyst)

        #"data1" and "data2" are made attributes of the Portfolio objects as 
        # "retData" and "indxData" respectively
        self.retData = data1
        self.indxData = data2


        
    
    def averageDailyReturn(self):
        """Calculates the geometric average return iteratively"""
        time = (self.end - self.start).days
        geoprod = 1
        for count in range(1, len(self.retData)):
            geoprod *= (1 + self.retData.at[count, "Daily Return"])
        geomean = (geoprod ** (1 / time)) - 1
        return geomean
        
    
    def volatility(self):
        """Calculates volatility by taking standard deviation of weoghted returns"""
        vol = np.std(self.retData["Weighted Return"])
        return vol
    
    def riskRatio(self):
        """Calculates ratio of (portfolio volatility / benchmark volatility)"""
        indxVol = np.std(self.indxData["Index Daily Return"])
        return self.volatility() / indxVol
    
    def marginalVolatility(self, ticker, shares):
        """Creates a new portfolio with "shares" additional shares of "ticker" stock, 
        finds its volatility, and subtracts the original portfolio volatility from
        the new"""
        newDyct = self.sharedyct.copy()
        if ticker in list(self.sharedyct.keys()):
            newDyct[ticker] += shares
        else:
            newDyct[ticker] = shares
        
        newPort = Portfolio(newDyct, self.start, self.end, self.indx)
        newVol = newPort.volatility()
        volDiff = newVol - self.volatility()
        
        return volDiff
    
    def maxDrawDown(self):
        """Calculates the maximum distance of a stock price from its running maximum"""
        priceMax = 0
        distMax = 0
        for count in range(len(self.data)):
            date = self.data.index.tolist()[count]
            priceMax = max(priceMax, self.data.at[date, "Close"])
            dist = priceMax - self.data.at[date, "Close"]
            distMax = max(distMax, dist)
        return distMax


