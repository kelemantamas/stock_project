# python2.7
# alphavantage api key: MO16CXFV5F3OGWX1
# intraday series, every 5 min, stockchange

import config
import requests
import mysql.connector
from mysql.connector import errorcode
import datetime
import time

conn = mysql.connector.connect(host=config.db['host'], user=config.db['user'], password=config.db['password'],
                               db=config.db['dbname'])
manage_table = conn.cursor()

API_URL = "https://www.alphavantage.co/query"
API_KEY = "MO16CXFV5F3OGWX1"

# creating database table (data), if not exists
try:
    manage_table.execute(
        "CREATE TABLE `" + config.db[
            'dbname'] + "`.`data` (`symbol` VARCHAR(10) NOT NULL, `datentime` DATETIME(6) NOT NULL , `open` FLOAT(10) NOT NULL , `high` FLOAT(10) NOT NULL , `low` FLOAT(10) NOT NULL , `close` FLOAT(10) NOT NULL , PRIMARY KEY (`symbol`, `datentime`))")
    print "Table 'data' created"
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print "Table 'data' already exists."
    else:
        print err.msg

actualtime = datetime.datetime.now().time()
starttime = datetime.datetime.strptime("14:00:00", "%H:%M:%S").time()
endtime = datetime.datetime.strptime("22:00:00", "%H:%M:%S").time()
# 14 - 22
# endless loop
while True:
    if actualtime > starttime and actualtime < endtime:
        for s in config.symb:
            symbol = s

            data = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": "5min",
                "outputsize": "full",
                # "datatype": "json",
                # datatype is optional, json is the default value, csv is the other one
                "apikey": API_KEY
            }

            try:
                response = requests.get(API_URL, data)
                data = response.json()
            except requests.exceptions.RequestException as req_err:
                print "Request error: {}".format(req_err)

            insert_data = (
                "INSERT INTO `data` " "(`symbol`, `datentime`, `open`, `high`, `low`, `close`)" "VALUES (%s, %s, %s, %s, %s, %s)")
            a = (data['Time Series (5min)'])

            keys = (a.keys())

            for key in keys:
                datentime = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
                open = float(a[key]['1. open'])
                high = float(a[key]['2. high'])
                low = float(a[key]['3. low'])
                close = float(a[key]['4. close'])
                stock_data = (symbol, datentime, open, high, low, close)

                try:
                    manage_table.execute(insert_data, stock_data)
                    print "Row inserted: ", symbol, " - ", datentime
                except mysql.connector.Error as err:
                    print "Unsuccessfull insertion: ", err.msg

                conn.commit()
            print datetime.datetime.now().time()
            print "Sleeping for 15 sec"
            time.sleep(15)
        print "Delaying. Next loop starts in 60 min"
        time.sleep(3600)
    else:
        print "Delaying. Next loop starts at 14:00:00"
        time.sleep(3600)

manage_table.close()
conn.close()
# print data
