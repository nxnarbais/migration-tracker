import os.path  
import json

DATA_FOLDER = "./data/"

def writeJSONToFile(filename, data):
  with open("{}{}".format(DATA_FOLDER, filename), 'w+') as outfile:
    json.dump(data, outfile)

def readJSONFromFile(filename):
  with open("{}{}".format(DATA_FOLDER, filename)) as json_file:
    return json.load(json_file)

def isFileAvailable(filename):
  if os.path.isfile("{}{}".format(DATA_FOLDER, filename)):
    return True
  else:
    return False

