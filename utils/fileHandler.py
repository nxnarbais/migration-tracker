import os.path  
import json
from datetime import datetime

DATA_FOLDER = "./data/"

def writeJSONToFile(filename, data):
  with open("{}{}".format(DATA_FOLDER, filename), 'w+') as outfile:
    json.dump({
      "updatedAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
      "data": data,
    }, outfile)

def readJSONFromFile(filename):
  with open("{}{}".format(DATA_FOLDER, filename)) as json_file:
    return json.load(json_file)

def isFileAvailable(filename):
  if os.path.isfile("{}{}".format(DATA_FOLDER, filename)):
    return True
  else:
    return False

