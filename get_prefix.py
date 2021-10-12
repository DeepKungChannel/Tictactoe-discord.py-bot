from replit import db #Replit database
import json

def update_prefix():
  result = db['prefixes'].value

  with open("prefixviewer.json","w") as f:
    json.dump(result,f,indent=4)