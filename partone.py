import requests
import datetime
import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = "22c395cec196961c2ee209164e4ca0a0"

tgtURL =  "https://api.forecast.io/forecast/" + API_KEY + "/"

def init_db():
	con = lite.connect('/Users/kuttush/Desktop/Spongebob/Thinkful/DataScience/DS_Project/latlong.db')
	cur = con.cursor()
	tgtCreateTableQuery = '''CREATE TABLE IF NOT EXISTS hourly (apparentTemperature REAL,
	summary TEXT,
        icon TEXT,
        temperature REAL,
	humidity REAL,
        windSpeed REAL,
        time INT,
	latitude REAL,
        longitude REAL,
        UNIQUE(latitude,longitude,time) ON CONFLICT REPLACE )'''
	with con:
		cur.execute(tgtCreateTableQuery)
	con.commit()
	con.close()

#the following info is obtained from http://www.csgnetwork.com/llinfotable.html
countries = {"USA": '39.91,77.02',
             "United States of Virgin Islands": '18.21, 64.56',
	     "India": '28.37,77.13',
             "UK": '51.36, 00.05',
             "Canada": '45.27, 75.42',
             "Australia": '35.15, 149.08',
             "New Zealand": '41.19, 174.46',
             "South Africa": '25.44, 28.12',
             "Jamaica": '18.00, 76.50',
	     "Kenya": '1.17, 36.48',
             "Zambia": '15.28, 28.16',
             "Zimbabwe": '17.43, 31.02'}

def init_country_table():
	con = lite.connect('/Users/kuttush/Desktop/Spongebob/Thinkful/DataScience/DS_Project/latlong.db')
        cur = con.cursor()
	tgtCreateTableQuery = '''CREATE TABLE IF NOT EXISTS countries(name TEXT, latitude REAL,
        longitude REAL, UNIQUE(name, latitude, longitude) ON CONFLICT REPLACE)'''
        cur.execute(tgtCreateTableQuery)
        for key in countries:
            tgtInsertQuery = "INSERT into countries(name, latitude, longitude) VALUES(?,?,?)"
            cur.execute(tgtInsertQuery,(key,countries[key].split(",")[0],countries[key].split(",")[1]))
        con.commit()
        con.close()

def update_hourly():
	con = lite.connect('/Users/kuttush/Desktop/Spongebob/Thinkful/DataScience/DS_Project/latlong.db')
	cur = con.cursor()
	for key in countries:
		for i in range(0,5):
			curDate = datetime.datetime.now()-datetime.timedelta(days=i)
			curTime = curDate.strftime("%Y-%m-%d-%H:%M:%S")
			curURL = tgtURL+countries[key]+","+curTime
			r = requests.get(curURL)
			curJSON = r.json()
			for curHourly in curJSON["hourly"]["data"]:
				curHourly["latitude"] = countries[key].split(",")[0]
				curHourly["longitude"] = countries[key].split(",")[1]
				print(getInsertFromDict(curHourly))
				cur.execute(getInsertFromDict(curHourly))
		break
	con.commit()
	con.close()

def getInsertFromDict(tgtJson):
	tgtKeyList = []
	tgtValueList = []
	for key in tgtJson:
		tgtKeyList.append(key)
		if isinstance(tgtJson[key],str):
			tgtValueList.append("'" + str(tgtJson[key]) + "'")
		else:
			tgtValueList.append(str(tgtJson[key]))
	tgtInsertQuery = "INSERT INTO hourly(" + ", ".join(tgtKeyList) + ")"
	tgtInsertQuery += " VALUES(" + ",".join(tgtValueList) + ")"
	return tgtInsertQuery

init_db()
init_country_table()
update_hourly()
tgtQuery = "select distinct latitude, longitude, max(temperature) as temperature, time from hourly group by latitude, longitude"
con = lite.connect('/Users/kuttush/Desktop/Spongebob/Thinkful/DataScience/DS_Project/latlong.db')
df = pd.read_sql(tgtQuery,con)
print("Maximum temperature in last 5 days" + str(df['temperature'].tolist()[0]))

hrlyQuery = "select * from hourly order by time"
df_hrly = pd.read_sql(hrlyQuery,con)
plt.figure()
plt.plot(df_hrly['time'],df_hrly['temperature'], color='green')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature variation in __ for last 5 days')
plt.savefig('/Users/kuttush/Desktop/Spongebob/Thinkful/DataScience/DS_Project/Temp5days.jpg')

















