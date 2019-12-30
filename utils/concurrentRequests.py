import concurrent.futures

from utils.fileHandler import isFileAvailable
from utils.fileHandler import writeJSONToFile
from utils.fileHandler import readJSONFromFile

CONNECTIONS = 10
TIMEOUT = 5

def execFctInParallel(arr, fct):
  ## Init
  i = 0
  total = len(arr)

  ## Exec concurrently
  with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    future_to_url = (executor.submit(fct, el, TIMEOUT) for el in arr)

    ## Get results
    output = []
    for future in concurrent.futures.as_completed(future_to_url):
      try:
        data = future.result()
        output.append(data)
        # print("load completed for {}".format(data.get('id')))
        i = i + 1
        print("progress {}/{}".format(i, total))
      except Exception as exc:
        print("ERROR")
        data = str(type(exc))
      finally:
        # output.append(data)
        print(str(len(output)),end="\r")
    return output

def storeParallelOuputToFile(output, filename):
    store = {}
    if(isFileAvailable(filename)):
        store = readJSONFromFile(filename).get("data")
    for o in output:
        oId = o.get('id')
        store[oId] = o.get('output')
    writeJSONToFile(filename, store)
    return store

def massObjectUpdate(arr, filename, fct, update = False):
  ## Initialize
  store = {}
  if(isFileAvailable(filename)):
    store = readJSONFromFile(filename).get("data")

  ## Identify ids that have to be updated
  idsToUpdate = []
  if(update):
    for o in arr:
      oId = str(o.getId())
      idsToUpdate.append(oId)
  else:
    keysInFile = []
    for key, val in store.items():
      keysInFile.append(key)
    # print("Keys: {}".format(keysInFile))
    for o in arr:
      oId = str(o.getId())
      if(not (oId in keysInFile)):
        idsToUpdate.append(oId)
  # print("IDs to update: {}".format(idsToUpdate))

  ## Fetch additional information and store them in file
  output = execFctInParallel(idsToUpdate, fct)
  store = storeParallelOuputToFile(output, filename)

  ## Enrich object with information just fetched
  for o in arr:
    oId = str(o.getId())
    o.setDetailsJSON(store[oId])

  return arr