# IB API TWS Python API - Getting Historical Data
# Author: David Tsang
# GitHub: https://davidtsanghw.github.io
# IB Page
# https://interactivebrokers.github.io/tws-api/historical_bars.html
# 15 May 2021

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


import time
from datetime import datetime
import pandas as pd
import sqlite3
import Parms

currency = Parms.getParm('CURRENCYPAIR')
durationString = Parms.getParm('DURATIONSTRING')
barsizeSetting = Parms.getParm('BARSIZESETTING')
queryTime = Parms.getParm('QUERYTIME')
ls_currencies = [currency]

#Physical file
wdir = ''
afile = wdir + str(Parms.getParm('FXDB'))
con = sqlite3.connect(afile)
cursor = con.cursor()

#Memory cache
mfile = ':memory:'
mCon = sqlite3.connect(mfile)
mCursor = mCon.cursor()

#Remove existing data to ensure the program is processing latest data in live run
for currency in ls_currencies:
    sql = "drop table if exists [" + currency + "]"
    con.execute(sql)    

class GetHistoricalApp(EWrapper,EClient):
    def __init__(self):
        #EWrapper.__init__(self)
        EClient.__init__(self,self)
        self.data = [] #Initialize variable to store candle
        self.FX_df={}
        self.pairs_list= ls_currencies
        self.count=0        
        return

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
        self.start()
            

    def error(self,reqId,errorCode,errorString):
        print('Error: ',reqId,' ',errorCode,' ',errorString)
        return

    def historicalData(self, reqId:int, bar):
        #print(f'Time: {bar.date} Open:{bar.open} High:{bar.high} Low:{bar.low} Close: {bar.close} Volume: {bar.volume}')
        self.FX_df[reqId].append([bar.date, bar.open,bar.high,bar.low,bar.close,bar.volume])
        return

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        print( datetime.fromtimestamp(int(datetime.now().timestamp())),'HistoricalDataEnd. ReqId:', reqId, 'from', start, 'to', end)

        self.FX_df[reqId] = pd.DataFrame(self.FX_df[reqId],columns=['DATETIME','OPEN','HIGH','LOW', 'CLOSE','VOLUME'])
        self.FX_df[reqId].to_sql('RAW', con, if_exists='replace', index = False)   

        self.FX_df[reqId]['DATETIME'] = pd.to_datetime(self.FX_df[reqId]['DATETIME'],unit='s')        
        self.FX_df[reqId]['SYMBOL'] = self.pairs_list[reqId]

        #Write to in-memory database for processing
        self.FX_df[reqId].to_sql(self.pairs_list[reqId], mCon, if_exists='replace', index=False)                
        sql = 'select *, Date(DateTime) as [DATE], Time(DateTime) as [TIME] from [' + self.pairs_list[reqId] + ']'
        self.FX_df[reqId] = pd.read_sql(sql, mCon)
        self.FX_df[reqId].to_sql(self.pairs_list[reqId], con, if_exists='replace', index = False)                   

        print(self.pairs_list[reqId] + ' ' + str(len(self.FX_df[reqId])) + ' records')
        self.count+=1

        if self.count==len(self.pairs_list):
            self.stop()

        return

    def start(self):
            
        for pair in range(len(self.pairs_list)):
            contract=FX_order(self.pairs_list[pair])
            self.FX_df[pair]=[]
            print(contract)
            print(pair)
            self.reqHistoricalData(pair,contract,queryTime,durationString,barsizeSetting,'MIDPOINT',0,2,False,[]) #request historical data

        return


    def stop(self):
        for pair in range(len(self.pairs_list)):
            self.cancelHistoricalData(pair)
        time.sleep(5)
        print('disconnecting')
        self.disconnect()
        return

def FX_order(symbol):
     contract = Contract()
     contract.symbol = symbol[:3]
     contract.secType = 'CASH'
     contract.exchange = 'IDEALPRO'
     contract.currency = symbol[3:]
     return contract

def GetContract(symbol):

#5 Feb 2022
#Product	Try this:
#10-year US Treasury Bond yield	TNX index on CBOE
#5-year bond index	FVX index on CBOE
#30-year bond index	TYX index on CBOE
     contract = Contract()
     contract.symbol = 'TYX'
     contract.secType = 'IND'
     contract.exchange = 'CBOE'
     contract.currency = 'USD'
     return contract

def main():
    app = GetHistoricalApp()
    
    port = int(Parms.getParm('DATAPORT'))
    app.connect('127.0.0.1',port,1001)
    app.run()

    return    

if __name__=="__main__":
    main()
