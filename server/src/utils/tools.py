from parser.model.Mcomponent import Mcomponent
from parser.model.Melement import Melement
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
    pattern = "[\s\.\-\/\\;#=,:]"
    name = re.sub(pattern,"",name)
    return name

def doesImageExist(pathname,elem,projectname):
    destination = '../output/'+projectname+"/public/"+pathname
    if not os.path.exists(destination) and ".png" in destination:
        elem.setimgpath("https://demofree.sirv.com/nope-not-here.jpg")
    if not os.path.exists(destination) and ".svg" in destination:
        elem.setsvgpath("https://placehold.co/50x50.svg?text=PLACEHOLDER")        
        
def getName(e):
    if isinstance(e,Melement):
        name = getFormatedName(e.getName()) + getElemId(e.idElement)
    elif(isinstance(e,Mcomponent)):
        name = getFormatedName(e.getNameComponent()) + getElemId(e.idComponent)
    return name

def getId(e):
    if(isinstance(e,Melement)):
        return e.idElement
    elif(isinstance(e,Mcomponent)):
        return e.idComponent
