import pandas
import sqlite3

def getParm(parm):

    df_parms = pandas.DataFrame()  
    df_parms = pandas.read_csv('parms.csv')

    ofile = ':memory:'
    oCon = sqlite3.connect(ofile)
    oCursor = oCon.cursor()
    df_parms.to_sql('PARMS', oCon, if_exists='replace', index=False)

    val = ''

    sql = "select * from parms where Parms = '" + parm + "' limit 1"
    df_ret = pandas.read_sql(sql, oCon)
    
    if len(df_ret) > 0:
        val = df_ret['Value'].iloc[0]
    
    return val

def getParms():
    df_ret = pandas.read_csv('parms.csv')
    return df_ret

def getTradeTime():
    df_ret = pandas.read_csv('TradeTime.csv')
    return df_ret
