import json

def ReadConfig(configPath: str):

    jsonFile = open(configPath)

    configObject = json.load(jsonFile)

    return configObject["configurationInfos"]