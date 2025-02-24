"""
os ficheiros na pasta teste irão simular por enquanto os dados obtidos da api
para nesta fase de development e debug nao atingir o limite da chamadas com o token obtido do figma
"""
import json
from parser.model.Mpage import Mpage
from parser.model.Melement import Melement
from parser.model.ContainerElement import ContainerElement
from parser.model.TextElement import TextElement
from parser.model.ContainerStyle import ContainerStyle
from parser.model.TextStyle import TextStyle
from parser.model.InteractionElement import InteractionElement

allpages = {}

def getFigmaData():
    prototype1 = "../tests/prototype7.json"
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
                page_width = page["absoluteRenderBounds"]["width"]
                page_height = page["absoluteRenderBounds"]["height"]
                pageX = page["absoluteRenderBounds"]["x"]
                pageY = page["absoluteRenderBounds"]["y"]
                p = processElement(element["name"],element,page_width,page_height,pageX,pageY)

                allpages[page["name"]].elements.append(p)
        else:
            continue

        setPageStyle(page["name"],page)


def processElement(name,data,page_width,page_height,pageX,pageY,parent_data=None):

    children = []

    elementwidth = data["absoluteRenderBounds"]["width"]
    elementheight = data["absoluteRenderBounds"]["height"]
    

    xielem = data["absoluteRenderBounds"]["x"]
    yielem = data["absoluteRenderBounds"]["y"]

    nrrows = 16

    # normalize the coordinates referencial
    if(pageX>0):
        xielem -= pageX
    if(pageY>0):
        yielem -= pageY


    if(parent_data!=None): #verifcar istooo
        xielem -= parent_data["absoluteRenderBounds"]["x"]
        yielem -= parent_data["absoluteRenderBounds"]["y"]

    else:
              
        nrrows = 48 #if it is first level element, then position it in the grid of 48 rows

    nr_columnstart = max(round((xielem / page_width) * 16 ) + 1,1)
    nr_columnend = min(round((elementwidth / page_width) * 16) + 1 + nr_columnstart,16)

    nr_rowstart = round((yielem / page_height) * nrrows ) + 1
    nr_rowend = min(round((elementheight / page_height) * nrrows) + nr_rowstart,nrrows)

    if(parent_data==None and nr_columnend==16):
        nrcolumn = nr_columnend
        nr_columnend = " span "+ str(nrcolumn)
    if(parent_data==None and nr_rowend==48):
        nrrow = nr_rowend
        nr_rowend = " span "+ str(nrrow)

    melement = None
    if(data["type"]=="TEXT"):

        color = data["fills"][0]["color"]
        rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
        style = TextStyle(data["style"]["fontStyle"],
                        data["style"]["fontWeight"],
                        str(round(data["style"]["fontSize"]/1.5))+"px",
                        data["style"]["fontFamily"],
                        "rgba("+','.join(str(val) for val in rgba)+")",
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend)
        mtextelement = TextElement(data["id"],"",data["characters"],style)
        melement = mtextelement
    if(data["type"]=="FRAME"):

        color = data["fills"][0]["color"]
        rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
        style = ContainerStyle()
        
        #style.setWidth(data["absoluteRenderBounds"]["width"])
        #style.setHeight(data["absoluteRenderBounds"]["height"])
        style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")

        style.setGridcolumnStart(nr_columnstart)
        style.setGridcolumnEnd(nr_columnend)
        style.setGridrowStart(nr_rowstart)
        style.setGridrowEnd(nr_rowend)

        if("cornerRadius" in data):
            style.setBorderRadius(data["cornerRadius"])            

        mcontainerelement = ContainerElement(data["id"],"",style)

        element_interactions = []
        for interaction in data["interactions"]:
            type = interaction["trigger"]["type"]
            interaction = InteractionElement(type)
            element_interactions.append(interaction)
        mcontainerelement.setInteractions(element_interactions)

        melement = mcontainerelement

    myparent_data = data
    if("children" in data):
        for element in data["children"]:
            if(element["type"]=="FRAME"):
                style.setDisplay("grid")
                style.setGridTemplateColumns("repeat(16,1fr)")
                style.setGridTemplateRows("repeat(16,1fr)")
            nestedelem = processElement(element["name"],element,data["absoluteRenderBounds"]["width"],data["absoluteRenderBounds"]["height"],pageX,pageY,myparent_data)
            children.append(nestedelem)

    melement.setChildren(children)
    return melement


def setPageStyle(pagename,pagedata):
    color = {
        "r": 0,
        "g": 0,
        "b": 0,
        "a": 0.1
        }
    if("color" in pagedata["background"][0]):
        color = pagedata["background"][0]["color"] #retificar porque pode haver mais do que uma cor e diferentes tonalidades
    rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
    #still dummy
    style = ContainerStyle()
    style.setWidth(pagedata["absoluteRenderBounds"]["width"])
    style.setHeight(pagedata["absoluteRenderBounds"]["height"])
    style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
    style.setDisplay("grid")
    style.setMargin("0")
    style.setPadding("0")
    style.setGridTemplateColumns("repeat(16,1fr)")
    
    allpages[pagename].setPageStyle(style)