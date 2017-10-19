import json

#Changes to config path must be reflected in imports.py
localConfig = '/home/devmain/PersAIAsis/tools/localConfig.txt'

def getConfig():
    bod = {}
    with open(localConfig,'r') as f:
        bod = json.load(f)
    return bod

def writeConfig(bod):
    with open(localConfig, 'w') as f:
        f.write(json.dumps(bod, sort_keys=False, indent=2))

def checkConfig(self,**kwargs):
    if "path" in kwargs:
        print kwargs["path"]
    else:
        with open(localConfig,'r') as f:
            bod = json.load(f)
            print bod.keys()
            select = ""
            print "Would you like to lookup further?"
            select = raw_input()
            if select.lower() != "no":
                try:
                    temp = bod[select]
                    kwargs = {"path":temp}
                    checkConfig(self,**kwargs)
                except KeyError as e:
                    print "Key not found =["
