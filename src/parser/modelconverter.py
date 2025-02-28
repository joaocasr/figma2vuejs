"""
os ficheiros na pasta teste irão simular por enquanto os dados obtidos da api
para nesta fase de development e debug nao atingir o limite da chamadas com o token obtido do figma
"""
import math
import json
from parser.model.Mpage import Mpage
from parser.model.Melement import Melement
from parser.model.ContainerElement import ContainerElement
from parser.model.Mcomponent import Mcomponent
from parser.model.TextElement import TextElement
from parser.model.ContainerStyle import ContainerStyle
from parser.model.ComponentStyle import ComponentStyle
from parser.model.TextStyle import TextStyle
from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction
from engine.stylegenerator import calculate_gradientDegree

allpages = {}

# key: component_id ; value: MComponent
allcomponents = {}

def getFigmaData(prototype):
    global allpages, allcomponents
    prototype1 = "../tests/prototype"+str(prototype)+".json"
    figmadata = {}
    with open(prototype1,"r") as file1:
        data = json.load(file1)
        figmadata = data
    project_name = figmadata["name"]
    pages = parsePageEntities(figmadata)
    return (project_name, pages, allpages)

def parsePageEntities(data):
    global allpages
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
    global allpages
    #iterate first for all the components nodes
    for melement in data["document"]["children"][0]["children"]:
        elements = []
        if(melement["type"]=="COMPONENT" and "children" in melement):
            for element in melement["children"]:
                component_width = melement["absoluteRenderBounds"]["width"]
                component_height = melement["absoluteRenderBounds"]["height"]
                componentX = melement["absoluteRenderBounds"]["x"]
                componentY = melement["absoluteRenderBounds"]["y"]
                p = processElement(element["name"],element,component_width,component_height,componentX,componentY)
                elements.append(p)
            
            allcomponents[melement["id"]] = Mcomponent(melement["id"],melement["name"],elements,"","")
            setComponentStyle(melement)

    #iterate the frame nodes (represent the pages)
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

    nrrows = 64

    # normalize the referencial coordinates
    if(parent_data!=None):
        xielem -= parent_data["absoluteRenderBounds"]["x"]
        yielem -= parent_data["absoluteRenderBounds"]["y"]

    else:
        if(pageX>0):
            xielem -= pageX
        if(pageY>0):
            yielem -= pageY
              
        nrrows = 128 #if it is first level element, then position it in the grid of 48 rows

    nr_columnstart = max(round((xielem / page_width) * 64 ) + 1,1)
    nr_columnend = min(round((elementwidth / page_width) * 64) + 1 + nr_columnstart,64)

    nr_rowstart = round((yielem / page_height) * nrrows ) + 1
    nr_rowend = min(round((elementheight / page_height) * nrrows) + nr_rowstart, nrrows)

    if(parent_data==None and nr_columnend==64):
        nrcolumn = nr_columnend
        nr_columnend = " span "+ str(nrcolumn)
    if(parent_data==None and nr_rowend==128):
        nrrow = nr_rowend
        nr_rowend = " span "+ str(nrrow)

    melement = None
    # handles TextElement
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
    # handles ContainerElement
    if(data["type"]=="FRAME"):


        lineargradient = None
        rgba = None
        for background in data["background"]:

            if("color" in background):
                color = data["background"][0]["color"]
                rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
            elif(background["type"] == "GRADIENT_LINEAR"):
                lineargradient = calculate_gradientDegree(background["gradientHandlePositions"][0],
                                                background["gradientHandlePositions"][1],
                                                background["gradientStops"][0],
                                                background["gradientStops"][1])
        
        style = ContainerStyle()
        
        if(rgba!=None): style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
        if(lineargradient!=None): style.setBackground(lineargradient)

        style.setGridcolumnStart(nr_columnstart)
        style.setGridcolumnEnd(nr_columnend)
        style.setGridrowStart(nr_rowstart)
        style.setGridrowEnd(nr_rowend)

        if("cornerRadius" in data):
            style.setBorderRadius(data["cornerRadius"])

        for effect in data["effects"]:
            if effect["type"] == "DROP_SHADOW":
                rgba_shadow = (effect["color"]["r"], effect["color"]["g"], effect["color"]["b"], effect["color"]["a"])
                shadowX , shadowY = (str(round(effect["offset"]["x"])), str(round(effect["offset"]["y"])))
                shadowRadius = str(round(effect["radius"]))+"px "
                spread = str(round(effect["spread"]))+"px "

                boxshadow = shadowX+"px " + shadowY+"px " + shadowRadius + spread + "rgba("+','.join(str(val) for val in rgba_shadow)+")"
                style.setBoxShadow(boxshadow)

        for stroke in data["strokes"]:
            rgba_stroke = (stroke["color"]["r"], stroke["color"]["g"], stroke["color"]["b"], stroke["color"]["a"])
            stroketype = str(stroke["type"]).lower()
            strokeWeight = str(data["strokeWeight"])+"px "

            borderstyle = strokeWeight + stroketype + " rgba("+','.join(str(val) for val in rgba_stroke)+")"
            style.setBorderStyle(borderstyle)

        mcontainerelement = ContainerElement(data["id"],"",style)

        element_interactions = []
        for interaction in data["interactions"]:
            type = interaction["trigger"]["type"]
            if(type == "ON_CLICK"):
                interactionelement = InteractionElement()
                interactionelement.setInteractionType(InteractionElement.Interaction.ONCLICK)

            for action in interaction["actions"]:
                if(action["type"]=="NODE" and action["navigation"]=="NAVIGATE"):
                    navigateAction = NavigationAction(action["destinationId"])
                    interactionelement.addAction(navigateAction)
                if(action["type"]=="NODE" and action["navigation"]=="OVERLAY"):
                    if(action["destinationId"] in allcomponents):
                        #  update the position of the component relatively to the node which will open the component overlay
                        compstyle = allcomponents[data["transitionNodeID"]].getComponentStyle()
                        (columnstart,columnend,rowstart,rowend)= calculate_RelativePosition(xielem+action["overlayRelativePosition"]["x"],
                                                                                            yielem+action["overlayRelativePosition"]["y"],
                                                                                            compstyle.getWidth(),
                                                                                            compstyle.getHeight(),
                                                                                            page_width,
                                                                                            page_height)
                        compstyle.setGridcolumnStart(columnstart)
                        compstyle.setGridcolumnEnd(columnend)
                        compstyle.setGridrowStart(rowstart)
                        compstyle.setGridrowEnd(rowend)
                        allcomponents[data["transitionNodeID"]].setComponentStyle(compstyle)

            element_interactions.append(interactionelement)
        mcontainerelement.setInteractions(element_interactions)

        melement = mcontainerelement

    myparent_data = data
    # Iterates for all nested children of each element
    if("children" in data):
        if(data["type"]=="FRAME"):
            style.setDisplay("grid")
            style.setGridTemplateColumns("repeat(64,1fr)")
            style.setGridTemplateRows("repeat(64,1fr)")
        for element in data["children"]:
            nestedelem = processElement(element["name"],element,data["absoluteRenderBounds"]["width"],data["absoluteRenderBounds"]["height"],pageX,pageY,myparent_data)
            children.append(nestedelem)

        melement.setChildren(children)
    return melement

# auxiliar funcion to calculate relative position when navigation is "OVERLAY"  
def calculate_RelativePosition(xielem,yielem,elementwidth,elementheight,page_width,page_height):

    nr_columnstart = max(round((xielem / page_width) * 64 ) + 1,1)
    nr_columnend = min(round((elementwidth / page_width) * 64) + 1 + nr_columnstart,64)

    nr_rowstart = round((yielem / page_height) * 128 ) + 1
    nr_rowend = min(round((elementheight / page_height) * 128) + nr_rowstart, 128)

    return (nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)


def setPageStyle(pagename,pagedata):
    global allpages

    lineargradient = None
    rgba = None
    for background in pagedata["background"]:

        if("color" in background):
            color = pagedata["background"][0]["color"]
            rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
        elif(background["type"] == "GRADIENT_LINEAR"):
            lineargradient = calculate_gradientDegree(background["gradientHandlePositions"][0],
                                            background["gradientHandlePositions"][1],
                                            background["gradientStops"][0],
                                            background["gradientStops"][1])

    style = ContainerStyle()
    style.setWidth(pagedata["absoluteRenderBounds"]["width"])
    style.setHeight(pagedata["absoluteRenderBounds"]["height"])
    if(rgba!=None): style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
    if(lineargradient!=None): style.setBackground(lineargradient)
    style.setDisplay("grid")
    style.setMargin("0")
    style.setPadding("0")
    style.setGridTemplateColumns("repeat(64,1fr)")
    
    allpages[pagename].assignPageStyle(style)

def setComponentStyle(component):
    global allcomponents


    lineargradient = None
    rgba = None
    for background in component["background"]:

        if("color" in background):
            color = component["background"][0]["color"]
            rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"] * 255)
        elif(background["type"] == "GRADIENT_LINEAR"):
            lineargradient = calculate_gradientDegree(background["gradientHandlePositions"][0],
                                            background["gradientHandlePositions"][1],
                                            background["gradientStops"][0],
                                            background["gradientStops"][1])

    id = component["id"]
    # falta fazer a verificacao do tipo de componente e atribuir os estilos apropriados
    componentStyle = ComponentStyle()
    componentStyle.setWidth(component["absoluteRenderBounds"]["width"])
    componentStyle.setHeight(component["absoluteRenderBounds"]["height"])
    if(rgba!=None): componentStyle.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
    if(lineargradient!=None): componentStyle.setBackground(lineargradient)
    componentStyle.setDisplay("grid")
    componentStyle.setMargin("0")
    componentStyle.setPadding("0")
    componentStyle.setGridTemplateColumns("repeat(64,1fr)")
    allcomponents[id].setComponentStyle(componentStyle)