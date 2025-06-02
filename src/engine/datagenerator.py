from utils.tools import getFormatedName,getElemId
pageEntities = dict()
topElement = None

def getObjectsDL(pagemame):
    global pageEntities
    return pageEntities[pagemame]
    
def buildPageEntities(container,pagename):
    global pageEntities
    if(pagename in pageEntities and container!="" and "list"+container not in pageEntities[pagename]): pageEntities[pagename]["list"+container]= []
    elif(pagename not in pageEntities and container!=""):
        pageEntities[pagename]={}
        pageEntities[pagename]["list"+container]= []
    elif(pagename not in pageEntities and container==""):
        pageEntities[pagename]={}
        pageEntities[pagename]["dataObjects"]= []

def parseEntity(data,entityname,id,pagename,container,isTopElement):
    global topElement
    if(isTopElement==True):
        topElement = data
    if(data["type"]=="TEXT"):
        attr = "atr"+getElemId(data["id"])
        buildEntity(data,container,pagename,id,attr,entityname,data["characters"])
    if(data["type"]=="RECTANGLE" and any(("imageRef" in x) for x in data["fills"])):
        name = data["name"]
        if("#" in data["name"]): name = data["name"].split("#")[0]
        value = "/"+getFormatedName(name)+getElemId(data["id"])+".png"
        attr = "atr"+getElemId(data["id"])
        buildEntity(data,container,pagename,id,attr,entityname,value)
    if("children" in data):
        for c in data["children"]:
            parseEntity(c,entityname,id,pagename,container,False)

def buildEntity(data,container,pagename,id,attr,entityname,value):
    global pageEntities, topElement
    exists = False 
    lista = "list"+container
    if(container==""): lista="dataObjects"
    if(topElement["type"]=="INSTANCE" or topElement["type"]=="COMPONENT"):
        if(lista not in pageEntities[pagename]): pageEntities[pagename][lista]= []
        for idx,item in enumerate(pageEntities[pagename][lista]):
            if(item["id"]==id):
                item["atributes"][attr]=value
                pageEntities[pagename][lista][idx]=item
                exists=True
        if(exists==False):
            item = {}
            item["id"]=id
            item["name"]=entityname
            if("atributes" not in item): item["atributes"]={}
            item["atributes"][attr]=value
            pageEntities[pagename][lista].append(item)
    else:
        if("object"+getElemId(topElement["id"]) not in pageEntities[pagename]):
            item = {}
            item[attr] = value
            pageEntities[pagename]["object"+getElemId(topElement["id"])] = item
        else:
            item = pageEntities[pagename]["object"+getElemId(topElement["id"])]
            item[attr] = value
            pageEntities[pagename]["object"+getElemId(topElement["id"])] = item