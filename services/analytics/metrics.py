import re

from utils.stringHandler import isMatchingRegex
from services.api.dashboards import getDashboardDetails, enrichDashboardsWithDetails_v2

def getMonitorsWithQueryMatchingPattern(monitors, regexStr):
  res = []
  regex = re.compile(regexStr)
  for m in monitors:
    query = m.getQuery()
    if(isMatchingRegex(query, regex)):
      res.append(m.getMainDescription())
  return res

def getDashboardsWithQueryMatchingPattern(dashboards, regexStr):
  dashboards = enrichDashboardsWithDetails_v2(dashboards)
  res = []
  regex = re.compile(regexStr)
  total = len(dashboards)
  count = 0
  for d in dashboards:
    count = count + 1
    print("search progress: {}/{}".format(count, total))
    i = 0
    widgets = d.getWidgets()
    for w in widgets:
      if(i == 0):
        requests = w.get('definition', {}).get('requests', [])
        for r in requests:
          if(i == 0):
            if type(r) is dict:
              query = r.get('q')
              if(isMatchingRegex(query, regex)):
                res.append(d.getMainDescription())
                i = i + 1
        # section required to take into account groups
        wWidgets = w.get('definition', {}).get('widgets', [])
        for ww in wWidgets:
          requests = ww.get('definition', {}).get('requests', [])
          for r in requests:
            if(i == 0):
              if type(r) is dict:
                query = r.get('q')
                if(isMatchingRegex(query, regex)):
                  res.append(d.getMainDescription())
                  i = i + 1
  return res

def getMetricQueryMatchingPatternInMonitors(monitors, regexStr):
  res = {}
  regex = re.compile(regexStr)
  for m in monitors:
    query = m.getQuery()
    if(isMatchingRegex(query, regex)):
      res[query] = res.get(query, 0) + 1
  return res

def getMetricQueryMatchingPatternInDashboards(dashboards, regexStr):
  dashboards = enrichDashboardsWithDetails_v2(dashboards)
  res = {}
  regex = re.compile(regexStr)
  total = len(dashboards)
  count = 0
  for d in dashboards:
    count = count + 1
    print("search progress: {}/{}".format(count, total))
    widgets = d.getWidgets()
    for w in widgets:
      requests = w.get('definition', {}).get('requests', [])
      for r in requests:
        if type(r) is dict:
          query = r.get('q')
          if(isMatchingRegex(query, regex)):
            res[query] = res.get(query, 0) + 1
      # section required to take into account groups
      wWidgets = w.get('definition', {}).get('widgets', [])
      for ww in wWidgets:
        requests = ww.get('definition', {}).get('requests', [])
        for r in requests:
          if type(r) is dict:
            query = r.get('q')
            if(isMatchingRegex(query, regex)):
              res[query] = res.get(query, 0) + 1
  return res

def splitQuery(query):
  # Number of arithmetic function used +,-,/,*
  arithmeticPattern = '( [+/\-*] )'
  arithmeticPatternRegex = re.compile(arithmeticPattern)
  arithmeticCount = len(re.findall(arithmeticPatternRegex, query))

  # Metrics
  metricPattern = ':([0-9a-zA-Z._]+){'
  metricPatternRegex = re.compile(metricPattern)
  metrics = re.findall(metricPatternRegex, query)

  # Tags for each metric
  tagsPattern = '(?<!by ){([0-9a-zA-Z._:/,\-]+)}'
  tagsPatternRegex = re.compile(tagsPattern)
  tags = re.findall(tagsPatternRegex, query)

  # By tags
  byTagsPattern = ' by {([0-9a-zA-Z._:,\-]+)}'
  byTagsPatternRegex = re.compile(byTagsPattern)
  byTags = re.findall(byTagsPatternRegex, query)

  return {
    "query": query,
    "metrics": metrics,
    "arithmeticCount": arithmeticCount,
    "tags": tags,
    "byTags": byTags
  }

# def countQueriesByOrigin(queryResults):
#   origins = {}
#   for dmp in queryResults:
#     query = dmp.get('query', '')
#     origin = query.split(':')[1].split('.')[0]
#     origins[origin] = origins.get(origin, 0) + 1
#   return origins

# def transformHistogramQueriesToDistribution(queryResults):
#   queryAnalytics = []
#   for dmp in queryResults:
#     query = dmp.get('query', '')

#     # Get query
#     regex = re.compile(".*sum\:(.*)\.(sum|count)\{.*")
#     m = re.search(regex, query)
#     if m:
#         metric = m.group(1)

#     # Get query type
#     queryType = ""
#     regex = re.compile(".*\.sum.*")
#     if(regex.match(query)):
#       queryType = "sum"
#     regex = re.compile(".*\.count.*")
#     if(regex.match(query)):
#       queryType = "count"
    
#     # Check if has upper_bound
#     hasUpperBound = False
#     regex = re.compile(".*upper_bound.*")
#     if(regex.match(query)):
#       hasUpperBound = True
    
#     newQuery = ""
#     if(not hasUpperBound):
#       newQuery = query
#       newQuery = newQuery.replace(".count", "").replace(".sum", "")
#       if(queryType == "count"):
#         newQuery = newQuery.replace("sum:", "count:")
#       # Remove rate
#       regex = re.compile("per_hour\((.*)\)")
#       m = re.search(regex, query)
#       if m:
#           newQuery = m.group(1)
#       regex = re.compile("per_minute\((.*)\)")
#       m = re.search(regex, query)
#       if m:
#           newQuery = m.group(1)
#       regex = re.compile("per_second\((.*)\)")
#       m = re.search(regex, query)
#       if m:
#           newQuery = m.group(1)
    
#     # Results
#     queryAnalytics.append({
#         "query": query,
#         "newQuery": newQuery,
#         "metric": metric,
#         "type": queryType,
#         "hasUpperBound": hasUpperBound
#     })
#   return queryAnalytics
  