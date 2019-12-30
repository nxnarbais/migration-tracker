from flask import Blueprint, render_template, jsonify, redirect, url_for

from services.api.monitors import getMonitors, getMonitorAlerts
from services.api.dashboards import getDashboards, getDashboardDetails, enrichDashboardsWithDetails, enrichDashboardsWithDetails_v2

update_endpoints = Blueprint('update_endpoints', __name__)

MAX_PAGES_FOR_HOST = 99999
@update_endpoints.route('/assets/update')
def update_assets():
  UPDATE = True # Set to True to force update, otherwise the data will be picked up from the storage
  monitors = getMonitors(UPDATE)
  dashboards = getDashboards(UPDATE)
  dashboards = enrichDashboardsWithDetails_v2(dashboards, UPDATE)
  return redirect(url_for('homepage'))

@update_endpoints.route('/assets/update/monitors')
def update_monitors():
  monitors = getMonitors(True)
  return redirect(url_for('homepage'))

@update_endpoints.route('/assets/update/dashboards')
def update_dashboards():
  dashboards = getDashboards(True)
  dashboards = enrichDashboardsWithDetails_v2(dashboards, True)
  return redirect(url_for('homepage'))
