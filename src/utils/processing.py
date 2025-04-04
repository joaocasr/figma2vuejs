import re 

def getElemId(id):
    elemid = id
    if(str(id).startswith("I")):
        ids = id.split(";")
        elemid = str(ids[len(ids)-1])
    pattern = "[:;]"
    elemid = re.sub(pattern,"",elemid)
    return elemid

def getFormatedName(name):
    name = re.sub('([0-9]*)(.*)',r'\2',name)
    pattern = "[\s\.\-\/\\;#:]"
    name = re.sub(pattern,"",name)
    return name
