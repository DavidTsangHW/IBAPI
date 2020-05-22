# IB API TWS Python API - Place Order
# Author: David Tsang
# GitHub: https://davidtsanghw.github.io
# 22 May 2020

# TERM OF USE
#
# VERY IMPORTANT!!!!
#
# TRADER WORK STATION (TWS) MUST BE LOGGED IN SUCCESSFULY WHEN RUNNING THIS PROGRAM
#
# MAKE SURE YOU ARE CONNECTING A PAPER ACCOUNT WHEN TEST AND DEBUGGING
#
# THE AUTHOR ACCEPTS NO RESPONSIBILITY FOR THE USE OF THIS PROGRAM. USE OF THIS PROGRAM IS ENTIRELY AT THE USER'S OWN RISK

# This program is in Python 3.7

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


class TestApp(EWrapper, EClient):

    contract = Contract()
    order = Order()

    def __init__(self):
        EClient.__init__(self, self)

    def setMyOrder(self,mContract,mOrder):
        self.contract = mContract
        self.order = mOrder        

    def nextValidId(self,orderId):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self,orderId,contract,order,orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self,reqId,contract,execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)        

    def start(self):
        self.placeOrder(self.nextOrderId, self.contract, self.order)

    def stop(self):
        self.done = True
        self.disconnect()

    def error(self,reqId,errorCode,errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    #def tickPrice(self,reqId,tickType,price,attrib):
    #    print("Tick Price. Ticker Id:",reqId,"tickType:",TickTypeEnum.to_str(tickType),"Price:",price,end= ' ')        

    #def tickSize(self,reqId,tickType,size):
    #    print("Tick Size. Ticker Id:",reqId,"tickType:",TickTypeEnum.to_str(tickType),"Size:",size)

def main():

    
    app = TestApp()

    app.connect("127.0.0.1", 7497, 0)

    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency= "USD"
    contract.primaryExchange = "NASDAQ"

    order = Order()
    order.action = "BUY"
    order.totalQuantity = 30
    order.orderType = "LMT"
    order.lmtPrice = 250

    app.setMyOrder(contract,order)
    
    Timer(3, app.stop).start()

    app.run()


if __name__ == '__main__':
    main()

    
