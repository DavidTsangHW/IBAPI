#talib wrapper
from . import globaldf
import sys
import pandas

try:
    import talib
except ImportError:
    print('TALIB is not installed')

def read_pattern(df_tdata,pattern):
    sym = df_tdata['SYMBOL'].iloc[0]
    filepath = '\\Python\\data\\patterns\\'+ sym +'-Patterns.csv'
    df_pdata = globaldf.read(filepath)
    df_results = pandas.merge(df_tdata, df_pdata,on=['DATE'], how='left')
    pt = df_results[pattern].to_list()
    return pt

def recg_pattern(df_tdata,pattern):
    modulename = 'talib'
    if modulename not in sys.modules:
        pt = read_pattern(df_tdata,pattern)
    else:    
        pt = recg_pattern_talib(df_tdata,pattern)
    return pt        

def STOCH(df_tdata):

    opens = df_tdata['OPEN']
    highs = df_tdata['HIGH']
    lows = df_tdata['LOW']
    closes = df_tdata['CLOSE']

    slowk, slowd = talib.STOCH(highs, lows, closes)

    return slowk, slowd

def RSI(df_tdata,timeperiod=14):

    opens = df_tdata['OPEN']
    highs = df_tdata['HIGH']
    lows = df_tdata['LOW']
    closes = df_tdata['CLOSE']
          
    real = talib.RSI(closes, timeperiod)
    return real

def recg_pattern_talib(df_tdata,pattern):

        opens = df_tdata['OPEN']
        highs = df_tdata['HIGH']
        lows = df_tdata['LOW']
        closes = df_tdata['CLOSE']
        
        if pattern == 'CDL2CROWS':
                pt = talib.CDL2CROWS(opens,highs,lows,closes)
        if pattern == 'CDL3BLACKCROWS':
                pt = talib.CDL3BLACKCROWS(opens,highs,lows,closes)
        if pattern == 'CDL3INSIDE':
                pt = talib.CDL3INSIDE(opens,highs,lows,closes)
        if pattern == 'CDL3LINESTRIKE':
                pt = talib.CDL3LINESTRIKE(opens,highs,lows,closes)
        if pattern == 'CDL3OUTSIDE':
                pt = talib.CDL3OUTSIDE(opens,highs,lows,closes)
        if pattern == 'CDL3STARSINSOUTH':
                pt = talib.CDL3STARSINSOUTH(opens,highs,lows,closes)
        if pattern == 'CDL3WHITESOLDIERS':
                pt = talib.CDL3WHITESOLDIERS(opens,highs,lows,closes)
        if pattern == 'CDLABANDONEDBABY':
                pt = talib.CDLABANDONEDBABY(opens,highs,lows,closes)
        if pattern == 'CDLADVANCEBLOCK':
                pt = talib.CDLADVANCEBLOCK(opens,highs,lows,closes)
        if pattern == 'CDLBELTHOLD':
                pt = talib.CDLBELTHOLD(opens,highs,lows,closes)
        if pattern == 'CDLBREAKAWAY':
                pt = talib.CDLBREAKAWAY(opens,highs,lows,closes)
        if pattern == 'CDLCLOSINGMARUBOZU':
                pt = talib.CDLCLOSINGMARUBOZU(opens,highs,lows,closes)
        if pattern == 'CDLCONCEALBABYSWALL':
                pt = talib.CDLCONCEALBABYSWALL(opens,highs,lows,closes)
        if pattern == 'CDLCOUNTERATTACK':
                pt = talib.CDLCOUNTERATTACK(opens,highs,lows,closes)
        if pattern == 'CDLDARKCLOUDCOVER':
                pt = talib.CDLDARKCLOUDCOVER(opens,highs,lows,closes)
        if pattern == 'CDLDOJI':
                pt = talib.CDLDOJI(opens,highs,lows,closes)
        if pattern == 'CDLDOJISTAR':
                pt = talib.CDLDOJISTAR(opens,highs,lows,closes)
        if pattern == 'CDLDRAGONFLYDOJI':
                pt = talib.CDLDRAGONFLYDOJI(opens,highs,lows,closes)
        if pattern == 'CDLENGULFING':
                pt = talib.CDLENGULFING(opens,highs,lows,closes)
        if pattern == 'CDLEVENINGDOJISTAR':
                pt = talib.CDLEVENINGDOJISTAR(opens,highs,lows,closes)
        if pattern == 'CDLEVENINGSTAR':
                pt = talib.CDLEVENINGSTAR(opens,highs,lows,closes)
        if pattern == 'CDLGAPSIDESIDEWHITE':
                pt = talib.CDLGAPSIDESIDEWHITE(opens,highs,lows,closes)
        if pattern == 'CDLGRAVESTONEDOJI':
                pt = talib.CDLGRAVESTONEDOJI(opens,highs,lows,closes)
        if pattern == 'CDLHAMMER':
                pt = talib.CDLHAMMER(opens,highs,lows,closes)
        if pattern == 'CDLHANGINGMAN':
                pt = talib.CDLHANGINGMAN(opens,highs,lows,closes)
        if pattern == 'CDLHARAMI':
                pt = talib.CDLHARAMI(opens,highs,lows,closes)
        if pattern == 'CDLHARAMICROSS':
                pt = talib.CDLHARAMICROSS(opens,highs,lows,closes)
        if pattern == 'CDLHIGHWAVE':
                pt = talib.CDLHIGHWAVE(opens,highs,lows,closes)
        if pattern == 'CDLHIKKAKE':
                pt = talib.CDLHIKKAKE(opens,highs,lows,closes)
        if pattern == 'CDLHIKKAKEMOD':
                pt = talib.CDLHIKKAKEMOD(opens,highs,lows,closes)
        if pattern == 'CDLHOMINGPIGEON':
                pt = talib.CDLHOMINGPIGEON(opens,highs,lows,closes)
        if pattern == 'CDLIDENTICAL3CROWS':
                pt = talib.CDLIDENTICAL3CROWS(opens,highs,lows,closes)
        if pattern == 'CDLINNECK':
                pt = talib.CDLINNECK(opens,highs,lows,closes)
        if pattern == 'CDLINVERTEDHAMMER':
                pt = talib.CDLINVERTEDHAMMER(opens,highs,lows,closes)
        if pattern == 'CDLKICKING':
                pt = talib.CDLKICKING(opens,highs,lows,closes)
        if pattern == 'CDLKICKINGBYLENGTH':
                pt = talib.CDLKICKINGBYLENGTH(opens,highs,lows,closes)
        if pattern == 'CDLLADDERBOTTOM':
                pt = talib.CDLLADDERBOTTOM(opens,highs,lows,closes)
        if pattern == 'CDLLONGLEGGEDDOJI':
                pt = talib.CDLLONGLEGGEDDOJI(opens,highs,lows,closes)
        if pattern == 'CDLLONGLINE':
                pt = talib.CDLLONGLINE(opens,highs,lows,closes)
        if pattern == 'CDLMARUBOZU':
                pt = talib.CDLMARUBOZU(opens,highs,lows,closes)
        if pattern == 'CDLMATCHINGLOW':
                pt = talib.CDLMATCHINGLOW(opens,highs,lows,closes)
        if pattern == 'CDLMATHOLD':
                pt = talib.CDLMATHOLD(opens,highs,lows,closes)
        if pattern == 'CDLMORNINGDOJISTAR':
                pt = talib.CDLMORNINGDOJISTAR(opens,highs,lows,closes)
        if pattern == 'CDLMORNINGSTAR':
                pt = talib.CDLMORNINGSTAR(opens,highs,lows,closes)
        if pattern == 'CDLONNECK':
                pt = talib.CDLONNECK(opens,highs,lows,closes)
        if pattern == 'CDLPIERCING':
                pt = talib.CDLPIERCING(opens,highs,lows,closes)
        if pattern == 'CDLRICKSHAWMAN':
                pt = talib.CDLRICKSHAWMAN(opens,highs,lows,closes)
        if pattern == 'CDLRISEFALL3METHODS':
                pt = talib.CDLRISEFALL3METHODS(opens,highs,lows,closes)
        if pattern == 'CDLSEPARATINGLINES':
                pt = talib.CDLSEPARATINGLINES(opens,highs,lows,closes)
        if pattern == 'CDLSHOOTINGSTAR':
                pt = talib.CDLSHOOTINGSTAR(opens,highs,lows,closes)
        if pattern == 'CDLSHORTLINE':
                pt = talib.CDLSHORTLINE(opens,highs,lows,closes)
        if pattern == 'CDLSPINNINGTOP':
                pt = talib.CDLSPINNINGTOP(opens,highs,lows,closes)
        if pattern == 'CDLSTALLEDPATTERN':
                pt = talib.CDLSTALLEDPATTERN(opens,highs,lows,closes)
        if pattern == 'CDLSTICKSANDWICH':
                pt = talib.CDLSTICKSANDWICH(opens,highs,lows,closes)
        if pattern == 'CDLTAKURI':
                pt = talib.CDLTAKURI(opens,highs,lows,closes)
        if pattern == 'CDLTASUKIGAP':
                pt = talib.CDLTASUKIGAP(opens,highs,lows,closes)
        if pattern == 'CDLTHRUSTING':
                pt = talib.CDLTHRUSTING(opens,highs,lows,closes)
        if pattern == 'CDLTRISTAR':
                pt = talib.CDLTRISTAR(opens,highs,lows,closes)
        if pattern == 'CDLUNIQUE3RIVER':
                pt = talib.CDLUNIQUE3RIVER(opens,highs,lows,closes)
        if pattern == 'CDLUPSIDEGAP2CROWS':
                pt = talib.CDLUPSIDEGAP2CROWS(opens,highs,lows,closes)
        if pattern == 'CDLXSIDEGAP3METHODS':
                pt = talib.CDLXSIDEGAP3METHODS(opens,highs,lows,closes)

        return pt


def getcdlpatterns():

        pat = []

        pat.append("CDL2CROWS")
        pat.append("CDL3BLACKCROWS")
        pat.append("CDL3INSIDE")
        pat.append("CDL3LINESTRIKE")
        pat.append("CDL3OUTSIDE")
        pat.append("CDL3STARSINSOUTH")
        pat.append("CDL3WHITESOLDIERS")
        pat.append("CDLABANDONEDBABY")
        pat.append("CDLADVANCEBLOCK")
        pat.append("CDLBELTHOLD")
        pat.append("CDLBREAKAWAY")
        pat.append("CDLCLOSINGMARUBOZU")
        pat.append("CDLCONCEALBABYSWALL")
        pat.append("CDLCOUNTERATTACK")
        pat.append("CDLDARKCLOUDCOVER")
        pat.append("CDLDOJI")
        pat.append("CDLDOJISTAR")
        pat.append("CDLDRAGONFLYDOJI")
        pat.append("CDLENGULFING")
        pat.append("CDLEVENINGDOJISTAR")
        pat.append("CDLEVENINGSTAR")
        pat.append("CDLGAPSIDESIDEWHITE")
        pat.append("CDLGRAVESTONEDOJI")
        pat.append("CDLHAMMER")
        pat.append("CDLHANGINGMAN")
        pat.append("CDLHARAMI")
        pat.append("CDLHARAMICROSS")
        pat.append("CDLHIGHWAVE")
        pat.append("CDLHIKKAKE")
        pat.append("CDLHIKKAKEMOD")
        pat.append("CDLHOMINGPIGEON")
        pat.append("CDLIDENTICAL3CROWS")
        pat.append("CDLINNECK")
        pat.append("CDLINVERTEDHAMMER")
        pat.append("CDLKICKING")
        pat.append("CDLKICKINGBYLENGTH")
        pat.append("CDLLADDERBOTTOM")
        pat.append("CDLLONGLEGGEDDOJI")
        pat.append("CDLLONGLINE")
        pat.append("CDLMARUBOZU")
        pat.append("CDLMATCHINGLOW")
        pat.append("CDLMATHOLD")
        pat.append("CDLMORNINGDOJISTAR")
        pat.append("CDLMORNINGSTAR")
        pat.append("CDLONNECK")
        pat.append("CDLPIERCING")
        pat.append("CDLRICKSHAWMAN")
        pat.append("CDLRISEFALL3METHODS")
        pat.append("CDLSEPARATINGLINES")
        pat.append("CDLSHOOTINGSTAR")
        pat.append("CDLSHORTLINE")
        pat.append("CDLSPINNINGTOP")
        pat.append("CDLSTALLEDPATTERN")
        pat.append("CDLSTICKSANDWICH")
        pat.append("CDLTAKURI")
        pat.append("CDLTASUKIGAP")
        pat.append("CDLTHRUSTING")
        pat.append("CDLTRISTAR")
        pat.append("CDLUNIQUE3RIVER")
        pat.append("CDLUPSIDEGAP2CROWS")
        pat.append("CDLXSIDEGAP3METHODS")

        return pat
