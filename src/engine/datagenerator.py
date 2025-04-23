from utils.processing import getFormatedName,getElemId
pageEntities = dict()

def getObjectsDL(pagemame):
    global pageEntities
    return pageEntities[pagemame]
    
def buildPageEntities(container,pagename):
    global pageEntities
    if(pagename in pageEntities and "list"+container not in pageEntities[pagename]): pageEntities[pagename]["list"+container]= []
    elif(pagename not in pageEntities):
        pageEntities[pagename]={}
        pageEntities[pagename]["list"+container]= []

def parseEntity(data,entityname,id,pagename,container):
    if(data["type"]=="TEXT"):
        attr = "atr"+getElemId(data["id"])
        buildEntity(container,pagename,id,attr,entityname,data["characters"])
    if("children" in data):
        for c in data["children"]:
            parseEntity(c,entityname,id,pagename,container)

def buildEntity(container,pagename,id,attr,entityname,value):
    global pageEntities
    exists = False 
    for idx,item in enumerate(pageEntities[pagename]["list"+container]):
        if(item["id"]==id):
            item["atributes"][attr]=value
            pageEntities[pagename]["list"+container][idx]=item
            exists=True
    if(exists==False):
        item = {}
        item["id"]=id
        item["name"]=entityname
        if("atributes" not in item): item["atributes"]={}
        item["atributes"][attr]=value
        pageEntities[pagename]["list"+container].append(item)