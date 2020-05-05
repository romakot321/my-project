import requests
import datetime

eventId = -1
bonusEventId = -1
idShard = -1 # 0 - Water shard, 1 - Sun shard, 2 - Air shard
s_city = "Irkutsk,RU"
city_id = 0
appid = "c65eacc5c2d1c3a134f1a8ba0c9906c8"
weathernow = ""
windnow = 0
date = datetime.datetime.now()
list1 = [0,0]
eventList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
eventList = ["upHP", "upDef", "upAtk"
			 "upDrop", "upRateSpawn", "upLvlMonsters",
			 "downHp", "downDef", "downAtk",
			 "downDrop", "downRateSpawn", "downLvlMonsters",
			 "maxMobInChunk+", "maxMobInChunk-"]

def getWeather():
	global weathernow, windnow
	try:
	    res = requests.get("http://api.openweathermap.org/data/2.5/find",
	                 params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
	    data = res.json()
	    cities = ["{} ({})".format(d['name'], d['sys']['country'])
	              for d in data['list']]
	    city_id = data['list'][0]['id']
	except Exception as e:
	    print("Exception (find):", e)
	    pass

	try:
	    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
	                 params={'id': city_id, 'units': 'metric', 'lang': 'en', 'APPID': appid})
	    data = res.json()
	    weathernow = data['weather'][0]['main']
	    windnow = data['wind']['speed']
	except Exception as e:
	    print("Exception (weather):", e)
	    pass

def setEvent():
	getWeather()
	global eventList, eventId, bonusEventId, idShard
	if(weathernow == "Rain"):
		if(date.month == 1):
			eventId = 0
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 2):
			eventId = 1
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 3):
			eventId = 2
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 4):
			eventId = 3
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 5):
			eventId = 4
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 6):
			eventId = 5
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 7):
			eventId = 6
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 8):
			eventId = 7
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 9):
			eventId = 8
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 10):
			eventId = 9
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 11):
			eventId = 10
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 12):
			eventId = 11
			if(windnow > 0 and windnow <= 5):
				buff = 2
		idShard = 0
	elif(weathernow == "Clear"):
		if(date.month == 1):
			eventId = 0
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 2):
			eventId = 1
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 3):
			eventId = 2
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 4):
			eventId = 3
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 5):
			eventId = 4
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 6):
			eventId = 5
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 7):
			eventId = 6
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 8):
			eventId = 7
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 9):
			eventId = 8
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 10):
			eventId = 9
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 11):
			eventId = 10
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 12):
			eventId = 11
			if(windnow > 0 and windnow <= 5):
				buff = 2
		idShard = 1
	elif(weathernow == "Clouds"):
		if(date.month == 1):
			eventId = 0
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 2):
			eventId = 1
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 3):
			eventId = 2
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 4):
			eventId = 3
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 5):
			eventId = 4
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 6):
			eventId = 5
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 7):
			eventId = 6
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 8):
			eventId = 7
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 9):
			eventId = 8
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 10):
			eventId = 9
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 11):
			eventId = 10
			if(windnow > 0 and windnow <= 5):
				buff = 2
		elif(date.month == 12):
			eventId = 11
			if(windnow > 0 and windnow <= 5):
				buff = 2
		idShard = 2
	if(date.hour >= 0 and date.hour <= 5):
		bonusEventId = 12
	elif(date.hour > 5 and date.hour < 0):
		bonusEventId = 13
	eventList = [eventId, bonusEventId, idShard]
	return eventList