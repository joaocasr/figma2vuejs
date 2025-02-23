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

allpages = {}

def getFigmaData():
    prototype1 = "../tests/prototype6.json"
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
                p = processElement(element["name"],element,page_width,page_height)

                allpages[page["name"]].elements.append(p)
        setPageStyle(page["name"],page)


def processElement(name,data,page_width,page_height,parent_data=None):

    children = []

    elementwidth = data["absoluteRenderBounds"]["width"]
    elementheight = data["absoluteRenderBounds"]["height"]
    

    xielem = data["absoluteRenderBounds"]["x"]
    yielem = data["absoluteRenderBounds"]["y"]

    nrrows = 16

    if(parent_data!=None):
        xielem -= parent_data["absoluteRenderBounds"]["x"]
        yielem -= parent_data["absoluteRenderBounds"]["y"]
    else:
        nrrows = 48 #if first level element then position it in the grid of 48 rows

    nr_columnstart = max(round((xielem / page_width) * 16 ) + 1,1)
    nr_columnend = min(round((elementwidth / page_width) * 16) + 1 + nr_columnstart,16)

    nr_rowstart = round((yielem / page_height) * nrrows ) + 1
    nr_rowend = min(round((elementheight / page_height) * nrrows) + nr_rowstart,nrrows+1)

    if(parent_data==None and nr_columnend==16):
        nrcolumn = nr_columnend
        nr_columnend = " span "+ str(nrcolumn)
    if(parent_data==None and nr_rowend==49):
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
        melement = mcontainerelement

    myparent_data = data
    if("children" in data):
        for element in data["children"]:
            if(element["type"]=="FRAME"):
                style.setDisplay("grid")
                style.setGridTemplateColumns("repeat(16,1fr)")
                style.setGridTemplateRows("repeat(16,1fr)")
            nestedelem = processElement(element["name"],element,data["absoluteRenderBounds"]["width"],data["absoluteRenderBounds"]["height"],myparent_data)
            children.append(nestedelem)

    melement.setChildren(children)
    return melement


def setPageStyle(pagename,pagedata):
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