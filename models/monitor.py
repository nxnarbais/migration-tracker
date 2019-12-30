from utils.ddUrlHandler import getBaseURL
from utils.ddUrlHandler import getBaseSupportURL

class Monitor:
  def __init__(self, monitorJSON):
    self.monitorJSON = monitorJSON

  def getJSON(self):
    return self.monitorJSON

  def getUrl(self):
    oId = self.monitorJSON.get('id')
    urls = {
      "url": "{}/monitors/{}".format(getBaseURL(), oId),
      "supportUrl": "{}?next_url=%2Fmonitors%2F{}".format(getBaseSupportURL(), oId)
    }
    return urls

  def getName(self):
    return self.monitorJSON.get('name')

  def getType(self):
    return self.monitorJSON.get('type')

  def getQuery(self):
    return self.monitorJSON.get('query')

  def getTags(self):
    return self.monitorJSON.get('tags', [])

  def getState(self):
    return self.monitorJSON.get('overall_state')  

  def getStateLastModified(self):
    return self.monitorJSON.get('overall_state_modified')
  
  def getOptions(self):
    return self.monitorJSON.get('options', {})

  def getEvaluationDelay(self):
    return self.getOptions().get('evaluation_delay', 0)

  def getAlertMessage(self):
    return self.monitorJSON.get('message', '')

  def getMainDescription(self):
    return {
      "type": "monitor",
      "name": self.getName(),
      "tags": self.getTags(),
      "xtype": self.getType(),
      "state_last_modified": self.getStateLastModified(),
      "query": self.getQuery(),
      "evaluation_delay": self.getEvaluationDelay(),
      "url": self.getUrl()
    }
  
  def getStdDescription(self):
    return {
      "type": "monitor",
      "name": self.getName(),
      "tags": self.getTags(),
      "url": self.getUrl()
    }