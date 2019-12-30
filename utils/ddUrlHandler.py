import os

ORG_ID = os.getenv("ORG_ID")
REGION = os.getenv("REGION")
SUBDOMAIN = os.getenv("SUBDOMAIN")

def getUrlExtension():
  if (REGION == "us"):
    return "com"
  else:
    return REGION

def getBaseURL():
  return "https://{}.datadoghq.{}".format(SUBDOMAIN, getUrlExtension())

def getBaseSupportURL():
  return "https://{}/{}".format(REGION, ORG_ID)
