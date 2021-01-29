import os
import json

def ImportJsonFile(filename):
    cwd = os.getcwd()
    f = open(os.path.join(cwd, filename), "r")
    jfile = json.loads(f.read())
    return jfile

def GetSchema(resource, cleanse = True):
    swaggerfilename = "swagger.json"
    swaggerfile = ImportJsonFile(swaggerfilename)
    schema = swaggerfile['components']['schemas'][resource]['properties']
    if cleanse is True:
        schema = Cleanse(schema)
    return schema

def Cleanse(dict):
    for i in dict:
        dict[i] = None
    return dict
