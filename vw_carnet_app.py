#!/usr/bin/python
# coding: utf8

import sys
import requests
import json

# Login information for the VW CarNet app
CARNET_USERNAME = 'usr'
CARNET_PASSWORD = 'pwd'

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
	print "token: " + token
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
    	
	r = requests.get('https://msg.volkswagen.de/fs-car/bs/cf/v1/VW/DE/vehicles/' + VIN + '/position', headers=HEADERS)
	#print "Position request: " + r.content
	responseData = json.loads(r.content)
	carPosition = responseData.get("findCarResponse").get("Position").get("carCoordinate")
	latReversed = str(carPosition.get("latitude"))[::-1]
	lonReversed = str(carPosition.get("longitude"))[::-1]
	lat = latReversed[:6] + "." + latReversed[6:]
	lon = lonReversed[:6] + "." + lonReversed[6:]
	timeStampCarSend = responseData.get("findCarResponse").get("Position").get("timestampCarSent")
	
	# Retrieve car counter
	r = requests.get('https://msg.volkswagen.de/fs-car/bs/vsr/v1/VW/DE/vehicles/' + VIN + '/status', headers=HEADERS)
	#print "Vehicle request: " + r.content
	responseData = json.loads(r.content)
	try: mileage = responseData.get("StoredVehicleDataResponse").get("vehicleData").get("data")[1].get("field")[0].get("value")
	except: mileage = 0

	try: serviceInKm = responseData.get("StoredVehicleDataResponse").get("vehicleData").get("data")[2].get("field")[2].get("value") 
	except: serviceInKm = 0
	serviceInKm = (serviceInKm * -1)

	try: serviceInDays = responseData.get("StoredVehicleDataResponse").get("vehicleData").get("data")[2].get("field")[3].get("value") 
	except: serviceInDays = 0
	serviceInDays = (serviceInDays * -1)

	try: parkingLight = responseData.get("StoredVehicleDataResponse").get("vehicleData").get("data")[3].get("field")[0].get("value") 
	except: parkingLight = 0
	if (parkingLight == 3):
		parkingLight = "left=on, right=off"
	elif (parkingLight == 4):
		parkingLight = "left=off, right=on"
	elif (parkingLight == 5):
		parkingLight = "left=on, right=on"
	else:
		parkingLight = "left=off, right=off"

	# Retrieve car temperature
	r = requests.get('https://msg.volkswagen.de/fs-car/bs/climatisation/v1/VW/DE/vehicles/' + VIN + '/climater', headers=HEADERS)
	#print "Climate request: " + r.content
	responseData = json.loads(r.content)
	carTemp = responseData.get("climater").get("status").get("temperatureStatusData").get("outdoorTemperature").get("content")
	carTempDot = str(carTemp)[:3] + "." + str(carTemp)[3:]
	celcius = float(carTempDot)-273
	climateHeatingStatus = responseData.get("climater").get("status").get("climatisationStatusData").get("climatisationState").get("content")
	climateHeatingWindowFrontStatus = responseData.get("climater").get("status").get("windowHeatingStatusData").get("windowHeatingStateFront").get("content")
	climateHeatingWindowRearStatus = responseData.get("climater").get("status").get("windowHeatingStatusData").get("windowHeatingStateRear").get("content")

	r = requests.get('https://msg.volkswagen.de/fs-car/bs/batterycharge/v1/VW/DE/vehicles/' + VIN + '/charger', headers=HEADERS)
	#print "Charger request: " + r.content
	responseData = json.loads(r.content)
	chargingMode = responseData.get("charger").get("status").get("chargingStatusData").get("chargingMode").get("content")
	chargingReason = responseData.get("charger").get("status").get("chargingStatusData").get("chargingReason").get("content")
	externalPowerSupplyState = responseData.get("charger").get("status").get("chargingStatusData").get("externalPowerSupplyState").get("content")
	energyFlow = responseData.get("charger").get("status").get("chargingStatusData").get("energyFlow").get("content")
	chargingState = responseData.get("charger").get("status").get("chargingStatusData").get("chargingState").get("content")

	stateOfCharge = responseData.get("charger").get("status").get("batteryStatusData").get("stateOfCharge").get("content")
	remainingChargingTime = responseData.get("charger").get("status").get("batteryStatusData").get("remainingChargingTime").get("content")
	remainingChargingTimeTargetSOC = responseData.get("charger").get("status").get("batteryStatusData").get("remainingChargingTimeTargetSOC").get("content")

	primaryEngineRange = responseData.get("charger").get("status").get("cruisingRangeStatusData").get("primaryEngineRange").get("content")
	

	# Retrieved information
	print "Timestamp: " + timeStampCarSend
	print "Location: lat " + str(lat[::-1]) + ", lon " + str(lon[::-1])
	print "Mileage: " + str(mileage) + "km"
	print "serviceInKm: " + str(serviceInKm) + "km"
	print "serviceInDays: " + str(serviceInDays) + "days"
	print "parkingLight: " + parkingLight
	print "Temperature: " + str(celcius) + "°C"
	print "Heating: " + climateHeatingStatus
	print "Front window heating: " + climateHeatingWindowFrontStatus
	print "Rear window heating: " + climateHeatingWindowRearStatus
	print "chargingMode: " + chargingMode
	print "chargingReason: " + chargingReason
	print "externalPowerSupplyState: " + externalPowerSupplyState
	print "energyFlow: " + energyFlow
	print "chargingState: " + chargingState

	print "stateOfCharge: " + str(stateOfCharge) + "%"
	print "remainingChargingTime: " + str(remainingChargingTime)
	print "remainingChargingTimeTargetSOC: " + remainingChargingTimeTargetSOC
	print "primaryEngineRange: " + str(primaryEngineRange) + "km"


def requestCarSendData(VIN):
	print "Requesting car to send it's data to the server"
    
	#this seems to be the request for the car to send it's data to the server
	r = requests.post('https://msg.volkswagen.de/fs-car/bs/vsr/v1/VW/DE/vehicles/' + VIN + '/requests', headers=HEADERS)
	#print "Vehicle requests: " + r.content	
	responseData = json.loads(r.content)
	requestId = responseData.get("CurrentVehicleDataResponse").get("requestId")
	#Don't know what this ID is good for. Maybe this is for more critical commands like open door...
	print "requestId: " + requestId

	
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
			print "VIN: " + VIN
		elif(sys.argv[1] == "requestCarSendData"):
			requestCarSendData(VIN)
		elif(sys.argv[1] == "startClimat"):
			startClimat(VIN)
		elif(sys.argv[1] == "stopClimat"):
			stopClimat(VIN)
		elif(sys.argv[1] == "startWindowMelt"):
			startWindowMelt(VIN)
		elif(sys.argv[1] == "stopWindowMelt"):
			stopWindowMelt(VIN)
