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
    schema['child'] = [{'filter': MulticastSendingFilter(ip, port)}]
    schema['name'] = "CT MC to {} with {}".format(ip, port)
    schema['description'] = "FilterList to allow the sending of multicast to the address of {} using UDP port {}".format(ip, port)
    schema.pop('createdOn')
    return nonulls(schema)

def MulticastSendingFilter(ip, port):
    schema = functions.GetSchema("Filter")
    schema['ipAddress'] = ip
    schema['qualifier'] = [Qualifier(port)]
    return nonulls(schema)

def QualifierFilter(port):
    schema = functions.GetSchema("QualifierFilter")
    schema["localPort"] = "*"
    schema["remotePort"] = port
    schema["exclude"] = False
    schema["protocol"] = "UDP"
    return nonulls(schema)

def nonulls(schema):
    newschema = {}
    for key in schema:
        if schema[key] is not None:
            newschema[key] = schema[key]
    return newschema

def Qualifier(port):
    schema = functions.GetSchema("Qualifier")
    schema["filter"] = [QualifierFilter(port)]
    schema["isProtocolQualifier"] = True
    schema["name"] = "MultiCast Sender Port {}".format(port)
    return nonulls(schema)

def Post(component, resource, data):
    headers = {'Accept':'application/json'}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    baseurl = functions.ImportJsonFile("swagger.json")['servers'][0]['url'].replace('ecoapi-host','localhost')
    url = baseurl + "latest/" + resource
    print(json.dumps(data, indent=2))
    r = requests.post(url=url, auth=GetCreds(component), json=data, headers=headers, verify=False)
    return r.text

data = {"name": 'name', "description": 'description', "child": [{"filter": {"ipAddress": "8.8.8.8"}}]}

r = Post("stealth","filterList", MulticastSendingFilterList("244.0.0.50", "50"))

print(r)