# IB API TWS Python API - Check Open Order
# Author: David Tsang
# GitHub: https://davidtsanghw.github.io
# 15 May 2021

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

import os

import pandas
import numpy

from datetime import date

import datetime as dt

import math

import sqlite3

wdir = '\\Python\\data\\'
ofile = wdir + 'orderfx.db'
con2 = sqlite3.connect(ofile)
cursor2 = con2.cursor()

class CheckOrderApp(EWrapper, EClient):

    posns = []
    
    df_pos = pandas.DataFrame()    

    def __init__(self):
        EClient.__init__(self, self)

    def openOrder(self, orderId, contract, order, orderState):
        print(contract.symbol)
        ls_order = str(order).split(' ')
        print(ls_order[2])
        print(ls_order[3].split('@')[0])
        print(ls_order[3].split('@')[1])

        self.posns.append((contract.symbol, contract.currency, contract.exchange, ls_order[2], ls_order[3].split('@')[0],ls_order[3].split('@')[1]))
            
    def orderStatus(self, orderId, status, filled, remaining,
                         avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", filled,
           "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
           "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",
           lastFillPrice, "ClientId:", clientId, "WhyHeld:",
           whyHeld, "MktCapPrice:", mktCapPrice)        

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        self.account = account[0] + account[2:4]
        self.posns.append((self.account,contract.symbol, position))

    def nextValidId(self,orderId):
        self.reqAllOpenOrders()
        self.start()

    #def execDetails(self,reqId,contract,execution):
        #print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)        

    def start(self):
        pass

    def error(self,reqId,errorCode,errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def openOrderEnd(self):
        if self.posns:
            self.df_pos = pandas.DataFrame(self.posns, columns = ['SYMBOL' , 'CURRENCY','EXCH','TYPE','QUANTITY','PRICE'])
            self.df_pos = self.df_pos.sort_values('SYMBOL')
            print(self.df_pos.head(100))
            self.df_pos.to_sql('OpenOrder',con2,if_exists='replace',index=False)

            sql = "select a.SYMBOL, POSITION, b.QUANTITY from position a left outer join (select SYMBOL, sum(QUANTITY) as [QUANTITY] from [OpenOrder] group by symbol) b on a.SYMBOL = b.SYMBOL"
            
            
        self.done = True
        self.disconnect()

def main():

    app = CheckOrderApp()
    app.connect("127.0.0.1", 7497, 1001)
    app.run()
    return


if __name__ == '__main__':
    main()
    
