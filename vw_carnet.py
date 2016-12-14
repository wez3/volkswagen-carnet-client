#!/usr/bin/python

import sys
import requests
import json

# Login information for the VW CarNet app
CARNET_USERNAME = ''
CARNET_PASSWORD = ''

# Fake the VW CarNet mobile app headers
HEADERS = { 'Accept': 'application/json',
			'X-App-Name': 'eRemote',
			'X-App-Version': '1.0.0',
			'User-Agent': 'okhttp/2.3.0' }

def carNetLogon():
	print "Logging in"
	r = requests.post('https://msg.volkswagen.de/fs-car/core/auth/v1/VW/DE/token', data = {'grant_type':'password',
												'username':CARNET_USERNAME,
												'password':CARNET_PASSWORD}, headers=HEADERS)
	responseData = json.loads(r.content)
	token = responseData.get("access_token")
	HEADERS["Authorization"] = "AudiAuth 1 " + token
	return token

def retrieveVehicles():
	print "Retrieving verhicle"
	r = requests.get('https://msg.volkswagen.de/fs-car/usermanagement/users/v1/VW/DE/vehicles', headers=HEADERS)
	responseData = json.loads(r.content)
	VIN = responseData.get("userVehicles").get("vehicle")[0]
	return VIN

def retrieveCarNetInfo(VIN):
	# Retrieve GPS
	print "Retrieving CarNetInfo"
        r = requests.post('https://msg.volkswagen.de/fs-car/bs/vsr/v1/VW/DE/vehicles/' + VIN + '/requests', headers=HEADERS)
	r = requests.get('https://msg.volkswagen.de/fs-car/bs/cf/v1/VW/DE/vehicles/' + VIN + '/position', headers=HEADERS)
	responseData = json.loads(r.content)
	carPosition = responseData.get("findCarResponse").get("Position").get("carCoordinate")
	latReversed = carPosition.get("latitude")[::-1]
	lonReversed = carPosition.get("longitude")[::-1]
	lat = latReversed[:6] + "." + latReversed[6:]
	lon = lonReversed[:6] + "." + lonReversed[6:]
	floc = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(lat[::-1]) + ',' + str(lon[::-1]))
	loc = json.loads(floc.content)["results"][0]["formatted_address"]

	# Retrieve car counter
	r = requests.get('https://msg.volkswagen.de/fs-car/bs/vsr/v1/VW/DE/vehicles/' + VIN + '/status', headers=HEADERS)
	responseData = json.loads(r.content)
	try:
		carCounter = responseData.get("StoredVehicleDataResponse").get("vehicleData").get("data")[0].get("field")[0].get("milCarCaptured")
	except:
		carCounter = 0

	# Retrieve car temperature
	r = requests.get('https://msg.volkswagen.de/fs-car/bs/climatisation/v1/VW/DE/vehicles/' + VIN + '/climater', headers=HEADERS)
	responseData = json.loads(r.content)
	carTemp = responseData.get("climater").get("status").get("temperatureStatusData").get("outdoorTemperature").get("content")
	carTempDot = str(carTemp)[:3] + "." + str(carTemp)[3:]
	celcius = float(carTempDot)-273

	# Retrieved information
	print str(loc)
	print str(carcounter)
	print str(celcius)
	
def startClimat(VIN):
	HEADERS["Content-Type"] = 'application/vnd.vwg.mbb.climateraction_v1_0_0+xml'
	r = requests.post('https://msg.volkswagen.de/fs-car/bs/climatisation/v1/VW/DE/vehicles/' + VIN + '/climater/actions',
															data='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><action xmlns:xsi="de.davidbs.android.modapp.model.jaxb.climate"><type>startClimatisation</type></action>',
															headers=HEADERS)
	print r.content
	return 0

def stopClimat(VIN):
	HEADERS["Content-Type"] = 'application/vnd.vwg.mbb.climateraction_v1_0_0+xml'
	r = requests.post('https://msg.volkswagen.de/fs-car/bs/climatisation/v1/VW/DE/vehicles/' + VIN + '/climater/actions',
															data='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><action xmlns:xsi="de.davidbs.android.modapp.model.jaxb.climate"><type>stopClimatisation</type></action>',
															headers=HEADERS)
	print r.content
	return 0

def startWindowMelt(VIN):
	HEADERS["Content-Type"] = 'application/vnd.vwg.mbb.climateraction_v1_0_0+xml'
	r = requests.post('https://msg.volkswagen.de/fs-car/bs/climatisation/v1/VW/DE/vehicles/' + VIN + '/climater/actions',
															data='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><action xmlns:xsi="de.davidbs.android.modapp.model.jaxb.climate"><type>startWindowHeating</type></action>',
															headers=HEADERS)
	print r.content
	return 0

def stopWindowMelt(VIN):
	HEADERS["Content-Type"] = 'application/vnd.vwg.mbb.climateraction_v1_0_0+xml'
	r = requests.post('https://msg.volkswagen.de/fs-car/bs/climatisation/v1/VW/DE/vehicles/' + VIN + '/climater/actions',
															data='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><action xmlns:xsi="de.davidbs.android.modapp.model.jaxb.climate"><type>stopWindowHeating</type></action>',
															headers=HEADERS)
	print r.content
	return 0

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Need at least one argument."
		sys.exit()
	else:
		token = carNetLogon()
		VIN = retrieveVehicles()
		if(sys.argv[1] == "retrieveCarNetInfo"):
			retrieveCarNetInfo(VIN)
		elif(sys.argv[1] == "startClimat"):
			startClimat(VIN)
		elif(sys.argv[1] == "stopClimat"):
			stopClimat(VIN)
		elif(sys.argv[1] == "startWindowMelt"):
			startWindowMelt(VIN)
		elif(sys.argv[1] == "stopWindowMelt"):
			stopWindowMelt(VIN)

