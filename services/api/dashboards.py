import requests
import os
from datadog import api

from models.dashboard import Dashboard

from utils.fileHandler import isFileAvailable
from utils.fileHandler import writeJSONToFile
from utils.fileHandler import readJSONFromFile

from utils.ddUrlHandler import getUrlExtension

from utils.concurrentRequests import massObjectUpdate

API_KEY = os.getenv("API_KEY")
APP_KEY = os.getenv("APP_KEY")
FILENAME = "dashboards.json"
FILENAME_DETAILS = "dashboardDetails.json"

def _getDashboardsJSON(update = False):
  if(update):
    dashboardsJSON = api.Dashboard.get_all()
    print("load (dashboards)")
    writeJSONToFile(FILENAME, dashboardsJSON)
    return dashboardsJSON
  else:
    if(isFileAvailable(FILENAME)):
      return readJSONFromFile(FILENAME)
    else:
      return _getDashboardsJSON(True)

def getDashboardDetails(dashboardId, update = False):
  # print("_getDashboardDetails: {}".format(dashboardId))
  if(update):
    dashboardDetailsJSON = api.Dashboard.get(dashboardId)
    dashboardDetailsJSONStored = readJSONFromFile(FILENAME_DETAILS)
    dashboardDetailsJSONStored[dashboardId] = dashboardDetailsJSON
    writeJSONToFile(FILENAME_DETAILS, dashboardDetailsJSONStored)
    return dashboardDetailsJSON
  else:
    if(isFileAvailable(FILENAME_DETAILS)):
      dashboardDetailsJSONStored = readJSONFromFile(FILENAME_DETAILS)
      if(dashboardId in dashboardDetailsJSONStored):
        return dashboardDetailsJSONStored[dashboardId]
      else:
        return getDashboardDetails(dashboardId, True)
    else:
      writeJSONToFile(FILENAME_DETAILS, {})
      return getDashboardDetails(dashboardId, True)

def enrichDashboardsWithDetails(arr, update = False):
  keys = []
  if(isFileAvailable(FILENAME_DETAILS)):
    detailsJSONStored = readJSONFromFile(FILENAME_DETAILS)
    for key, val in detailsJSONStored.items():
      keys.append(key)
  # print("Keys: {}".format(keys))

  total = len(arr)
  i = 0
  for o in arr:
    i = i + 1
    print("load progress (dashboards) {}/{}".format(i, total))
    oId = str(o.getId())
    # print("Check for id: {} in keys: {}".format(oId, keys))
    if((oId in keys) and not update):
      # print("in file")
      o.setDetailsJSON(detailsJSONStored[oId])
    else:
      # print("api call")
      o.setDetailsJSON(getDashboardDetails(oId, update))
  return arr

def getDashboards(update = False):
  dashboardJSON = _getDashboardsJSON(update).get('dashboards', [])
  dashboards = []
  for d in dashboardJSON:
    dashboards.append(Dashboard(d))
  return dashboards


TIMEOUT = 20
def _getDetails(id, timeout = TIMEOUT):
  return {
    "id": id,
    "output": api.Dashboard.get(id)
  }

def enrichDashboardsWithDetails_v2(arr, update = False):
  arr = massObjectUpdate(arr, FILENAME_DETAILS, _getDetails, update)
  return arr