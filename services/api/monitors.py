import requests
import os
from datadog import api

from models.monitor import Monitor

from utils.fileHandler import isFileAvailable
from utils.fileHandler import writeJSONToFile
from utils.fileHandler import readJSONFromFile

from utils.ddUrlHandler import getUrlExtension

API_KEY = os.getenv("API_KEY")
APP_KEY = os.getenv("APP_KEY")
FILENAME = "monitors.json"
FILENAME_ALERTS = "monitorAlerts.csv"

def _getMonitorsJSON(update = False):
  if(update):
    monitorsJSON = api.Monitor.get_all()
    print("load (monitors)")
    print("loaded {} monitors".format(len(monitorsJSON)))
    writeJSONToFile(FILENAME, monitorsJSON)
    return {
      "data": monitorsJSON
    }
  else:
    if(isFileAvailable(FILENAME)):
      return readJSONFromFile(FILENAME)
    else:
      return _getMonitorsJSON(True)

def getMonitors(update = False):
  monitorsJSON = _getMonitorsJSON(update).get("data", [])
  monitors = []
  for m in monitorsJSON:
    monitors.append(Monitor(m))
  return monitors

def getMonitorsMetadata(update = False):
  monitorsJSON = _getMonitorsJSON(update)
  monitors = []
  for m in monitorsJSON.get('data'):
    monitors.append(Monitor(m))
  monitorsJSON["data"] = monitors
  return monitorsJSON

def _getMonitorDetailsJSON(monitorId):
  return api.Monitor.get(monitorId, group_states='all')
