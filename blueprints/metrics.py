from flask import Blueprint, render_template, jsonify

from services.api.monitors import getMonitors
from services.api.dashboards import getDashboards

from services.analytics.metrics import getDashboardsWithQueryMatchingPattern, getMonitorsWithQueryMatchingPattern, getMetricQueryMatchingPatternInMonitors, getMetricQueryMatchingPatternInDashboards, splitQuery

from utils.fileHandler import writeJSONToFile

metric_endpoints = Blueprint('metric_endpoints', __name__)

TITLE = "Metric Analytics"
MAIN_TEMPLATE = "generic/table.html"

# PATTERN = ".*sum\:(?!aws)(?!jvm).*\.(sum|count)\{.*" # histogram pattern
# PATTERN = ".*sum\:(?!aws)(?!jvm).*\.(sum|count)\{.*upper_bound.*" # histogram pattern

@metric_endpoints.route('/metrics/analytics/search_in_monitors/migration/upper_bound')
def metrics_search_in_monitors_migration_upper_bound():
  monitors = getMonitors()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*upper_bound.*"
  print(pattern)
  res = getMonitorsWithQueryMatchingPattern(monitors, pattern)
  msg = {
    "title": "Search for pattern in monitors",
    "message": "Pattern `{}`".format(pattern)
  }
  return render_template(MAIN_TEMPLATE, title=TITLE, list=res, message=msg, total=len(monitors))

@metric_endpoints.route('/metrics/analytics/search_in_monitors/migration')
def metrics_search_in_monitors_migration():
  monitors = getMonitors()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*"
  print(pattern)
  res = getMonitorsWithQueryMatchingPattern(monitors, pattern)
  msg = {
    "title": "Search for pattern in monitors",
    "message": "Pattern `{}`".format(pattern)
  }
  return render_template(MAIN_TEMPLATE, title=TITLE, list=res, message=msg, total=len(monitors))

@metric_endpoints.route('/metrics/analytics/search_in_monitors_and_count/migration/upper_bound')
def metrics_search_in_monitors_and_count_migration_upper_bound():
  monitors = getMonitors()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*upper_bound.*"
  res = getMetricQueryMatchingPatternInMonitors(monitors, pattern)
  msg = {
    "title": "Search for pattern in monitors",
    "message": "Pattern {}".format(pattern)
  }
  arr = []
  for key, value in res.items():
    queryDetails = splitQuery(key)
    queryDetails["count"] = value
    arr.append(queryDetails)
  metricCount = {}
  metricCountByTag = {}
  for el in arr:
    metrics = el.get('metrics', [])
    for m in metrics:
      metricCount[m] = metricCount.get(m, 0) + 1
  newArr = []
  for key, value in metricCount.items():
    newArr.append({
      "metric": key,
      "count": value
    })
  # return render_template(MAIN_TEMPLATE, title=TITLE, list=arr, message=msg)
  return render_template(MAIN_TEMPLATE, title=TITLE, list=newArr, message=msg)

@metric_endpoints.route('/metrics/analytics/search_in_monitors_and_count/migration')
def metrics_search_in_monitors_and_count_migration():
  monitors = getMonitors()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*"
  res = getMetricQueryMatchingPatternInMonitors(monitors, pattern)
  msg = {
    "title": "Search for pattern in monitors",
    "message": "Pattern {}".format(pattern)
  }
  arr = []
  for key, value in res.items():
    queryDetails = splitQuery(key)
    queryDetails["count"] = value
    arr.append(queryDetails)
  metricCount = {}
  for el in arr:
    metrics = el.get('metrics', [])
    for m in metrics:
      metricCount[m] = metricCount.get(m, 0) + 1
  newArr = []
  for key, value in metricCount.items():
    newArr.append({
      "metric": key,
      "count": value
    })

  # return render_template(MAIN_TEMPLATE, title=TITLE, list=arr, message=msg)
  return render_template(MAIN_TEMPLATE, title=TITLE, list=newArr, message=msg)



@metric_endpoints.route('/metrics/analytics/search_in_dashboards/migration/upper_bound')
def metrics_search_in_dashboards_migration_upper_bound():
  dashboards = getDashboards()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*upper_bound.*"
  res = getDashboardsWithQueryMatchingPattern(dashboards, pattern)
  msg = {
    "title": "Search for pattern in dashboards",
    "message": "Pattern {}".format(pattern)
  }
  return render_template(MAIN_TEMPLATE, title=TITLE, list=res, message=msg, total=len(dashboards))

@metric_endpoints.route('/metrics/analytics/search_in_dashboards/migration')
def metrics_search_in_dashboards_migration():
  dashboards = getDashboards()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*"
  res = getDashboardsWithQueryMatchingPattern(dashboards, pattern)
  msg = {
    "title": "Search for pattern in dashboards",
    "message": "Pattern {}".format(pattern)
  }
  return render_template(MAIN_TEMPLATE, title=TITLE, list=res, message=msg, total=len(dashboards))

@metric_endpoints.route('/metrics/analytics/search_in_dashboards_and_count/migration/upper_bound')
def metrics_search_in_dashboards_and_count_migration_upper_bound():
  dashboards = getDashboards()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*upper_bound.*"
  res = getMetricQueryMatchingPatternInDashboards(dashboards, pattern)
  msg = {
    "title": "Search for pattern in dashboards",
    "message": "Pattern {}".format(pattern)
  }
  arr = []
  for key, value in res.items():
    queryDetails = splitQuery(key)
    queryDetails["count"] = value
    arr.append(queryDetails)
  writeJSONToFile("dashboard-search.json",arr)
  metricCount = {}
  for el in arr:
    metrics = el.get('metrics', [])
    for m in metrics:
      metricCount[m] = metricCount.get(m, 0) + 1
  newArr = []
  for key, value in metricCount.items():
    newArr.append({
      "metric": key,
      "count": value
    })
  return render_template(MAIN_TEMPLATE, title=TITLE, list=newArr, message=msg)

@metric_endpoints.route('/metrics/analytics/search_in_dashboards_and_count/migration')
def metrics_search_in_dashboards_and_count_migration():
  dashboards = getDashboards()
  pattern = ".*sum\:(starbug|c2c).*\.(sum|count)\{.*"
  res = getMetricQueryMatchingPatternInDashboards(dashboards, pattern)
  msg = {
    "title": "Search for pattern in dashboards",
    "message": "Pattern {}".format(pattern)
  }
  arr = []
  for key, value in res.items():
    queryDetails = splitQuery(key)
    queryDetails["count"] = value
    arr.append(queryDetails)
  writeJSONToFile("dashboard-search.json",arr)
  metricCount = {}
  for el in arr:
    metrics = el.get('metrics', [])
    for m in metrics:
      metricCount[m] = metricCount.get(m, 0) + 1
  newArr = []
  for key, value in metricCount.items():
    newArr.append({
      "metric": key,
      "count": value
    })
  return render_template(MAIN_TEMPLATE, title=TITLE, list=newArr, message=msg)

