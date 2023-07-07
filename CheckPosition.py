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
# MAKE SURE YOU ARE CONNECTING A PAPER ACCOUNT FOR TEST AND DEBUG
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
# 2. Socket port: Same as Parms.csv
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

import sys

import pandas
import numpy

from datetime import date

import datetime as dt

import math

import sqlite3

import Parms

argv = sys.argv

longshort = argv[1]

wdir = ''
ofile = wdir + longshort + 'orderfx.db'
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
        self.df_pos = pandas.DataFrame(self.posns, columns = ['ACCOUNT','SYMBOL' , 'CURRENCY','EXCH','POSITION'])
        self.df_pos = self.df_pos.sort_values('SYMBOL')
        self.df_pos.to_sql('Position',con2,if_exists='replace',index=False)
        print(self.df_pos)
        self.done = True
        self.disconnect()
        return

def main():

    app = CheckPositionApp()
    port = int(Parms.getParm(longshort + 'PORT')) 
    app.connect("127.0.0.1", port, 1001)
    app.run()
    return


if __name__ == '__main__':
    main()
    con2.close()
    
