# Python Volkswagen CarNet Client

**This script is deprecated**

A newer version can be found at https://github.com/bgewehr/volkswagen-carnet-client

This is a Python client for Volkswagen CarNet, it simulates the behaviour of the CarNet app. It allows users to retrieve information about the vehicle (location, temperature and mileage), next to this the Window melt and Climat functionalities can be started from the Python script.

# Installation

Clone the Github page and modify the following values in the vw_carnet.py script:
```
CARNET_USERNAME = ''
CARNET_PASSWORD = ''
```

# Usage

Run the script with a argument. The following are supported:
```
python vw_carnet.py retrieveCarNetInfo
```

```
python vw_carnet.py requestCarSendData
```

```
python vw_carnet.py startClimat
```

```
python vw_carnet.py stopClimat
```

```
python vw_carnet.py startWindowMelt
```

```
python vw_carnet.py stopWindowMelt
```
