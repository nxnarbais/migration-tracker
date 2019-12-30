from datadog import initialize, api

from flask import Flask
from flask import request
from flask import render_template, redirect, jsonify, url_for

import os
import datetime
import json

from utils.ddUrlHandler import getUrlExtension

from blueprints.update import update_endpoints
from blueprints.metrics import metric_endpoints

from services.api.monitors import getMonitors, getMonitorAlerts
from services.api.dashboards import getDashboards, getDashboardDetails, enrichDashboardsWithDetails

app = Flask(__name__)

app.register_blueprint(metric_endpoints)
app.register_blueprint(update_endpoints)

startTime = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")

options = {
    'api_key': os.getenv("API_KEY"),
    'app_key': os.getenv("APP_KEY"),
    'api_host': 'https://api.datadoghq.{}/'.format(getUrlExtension())
}
initialize(**options)

@app.route('/')
def homepage():
  monitors = getMonitors()
  dashboards = getDashboards()

  return render_template('homepage.html',
    title="Homepage",
    monitorCount = len(monitors),
    dashboardCount = len(dashboards),
  )

if __name__ == "__main__":
  app.run(debug = True, host = '0.0.0.0')
  
