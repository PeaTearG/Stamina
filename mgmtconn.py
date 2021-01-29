import requests
import json
import functions
import urllib3

def GetCreds(component):
    credsfile = "creds.json"
    creds = functions.ImportJsonFile(credsfile)
    for cred in creds['components']:
        if cred['component'] == component:
            auth = (cred['username'], cred['password'])
    return auth

def MulticastSendingFilterList(ip, port):
    schema = functions.GetSchema("FilterList")
    schema['child'] = [MulticastSendingFilter(ip, port)]
    schema['name'] = "CT MC to {} with {}".format(ip, port)
    schema['description'] = "FilterList to allow the sending of multicast to the address of {} using UDP port {}".format(ip, port)
    return schema

def MulticastSendingFilter(ip, port):
    schema = functions.GetSchema("Filter")
    schema['ipAddress'] = ip
    schema['qualifier'] = Qualifier(port)
    return schema

def QualifierFilter(port):
    schema = functions.GetSchema("QualifierFilter")
    schema["localPort"] = "*"
    schema["remotePort"] = port
    schema["exclude"] = False
    schema["protocol"] = "UDP"
    return schema

def Qualifier(port):
    schema = functions.GetSchema("Qualifier")
    schema["filter"] = QualifierFilter(port)
    schema["isProtocolQualifier"] = True
    schema["name"] = "MultiCast Sender Port {}".format(port)
    return schema

def Post(component, resource, data):
    headers = {'Accept':'application/json'}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = requests.post(url=functions.ImportJsonFile("swagger.json")['servers'][0]['url'].replace('ecoapi-host','localhost')+resource, auth=GetCreds(component), json=data, headers=headers)
    return r.text
