from utils.ddUrlHandler import getBaseURL
from utils.ddUrlHandler import getBaseSupportURL

class Dashboard:
  def __init__(self, dashboardJSON):
    self.dashboardJSON = dashboardJSON

  def getJSON(self):
    return self.dashboardJSON
  
  def getFullJSON(self):
    dashboardJSON = self.dashboardJSON
    dashboardJSON['details'] = self.dashboardDetailsJSON
    return dashboardJSON
  
  def getId(self):
    return self.dashboardJSON.get('id')

  def getUrl(self):
    oId = self.getId()
    urls = {
      "url": "{}/dashboard/{}".format(getBaseURL(), oId),
      "supportUrl": "{}?next_url=%2Fdashboard%2F{}".format(getBaseSupportURL(), oId)
    }
    return urls

  def getName(self):
    return self.dashboardJSON.get('title')

  def getType(self):
    return self.dashboardJSON.get('layout_type')
  
  def getCreatedDate(self):
    return self.dashboardJSON.get('created_at')
  
  def getModifiedDate(self):
    return self.dashboardJSON.get('modified_at')
  
  def setDetailsJSON(self, dashboardDetailsJSON):
    self.dashboardDetailsJSON = dashboardDetailsJSON
    
  def getDetailsJSON(self):
    return self.dashboardDetailsJSON
  
  def getWidgets(self):
    return self.dashboardDetailsJSON.get('widgets', [])

  # No tags for a dashboard
  def getTags(self):
    return []
  
  def getMainDescription(self):
    return {
      "type": "dashboard",
      "name": self.getName(),
      # "tags": self.getTags(),
      "xtype": self.getType(),
      "last_modified": self.getModifiedDate(),
      "url": self.getUrl()
    }
  
  def getStdDescription(self):
    return {
      "type": "dashboard",
      "name": self.getName(),
      "tags": self.getTags(),
      "url": self.getUrl()
    }
