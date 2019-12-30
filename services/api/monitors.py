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
    return monitorsJSON
  else:
    if(isFileAvailable(FILENAME)):
      return readJSONFromFile(FILENAME)
    else:
      return _getMonitorsJSON(True)

def getMonitors(update = False):
  monitorsJSON = _getMonitorsJSON(update)
  monitors = []
  for m in monitorsJSON:
    monitors.append(Monitor(m))
  return monitors

def _getMonitorDetailsJSON(monitorId):
  return api.Monitor.get(monitorId, group_states='all')

## Doc: https://docs.datadoghq.com/monitors/faq/how-can-i-export-alert-history/
def getMonitorAlerts(update = False):
  if(update):
    baseUrl = "https://app.datadoghq.{}/".format(getUrlExtension())
    endpoint = "report/hourly_data/monitor"
    # print('{}{}?api_key={}&application_key={}'.format(baseUrl, endpoint, API_KEY, APP_KEY))
    r = requests.get('{}{}?api_key={}&application_key={}'.format(baseUrl, endpoint, API_KEY, APP_KEY))
    c = r.content.decode()
    writeJSONToFile(FILENAME_ALERTS, c)
    output = []
    lines = c.split("\n")
    for l in lines:
      output.append(l.split(","))
    return output
  else:
    if(isFileAvailable(FILENAME_ALERTS)):
      c = readJSONFromFile(FILENAME_ALERTS)
      output = []
      lines = c.split("\n")
      for l in lines:
        output.append(l.split(","))
      return output
    else:
      return getMonitorAlerts(True)
