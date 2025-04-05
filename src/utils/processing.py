import re 
import os

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

def doesImageExist(pathname,elem,projectname):
    destination = '../output/'+projectname+"/public/"+pathname
    if not os.path.exists(destination) and ".png" in destination:
        elem.setimgpath("https://demofree.sirv.com/nope-not-here.jpg")
    if not os.path.exists(destination) and ".svg" in destination:
        elem.setsvgpath("https://placehold.co/50x50.svg?text=PLACEHOLDER")