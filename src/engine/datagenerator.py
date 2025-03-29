pageEntities = dict()

def buildPageEntities(container,pagename):
    global pageEntities
    if pagename in pageEntities: pageEntities[pagename]["list"+container]= []
    else:
        pageEntities[pagename]={}
        pageEntities[pagename]["list"+container]= []

def buildEntity(container,pagename,entityname,attr,value):
    global pageEntities
    exists = False 
    for idx,item in enumerate(pageEntities[pagename]["list"+container]):
        if(item["name"]==entityname):
            item[attr]=value
            pageEntities[pagename]["list"+container][idx]=item
            exists=True
    if(exists==False):
        item = {}
        item["name"]=entityname
        item[attr]=value
        pageEntities[pagename]["list"+container].append()