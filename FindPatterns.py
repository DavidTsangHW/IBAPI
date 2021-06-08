import pandas
import sys

from lib import talibw

import talib
import sqlite3

wdir = '\\Python\\data\\'
afile = wdir + 'tatest.db'

con = sqlite3.connect(afile)
cursor = con.cursor()

def main():

    patterns = talibw.getcdlpatterns()

    sql = "drop table if exists patterns"
    con.execute(sql)
    con.commit()

    sql = "select distinct symbol from historical"
    df_symbols = pandas.read_sql(sql,con)

    ls_symbols = df_symbols['SYMBOL'].tolist()

    print(str(len(ls_symbols)) + " symbols")
    
    for sym in ls_symbols:

            sql = "select * from historical where SYMBOL = '" + sym + "'"
            df_tdata = pandas.read_sql(sql,con)
            
            df_tdata['SYMBOL'] = sym
            df_tdata['DATE'] = pandas.to_datetime(df_tdata['DATE']).apply(lambda x: x.date())

            for p in patterns:
                pt = talibw.recg_pattern(df_tdata,p)            
                df_tdata[p] = pt

            sma = [3,5,7,9,11,25]

            close = df_tdata['CLOSE']

            for s in sma:
                df_tdata['SMA' + str(s)] = talib.SMA(close, s)
                
            df_tdata.to_sql('patterns', con, if_exists='append', index=False)                
            
            print(sym + ' Completed')

argv = sys.argv
cargv = len(argv)

main()

con.close()        


