# IB API TWS Python API - PositionCheck
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

class CheckPositionApp(EWrapper, EClient):
    
    posns = []
    account = ''
    
    df_pos = pandas.DataFrame()    

    def __init__(self):
        EClient.__init__(self, self)

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        self.account = account[0] + account[2:4]
        self.posns.append((self.account,contract.symbol, contract.currency, contract.exchange, position))

    def nextValidId(self,orderId):
        self.reqPositions()
        self.start()

    def execDetails(self,reqId,contract,execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)        

    def start(self):
        pass

    def error(self,reqId,errorCode,errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def positionEnd(self):   
        if self.posns:
            self.df_pos = pandas.DataFrame(self.posns, columns = ['ACCOUNT','SYMBOL' , 'CURRENCY','EXCH','POSITION'])
            self.df_pos = self.df_pos.sort_values('SYMBOL')
            print(self.df_pos.head(100))
            self.df_pos.to_sql('Position',con2,if_exists='replace',index=False)
        self.done = True
        self.disconnect()
        return

def main():

    app = CheckPositionApp()
    app.connect("127.0.0.1", 7497, 1001)
    app.run()
    return


if __name__ == '__main__':
    main()
    
