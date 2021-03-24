# IB API TWS Python API - Place Order 
# Author: David Tsang
# GitHub: https://davidtsanghw.github.io
# 23 March 2021

# TERM OF USE
#
# VERY IMPORTANT!!!!
#
# TRADER WORK STATION (TWS) MUST BE LOGGED IN SUCCESSFULY WHEN RUNNING THIS PROGRAM
#
# MAKE SURE YOU ARE CONNECTING A PAPER ACCOUNT WHEN TEST AND DEBUGGING
#
# THE AUTHOR ACCEPTS NO RESPONSIBILITY FOR THE USE OF THIS PROGRAM. USE OF THIS PROGRAM IS ENTIRELY AT THE USER'S OWN RISK

# This program is in Python 3.9

# Prerequisites
# 1. Download and install TWS
# 2. Download and install IB API
# 3. Configure TWS

# Configure TWS
# TWS > Global Configuration > API > Settings >
# 1. Enable Active X and Socket Clients > Enable
# 2. Socket port: 7497
# 3. Read-only API > disable
# 4. Allow connections from localhost only > Disable
# 5. Allow connections from localhost only > Trusted IPs > Create > Enter 127.0.0.1
#
# ******  4 and 5 disable confirmation when connecting TWS    


from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import *
from ibapi.ticktype import TickTypeEnum

from threading import Timer

import os

import pandas
import numpy

from datetime import date

import datetime as dt

import math

import urllib.request

orderFiles = []

#Tradebot 1
orderFiles.append('ordersT1_30AUD.csv')

#Lot size not handled in this loader
#orderFiles.append('ordersT1_30HKD.csv')

orderFiles.append('ordersT1_30USD.csv')

#Tradebot 5
orderFiles.append('ordersT5_30AUD.csv')

#Tradebot 6
orderFiles.append('ordersT6_30AUD.csv')

orderFile = 'ordersT5_30AUD.csv'
for orderFile in orderFiles:
    url = 'https://davidtsanghw.github.io/orderfiles/' + orderFile
    urllib.request.urlretrieve(url, orderFile)

transmit = False

class PlaceOrderApp(EWrapper, EClient):

    posns = []
    filepath = ''
    account = ''
    LotAmt = 0
    
    nextOrderId = 1000

    df_pos = pandas.DataFrame()    

    def __init__(self):
        EClient.__init__(self, self)

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        self.account = account[0] + account[2:4]
        self.LotAmt = 10000
        if contract.currency == 'AUD':
            self.LotAmt = self.LotAmt / 6
        elif contract.currency == 'USD':
            self.LotAmt = self.LotAmt / 7.8
            
        self.posns.append((self.account,contract.symbol, position,0,0))
        

    def nextValidId(self,orderId):
        self.reqAllOpenOrders()        
        self.nextOrderId = orderId
        self.reqPositions()
        self.start()

    def execDetails(self,reqId,contract,execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)        

    def start(self):
        pass
        
    def stop(self):
        self.done = True
        self.disconnect()

    def error(self,reqId,errorCode,errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def positionEnd(self):   
        if self.posns:
            self.df_pos = pandas.DataFrame(self.posns, columns = ['ACCOUNT','SYMBOL' , 'POSITION','BUY','SELL'])
            self.placeBuyOrders()
            self.df_pos = self.df_pos.sort_values('SYMBOL')
            print(self.df_pos.head(100))            
        self.disconnect()

    def placeBuyOrders(self):

        df_orders = pandas.DataFrame()
        
        for orderFile in orderFiles:
            df_read = pandas.read_csv(orderFile)
            print('Reading ' + orderFile)
            if len(df_orders) == 0:
                df_orders = df_read
            else:
                df_orders = pandas.concat([df_orders, df_read])

        df_orders["P.SYMBOL"]= df_orders["P.SYMBOL"].str.replace("ASX-","")
        df_orders["P.SYMBOL"]= df_orders["P.SYMBOL"].str.replace(".HK","")
        df_orders = df_orders[(df_orders['STATUS'] == 'OPEN')]
        df_orders = df_orders[(df_orders['NEW'] == '+')]
        df_orders = df_orders.sort_values('P.DATE')

        contractOrders = []

        if len(df_orders) == 0:
            print('No buy order')
        
        for i in range(0,len(df_orders)):

            order = df_orders.iloc[i]

            #Searching Contract Description
            #https://interactivebrokers.github.io/tws-api/contracts.html
            contract = Contract()
            contract.symbol = df_orders.iloc[i]['P.SYMBOL']
            contract.currency= df_orders.iloc[i]['CURRENCY']

            exch = 'SMART'
            if df_orders.iloc[i]['CURRENCY'] == 'HKD':
                exch = 'SEHK'                
            contract.secType = "STK"
            contract.exchange = exch
            contract.primaryExchange = exch

            tradingQuantity = max([1,math.floor(self.LotAmt / df_orders.iloc[i]['T.PRICE'])])

            order = Order()
            order.action = "BUY"
            order.totalQuantity = tradingQuantity
            order.orderType = "MKT"
            order.orderId = self.nextOrderId

            print(contract)

            order.transmit = transmit
            self.nextOrderId = self.nextOrderId + 1        
            self.placeOrder(order.orderId, contract, order)

            takeProfit = Order()
            takeProfit.action = "SELL"
            takeProfit.totalQuantity = tradingQuantity
            takeProfit.orderType = "LMT"
            takeProfit.lmtPrice = df_orders.iloc[i]['EST.S.PRICE']
            takeProfit.parentId = order.orderId
            takeProfit.orderId = self.nextOrderId
            self.nextOrderId = self.nextOrderId + 1            
            
            #Specifies whether the order will be transmitted by TWS. If set to false, the order will be created at TWS but will not be sent.
            takeProfit.transmit = transmit
            #The trade's "Good Till Date," format "YYYYMMDD hh:mm:ss (optional time zone)".
            takeProfit.tif = "GTD"
            takeProfit.goodTillDate = df_orders.iloc[i]['EST.S.DATE'].replace("-","") + ' 23:59:59 EST'
            
            self.placeOrder(takeProfit.orderId, contract, takeProfit)            

def main():

    app = PlaceOrderApp()
    app.connect("127.0.0.1", 7497, 100)
    app.run()

    return


if __name__ == '__main__':

    main()
    
