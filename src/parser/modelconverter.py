"""
os ficheiros na pasta teste irão simular por enquanto os dados obtidos da api
para nesta fase de development e debug nao atingir o limite da chamadas com o token obtido do figma
"""
import json
from parser.model.Mpage import Mpage
from parser.model.Melement import Melement
from parser.model.ContainerStyle import ContainerStyle

allpages = {}

def getFigmaData():
    prototype1 = "../tests/prototype3.json"
    figmadata = {}
    with open(prototype1,"r") as file1:
        data = json.load(file1)
        figmadata = data
    project_name = figmadata["name"]
    pages = parsePageEntities(figmadata)
    return (project_name,
            pages)

def parsePageEntities(data):
    pages = []
    for page in data["document"]["children"][0]["children"]:
        if(page["type"]=="FRAME"):
            pagina = Mpage(page["name"],
                            "/"+page["name"],
                            page["id"])
            pages.append(pagina)
            allpages[pagina.getPagename()] = pagina
    iterate_nestedElements(data)
    return allpages

def iterate_nestedElements(data):    
    for page in data["document"]["children"][0]["children"]:
        if(page["type"]=="FRAME" and "children" in page):
            for element in page["children"]:
                p = processElement(element["name"],element)
                allpages[page["name"]].elements.append(p)
        setPageStyle(page["name"],page)


def processElement(name,data):

    children = []
    melement = Melement(data["id"],"")
    if("children" in data):
        for element in data["children"]:
            nestedelem = processElement(element["name"],element)
            children.append(nestedelem)

    melement.setChildren(children)
    return melement


def setPageStyle(pagename,pagedata):
    color = pagedata["background"][0]["color"] #retificar porque pode haver mais do que uma cor e diferentes tonalidades
    rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
    #still dummy
    style = ContainerStyle(pagedata["absoluteRenderBounds"]["width"],
                           pagedata["absoluteRenderBounds"]["height"],
                           "rgba("+','.join(str(val) for val in rgba)+")",
                           "grid",
                           "0",
                           "0",
                           "repeat(16,1fr)",
                           "repeat(16,1fr)"
    )
    allpages[pagename].setPageStyle(style)