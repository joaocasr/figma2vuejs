"""
os ficheiros na pasta teste irão simular por enquanto os dados obtidos da api
para nesta fase de development e debug nao atingir o limite da chamadas com o token obtido do figma
"""
import math,json,re,os,time,requests,wget
from dotenv import load_dotenv, find_dotenv
from parser.model.Mpage import Mpage
from parser.model.Melement import Melement
from parser.model.ContainerElement import ContainerElement
from parser.model.VectorElement import VectorElement
from parser.model.VectorStyle import VectorStyle
from parser.model.ImageElement import ImageElement
from parser.model.ShapeElement import ShapeElement
from parser.model.ShapeStyle import ShapeStyle
from parser.model.Mcomponent import Mcomponent
from parser.model.TextElement import TextElement
from parser.model.ContainerStyle import ContainerStyle
from parser.model.ImageStyle import ImageStyle
from parser.model.ComponentStyle import ComponentStyle
from parser.model.TextStyle import TextStyle
from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction 
from parser.model.CloseAction import CloseAction
from parser.model.OverlayAction import OverlayAction
from engine.stylegenerator import calculate_gradientDegree
from parser.assetsconverter import convertToDropdown, convertToSearchInput, convertToDatePicker, convertToSlider, convertToRating

allpages = {}
allimages = []
allsvgs = []
componentVariables = {}
# key: component_id ; value: MComponent
allcomponents = {}
pageComponents = {}
assetComponents = ["InputSearch","DatePicker","Dropdown","ReadOnlyRating"]
pageWidth = -1
tags = ["nav","footer","main","section","aside","article","p","header","h1","h2","h3","h4","h5","h6","ul","li"]
figmadata = {}

def getFigmaData(prototype):
    global allpages, allcomponents,pageComponents, figmadata
    prototype1 = "../tests/prototype"+str(prototype)+".json"

    with open(prototype1,"r") as file:
        data = json.load(file)
        figmadata = data
    project_name = figmadata["name"]
    parsePageEntities(figmadata)

    #"""
    #update overlay components coordinates
    for p in pageComponents:
        for c in pageComponents[p]:
            if(c.getTypeComponent()=="OVERLAY"):
                updateOverlayPosition(c,c.style.getOverlayVector()[0],c.style.getOverlayVector()[1],allpages[p].style.getWidth(),allpages[p].style.getHeight())
                allpages[p].addElement(c)
    #"""
    # assign the components for each page
    for p in pageComponents:
        if(p in allpages):
            allpages[p].components = pageComponents[p]
    #print(allpages['PrincipalPage'].elements)

    extractImages(project_name)
    extractSVGs(project_name)
    return (project_name, allpages)

def parsePageEntities(data):
    global allpages
    pages = []
    for page in data["document"]["children"][0]["children"]:
        if(page["type"]=="FRAME"):
            pagina = Mpage(page["name"],"/"+page["name"],page["id"])
            pages.append(pagina)
            allpages[pagina.getPagename()] = pagina
    iterate_nestedElements(data)
    return allpages

def iterate_nestedElements(data):    
    global allpages, pageWidth, primeVueComponents
    #iterate first for all the components nodes (except primevue components)
    for melement in data["document"]["children"][0]["children"]:
        elements = []
        if(melement["type"]=="COMPONENT" and "children" in melement and melement["name"] not in assetComponents):
            pageWidth = melement["absoluteRenderBounds"]["width"]*1.2
            for element in melement["children"]:
                component_width = melement["absoluteRenderBounds"]["width"]
                component_height = melement["absoluteRenderBounds"]["height"]
                componentX = melement["absoluteRenderBounds"]["x"]
                componentY = melement["absoluteRenderBounds"]["y"]
                #try:
                p = processElement(melement["name"],element["name"],element,component_width,component_height,componentX,componentY,melement)
                if(p!=None): elements.append(p)
                #except:
                    #raise Exception("Error while converting "+element["name"]+". Correct your prototype!")

            tag = getElementTag(melement)
            allcomponents[melement["id"]] = Mcomponent(melement["id"],melement["name"],tag,"",elements)
            setComponentStyle(melement)

    #iterate the frame nodes (represent the pages)
    for page in data["document"]["children"][0]["children"]:
        if(page["type"]=="FRAME" and "children" in page):
            pageWidth = page["absoluteRenderBounds"]["width"]
            for element in page["children"]:
                page_width = page["absoluteRenderBounds"]["width"]
                page_height = page["absoluteRenderBounds"]["height"]
                pageX = page["absoluteRenderBounds"]["x"]
                pageY = page["absoluteRenderBounds"]["y"]
                #try:
                p = processElement(page["name"],element["name"],element,page_width,page_height,pageX,pageY,element)
                if(p!=None): allpages[page["name"]].elements.append(p)
                #except:
                    #raise Exception("Error while converting "+element["name"]+". Correct your prototype!")

        else:
            continue

        setPageStyle(page["name"],page)


def processElement(pagename,name,data,page_width,page_height,pageX,pageY,firstlevelelem,parent_data=None):
    global allcomponents,pageComponents,allpages,pageWidth, figmadata, allimages, allsvgs
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

    (nr_columnstart,nr_columnend,nr_rowstart,nr_rowend) = getPosition(xielem,yielem,elementwidth,elementheight,page_width,page_height,nrrows)

    if(parent_data==None and nr_columnend==64):
        nrcolumn = nr_columnend
        nr_columnend = " span "+ str(nrcolumn)
    if(parent_data==None and nr_rowend==128):
        nrrow = nr_rowend
        nr_rowend = " span "+ str(nrrow)

    tag = getElementTag(data)
    scrollBehaviour = None

    melement = None
    # handling assets from components created
    if(data["name"]=="Dropdown" and data["type"]=="INSTANCE"):
        componentsetId = ""
        for id in figmadata["componentSets"]:
            if(figmadata["componentSets"][id]["name"]=="Dropdown"):
                componentsetId = id
                break
        componentset = None
        for c in figmadata["document"]["children"][0]["children"]:
            if(c["id"]==componentsetId):
                componentset = c
                break
        melement = convertToDropdown(componentset,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        elemid = getElemId(data["id"])
        if(not pagename in allpages):
            addComponentVariable(pagename,{"selectedOption"+elemid:'""'})
            addComponentVariable(pagename,{"allOptions"+elemid:melement.options})
            addComponentVariable(pagename,{"allOptionValues"+elemid:[]})
        else:
            allpages[pagename].addVariable({"selectedOption"+elemid:'""'})
            allpages[pagename].addVariable({"allOptions"+elemid:melement.options})
            allpages[pagename].addVariable({"allOptionValues"+elemid:[]})
        return melement
    elif(data["name"]=="ReadOnlyRating" and data["type"]=="INSTANCE"):
        melement = convertToRating(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"],True)
        if(not pagename in allpages):
            addComponentVariable(pagename,{melement.vmodel:'"'+str(melement.selected)+'"'})
        else:
            allpages[pagename].addVariable({melement.vmodel:'"'+str(melement.selected)+'"'})
        return melement
    elif(data["name"]=="InputSearch" and data["type"]=="INSTANCE"):
        componentsetId = data["componentId"]
        componentset = None
        for c in figmadata["document"]["children"][0]["children"]:
            if(c["id"]==componentsetId):
                componentset = c
                break
        melement = convertToSearchInput(componentset,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        allpages[pagename].addVariable({melement.vmodel:'""'})
        return melement
    elif(data["name"]=="DatePicker" and data["type"]=="INSTANCE"):
        componentsetId = data["componentId"]
        componentset = None
        for c in figmadata["document"]["children"][0]["children"]:
            if(c["id"]==componentsetId):
                componentset = c
                break
        melement = convertToDatePicker(componentset,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        allpages[pagename].addVariable({melement.vmodel:'""'})
        return melement
    elif((data["name"]=="Slider" or data["name"]=="DualSlider") and data["type"]=="INSTANCE"):
        componentsetId = figmadata["components"][data["componentId"]]["componentSetId"]
        componentset = None
        for c in figmadata["document"]["children"][0]["children"]:
            if(c["id"]==componentsetId):
                componentset = c
                break
        for c in figmadata["document"]["children"][0]["children"]:
            if(c["id"]==componentsetId):
                componentset = c
                break
        melement = convertToSlider(componentset,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        allpages[pagename].addVariable({melement.vmodel:'""'})
        return melement        
    elif(data["name"]=="Form" and data["type"]=="INSTANCE"):
        return None
    # handling VectorElements
    elif(data["type"]=="VECTOR"):
        style = VectorStyle(data["absoluteRenderBounds"]["x"],
                        data["absoluteRenderBounds"]["y"],
                        elementwidth,
                        elementheight,
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend)
        name = data["name"]
        if("#" in data["name"]): name = data["name"].split("#")[0]
        svgpath = re.sub(r"[\s,@\.-]","",name)

        allsvgs.append({"id":data["id"],"name":name})
        mvectorelement = VectorElement(data["id"],"img",data["name"],"/"+svgpath+".svg",style)
        melement = mvectorelement
    # handling ImageElement
    elif(data["type"]=="RECTANGLE" and any(("imageRef" in x) for x in data["fills"])):
        
        data["type"] = "IMAGE"
        style = ImageStyle(data["absoluteRenderBounds"]["x"],
                        data["absoluteRenderBounds"]["y"],
                        elementwidth,
                        elementheight,
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend
                        )
        if("cornerRadius" in data): style.setCornerRadius(data["cornerRadius"])
        if("rectangleCornerRadii" in data): setCornerRadius(style,data["rectangleCornerRadii"])
        for effect in data["effects"]:
            if effect["type"] == "DROP_SHADOW":
                rgba_shadow = (effect["color"]["r"]*255, effect["color"]["g"]*255, effect["color"]["b"]*255, effect["color"]["a"])
                shadowX , shadowY = (str(round(effect["offset"]["x"])), str(round(effect["offset"]["y"])))
                shadowRadius = str(round(effect["radius"]))+"px "
                spread = ""
                if("spread" in effect): spread = str(round(effect["spread"]))+"px "

                boxshadow = shadowX+"px " + shadowY+"px " + shadowRadius + spread + "rgba("+','.join(str(val) for val in rgba_shadow)+")"
                style.setBoxShadow(boxshadow)
        if(tag==""): tag = "img"
        
        name = data["name"]
        if("#" in data["name"]): name = data["name"].split("#")[0]
        imgpath = re.sub(r"[\s,@\.-]","",name)
        allimages.append({"id":data["id"],"name":name})
        mimagelement = ImageElement(data["id"],tag,data["name"],data["fills"][0]["imageRef"],style)
        mimagelement.setimgpath("/"+imgpath+".png")
        melement = mimagelement

    # handles shape elements
    elif(data["type"]=="STAR" or data["type"]=="REGULAR_POLYGON" or data["type"]=="RECTANGLE" or data["type"]=="ELLIPSE" or data["type"]=="LINE"):
        rotation = None
        if("rotation" in data):
            rotation = str(data["rotation"])+"rad"
        rgba = None

        colorData=""
        if(len(data["fills"])==0):
            colorData= "strokes"
        else:
            colorData= "fills"
        lineargradient=None    
        for fill in data[colorData]:
            if(fill["type"]=="SOLID"):
                if("color" in fill):
                    color = fill["color"]
                    a = color["a"]
                    if("opacity" in fill): a = fill["opacity"]
                    rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , a)
            if(fill["type"]=="GRADIENT_LINEAR"):
                lineargradient = calculate_gradientDegree(fill["gradientHandlePositions"][1],
                                                fill["gradientHandlePositions"][0],
                                                fill["gradientStops"][1],
                                                fill["gradientStops"][0])

        shapestyle = ShapeStyle(data["absoluteRenderBounds"]["x"],
                        data["absoluteRenderBounds"]["y"],
                        elementwidth,
                        elementheight,
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend)
        if(rgba!=None): shapestyle.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
        if(lineargradient!=None): shapestyle.setBackground(lineargradient)
        if(rotation!=None): shapestyle.setTransform(rotation)

        for effect in data["effects"]:
            if effect["type"] == "DROP_SHADOW":
                rgba_shadow = (effect["color"]["r"], effect["color"]["g"], effect["color"]["b"], effect["color"]["a"])
                shadowX , shadowY = (str(round(effect["offset"]["x"])), str(round(effect["offset"]["y"])))
                shadowRadius = str(round(effect["radius"]))+"px "
                spread = ""
                if("spread" in effect): spread = str(round(effect["spread"]))+"px "

                boxshadow = shadowX+"px " + shadowY+"px " + shadowRadius + spread + "rgba("+','.join(str(val) for val in rgba_shadow)+")"
                shapestyle.setBoxShadow(boxshadow)

        if("strokes" in data):
            for s in data["strokes"]:
                if("color" in s):
                    color = s["color"]
                    a = color["a"]
                    if("visible" in s and s["visible"]==False): a = 0
                    rgbaborder = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , a)
                    shapestyle.setBorderColor("rgba("+','.join(str(val) for val in rgbaborder)+")")
        if("strokeWeight" in data): shapestyle.setborderWidth(str(data["strokeWeight"]))
        if("cornerRadius" in data): shapestyle.setborderRadius(str(data["cornerRadius"]))

        if(data["type"]=="RECTANGLE" and "rectangleCornerRadii" in data): setCornerRadius(shapestyle,data["rectangleCornerRadii"])
        mshapeelement = ShapeElement(data["id"],tag,data["name"],data["type"],shapestyle)
        melement = mshapeelement
                  
    # handles TextElement
    elif(data["type"]=="TEXT"):

        fontsize = ((data["style"]["fontSize"]) / (pageWidth / 100))
        #lineheight = ((round(data["style"]["lineHeightPx"])) / (pageWidth / 100))
        lineheight = (round(data["style"]["lineHeightPx"])) 
        color = data["fills"][0]["color"]
        rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
        autoresize = None
        if("textAutoResize" in data["style"]):
            autoresize = data["style"]["textAutoResize"]
        style = TextStyle(data["absoluteRenderBounds"]["x"],
                        data["absoluteRenderBounds"]["y"],
                        elementwidth,
                        elementheight,
                        data["style"]["textAlignHorizontal"],
                        str(lineheight)+"px",
                        autoresize,
                        data["style"]["fontStyle"],
                        data["style"]["fontWeight"],
                        str(fontsize)+"vw",
                        data["style"]["fontFamily"],
                        "rgba("+','.join(str(val) for val in rgba)+")",
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend)
        mtextelement = TextElement(data["id"],tag,data["name"],data["characters"],style)
        melement = mtextelement
    
    elif(data["type"]=="INSTANCE"):
        scrollBehaviour = None
        if(data["scrollBehavior"]=="FIXED"): scrollBehaviour = "sticky"
        componentelement = Mcomponent(data["id"],data["name"],tag,"")
        componentStyle = setComponentStyle(data)
        componentStyle.setPosition(scrollBehaviour)
        componentStyle.setGridcolumnStart(nr_columnstart)
        componentStyle.setGridcolumnEnd(nr_columnend)
        componentStyle.setGridrowStart(nr_rowstart)
        componentStyle.setGridrowEnd(nr_rowend)
        componentStyle.setPosition(scrollBehaviour)
        componentStyle.setinstanceFromComponentId(data["componentId"])

        assignComponentData(componentelement)
        componentelement.setComponentStyle(componentStyle)
        pageComponents.setdefault(pagename, []).append(componentelement)
        melement = componentelement

    # handles ContainerElement
    elif(data["type"]=="FRAME" or data["type"]=="GROUP"):

        lineargradient = None
        rgba = None
        for background in data["background"]:

            if("color" in background):
                color = data["background"][0]["color"]
                rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
            elif(background["type"] == "GRADIENT_LINEAR"):
                lineargradient = calculate_gradientDegree(background["gradientHandlePositions"][1],
                                                background["gradientHandlePositions"][0],
                                                background["gradientStops"][1],
                                                background["gradientStops"][0])
            if("color" in background and "visible" in data["background"][0] and data["background"][0]["visible"]==False): rgba=None
            if(background["type"] == "GRADIENT_LINEAR" and "visible" in background and background["visible"]==False): lineargradient=None
        style = ContainerStyle()
        
        if(rgba!=None): style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
        if(lineargradient!=None): style.setBackground(lineargradient)

        style.setX(data["absoluteRenderBounds"]["x"])
        style.setY(data["absoluteRenderBounds"]["y"])
        style.setHeight(data["absoluteRenderBounds"]["height"])
        style.setWidth(data["absoluteRenderBounds"]["width"])
        style.setGridcolumnStart(nr_columnstart)
        style.setGridcolumnEnd(nr_columnend)
        style.setGridrowStart(nr_rowstart)
        style.setGridrowEnd(nr_rowend)
        if(data["scrollBehavior"]=="FIXED"): scrollBehaviour = "sticky"
        style.setPosition(scrollBehaviour)

        if("cornerRadius" in data):
            style.setBorderRadius(data["cornerRadius"])
        if("rectangleCornerRadii" in data): setCornerRadius(style,data["rectangleCornerRadii"])

        for effect in data["effects"]:
            if effect["type"] == "DROP_SHADOW":
                rgba_shadow = (effect["color"]["r"]*255, effect["color"]["g"]*255, effect["color"]["b"]*255, effect["color"]["a"])
                shadowX , shadowY = (str(round(effect["offset"]["x"])), str(round(effect["offset"]["y"])))
                shadowRadius = str(round(effect["radius"]))+"px "
                spread = "0px"
                if("spread" in effect): spread = str(round(effect["spread"]))+"px "

                boxshadow = shadowX+"px " + shadowY+"px " + shadowRadius + spread + "rgba("+','.join(str(val) for val in rgba_shadow)+")"
                style.setBoxShadow(boxshadow)

        for stroke in data["strokes"]:
            rgba_stroke = (stroke["color"]["r"]*255, stroke["color"]["g"]*255, stroke["color"]["b"]*255, stroke["color"]["a"])
            stroketype = str(stroke["type"]).lower()
            strokeWeight = str(data["strokeWeight"])+"px "

            borderstyle = strokeWeight + stroketype + " rgba("+','.join(str(val) for val in rgba_stroke)+")"
            style.setBorderStyle(borderstyle)
        melement = ContainerElement(data["id"],tag,data["name"],style)

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
                        # neste caso estamos apenas a criar o elemento com overlay position se for apenas um componente já que considero que os frames no primeiro nivel correspondem a paginas
                        # caso queira extender é essencial acrescentar um 'type' no Melement para ajustar as coordenadas no final
                        #  update the position of the component relatively to the node which will open the component overlay
                        compstyle = allcomponents[data["transitionNodeID"]].getComponentStyle()
                        (xe,ye) = (xielem,yielem)
                        (rx,ry) = (action["overlayRelativePosition"]["x"],action["overlayRelativePosition"]["y"])
                        (px,py) = (rx+xe,ry+ye)
                        (vx,vy) = (px-compstyle.getX(),py-compstyle.getY())
                        compstyle.setOverlayVector(vx,vy)

                        allcomponents[data["transitionNodeID"]].setComponentStyle(compstyle)
                        allcomponents[data["transitionNodeID"]].setTypeComponent("OVERLAY")
                        pageComponents.setdefault(pagename, []).append(allcomponents[data["transitionNodeID"]])
                        #allpages[pagename].addElement(allcomponents[data["transitionNodeID"]])

                        #adicionar variavel na pagina visto que o componente não estará visivel no imediato
                        idcomponent = getElemId(action["destinationId"])
                        allpages[pagename].addVariable({"show"+idcomponent:"false"})

                        overlayAction = OverlayAction(action["destinationId"])
                        interactionelement.addAction(overlayAction)
                if(action["type"]=="CLOSE"):
                    closeAction = CloseAction(firstlevelelem["id"])
                    interactionelement.addAction(closeAction)

        element_interactions.append(interactionelement)
    if(melement!=None):
        melement.setInteractions(element_interactions)
        if(firstlevelelem["type"]=="COMPONENT"):
            melement.setupperIdComponent(firstlevelelem["id"])

    myparent_data = data
    # Iterates for all nested children of each element
    if("children" in data):
        if(data["type"]=="FRAME" or data["type"]=="GROUP"):
            style.setDisplay("grid")
            style.setGridTemplateColumns("repeat(64,1fr)")
            style.setGridTemplateRows("repeat(64,1fr)")
        for element in data["children"]:
            nestedelem = processElement(pagename,element["name"],element,data["absoluteRenderBounds"]["width"],data["absoluteRenderBounds"]["height"],pageX,pageY,firstlevelelem,myparent_data)
            children.append(nestedelem)

        if(melement!=None): melement.setChildren(children)
    return melement

# auxiliar funcion to calculate position 
def getPosition(xielem,yielem,elementwidth,elementheight,page_width,page_height, nrrows):

    nr_columnstart = max(round((xielem / page_width) * 64 ) + 1,1)
    nr_columnend = min(round((elementwidth / page_width) * 64) + 1 + nr_columnstart,65)

    nr_rowstart = round((yielem / page_height) * nrrows ) + 1
    nr_rowend = min(round((elementheight / page_height) * nrrows) + nr_rowstart, nrrows)

    #if(nr_columnstart<0): nr_columnstart=max(abs(nr_columnstart),1)
    #if(nr_columnend<0): nr_columnend=min(abs(nr_columnend),65)
    #if(nr_rowstart<0): nr_rowstart=abs(nr_rowstart)
    #if(nr_rowend<0): nr_rowend=min(abs(nr_rowend),nrrows)
    return (nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)


def setPageStyle(pagename,pagedata):
    global allpages

    lineargradient = None
    rgba = None
    for background in pagedata["background"]:

        if("color" in background):
            color = pagedata["background"][0]["color"]
            rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
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
    if(len(component["background"])>0):
        for background in component["background"]:

            if("color" in background):
                color = component["background"][0]["color"]
                rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
            elif(background["type"] == "GRADIENT_LINEAR"):
                lineargradient = calculate_gradientDegree(background["gradientHandlePositions"][0],
                                                background["gradientHandlePositions"][1],
                                                background["gradientStops"][0],
                                                background["gradientStops"][1])
    else:
        rgba = (component["backgroundColor"]["r"] * 255 , component["backgroundColor"]["g"] * 255 , component["backgroundColor"]["b"] * 255 , component["backgroundColor"]["a"])
    id = component["id"]

    componentStyle = ComponentStyle()
    componentStyle.setX(component["absoluteRenderBounds"]["x"])
    componentStyle.setY(component["absoluteRenderBounds"]["y"])
    componentStyle.setWidth(component["absoluteRenderBounds"]["width"])
    componentStyle.setHeight(component["absoluteRenderBounds"]["height"])
    if(rgba!=None): componentStyle.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
    if(lineargradient!=None): componentStyle.setBackground(lineargradient)
    componentStyle.setDisplay("grid")
    componentStyle.setMargin("0")
    componentStyle.setPadding("0")
    componentStyle.setGridTemplateColumns("repeat(64,1fr)")
    componentStyle.setGridTemplateRows("repeat(64,1fr)")
    if("cornerRadius" in component):
        componentStyle.setBorderRadius(component["cornerRadius"])

    for effect in component["effects"]:
        if effect["type"] == "DROP_SHADOW":
            rgba_shadow = (effect["color"]["r"]*255, effect["color"]["g"]*255, effect["color"]["b"]*255, effect["color"]["a"])
            shadowX , shadowY = (str(round(effect["offset"]["x"])), str(round(effect["offset"]["y"])))
            shadowRadius = str(round(effect["radius"]))+"px "
            spread = "0px"
            if("spread" in effect): spread = str(round(effect["spread"]))+"px "

            boxshadow = shadowX+"px " + shadowY+"px " + shadowRadius + spread + " rgba("+','.join(str(val) for val in rgba_shadow)+")"
            componentStyle.setBoxShadow(boxshadow)

    for stroke in component["strokes"]:
        rgba_stroke = (stroke["color"]["r"]*255, stroke["color"]["g"]*255, stroke["color"]["b"]*255, stroke["color"]["a"])
        stroketype = str(stroke["type"]).lower()
        strokeWeight = str(component["strokeWeight"])+"px "

        borderstyle = strokeWeight + stroketype + " rgba("+','.join(str(val) for val in rgba_stroke)+")"
        componentStyle.setBorderStyle(borderstyle)
    
    if(id in allcomponents): allcomponents[id].setComponentStyle(componentStyle)

    return componentStyle


def updateOverlayPosition(component, vx, vy, page_width, page_height):
    if isinstance(component, (Mcomponent, TextElement, ContainerElement )):
        if isinstance(component, Mcomponent):
            nrrows = 128 
        else:
            nrrows = 64
        (columnstart, columnend, rowstart, rowend) = getPosition(component.style.getX() + vx,
                                                                component.style.getY() + vy,
                                                                component.style.getWidth(),
                                                                component.style.getHeight(),
                                                                page_width,
                                                                page_height,
                                                                nrrows
                                                            )
        component.style.setGridcolumnStart(columnstart)
        component.style.setGridcolumnEnd(columnend)
        component.style.setGridrowStart(rowstart)
        component.style.setGridrowEnd(rowend)

    if(component!=None and component.children):
        for element in component.children:
            updateOverlayPosition(element, vx, vy, page_width, page_height)

def setCornerRadius(style,corners):
    style.setBorderTopLeftRadius(str(corners[0]))
    style.setBorderTopRightRadius(str(corners[1]))
    style.setBorderBottomRightRadius(str(corners[2]))
    style.setBorderBottomLeftRadius(str(corners[3]))

def getElementTag(elem):
    global tags
    tag = ""
    if("#" in elem["name"]):
        ntag = elem["name"].split("#")[1]
        if(ntag.lower() in tags):
            tag = ntag.lower()
    return tag

def extractImages(projectname):
    global allimages
    load_dotenv(find_dotenv())
    FIGMA_API_KEY = os.environ.get("FIGMA_API_KEY")
    FILE_KEY = os.environ.get("FILE_KEY")
    myimageids = ','.join(x["id"] for x in allimages)
    
    url = f"https://api.figma.com/v1/images/"+FILE_KEY+"/?ids="+myimageids+"&format=png"
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}

    resultingImages = []
    for mimage in allimages:
        imgpath = re.sub(r"[\s,@\.-]","",mimage["name"])
        destination = '../output/'+projectname+"/public/"+imgpath+".png"

        if(not os.path.isfile(destination)):
            filteredImages = list(filter(lambda x: x["name"]==mimage["name"],allimages))
            resultingImages.extend(filteredImages)

    if(len(resultingImages)>0):
        response = requests.get(url, headers=headers)
        images = response.json()
        if("err" in images and images["err"]==None):
            for mimage in resultingImages:
                imgurl = images["images"][str(mimage["id"])]
                imgpath = re.sub(r"[\s,@\.-]","",mimage["name"])
                if(imgurl!=None):
                    destination = '../output/'+projectname+"/public/"+imgpath+".png"
                    print("\nDownloading image "+imgpath+"...")
                    if(not os.path.isfile(destination)):
                        filename = wget.download(imgurl, out=destination)
                else:
                    destination = '../output/'+projectname+"/public/"+imgpath+".png"
                    wget.download("https://demofree.sirv.com/nope-not-here.jpg",out=destination)
        elif(images["status"]==403):
            print("something went wrong...")

def extractSVGs(projectname):
    global allsvgs
    load_dotenv(find_dotenv())
    FIGMA_API_KEY = os.environ.get("FIGMA_API_KEY")
    FILE_KEY = os.environ.get("FILE_KEY")
    mysvgsids = ','.join(x["id"] for x in allsvgs)
    
    url = f"https://api.figma.com/v1/images/"+FILE_KEY+"/?ids="+mysvgsids+"&format=svg"
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}

    resultingSvgs = []
    for msvg in allsvgs:
        svgpath = re.sub(r"[\s,@\.-]","",msvg["name"])
        destination = '../output/'+projectname+"/public/"+svgpath+".svg"
        if(not os.path.isfile(destination)):
            filteredSvgs = list(filter(lambda x: x["name"]==msvg["name"],allsvgs))
            resultingSvgs.extend(filteredSvgs)

    if(len(resultingSvgs)>0):
        response = requests.get(url, headers=headers)
        svgs = response.json()
        if("err" in svgs and svgs["err"]==None):
            for msvg in resultingSvgs:
                svgurl = svgs["images"][str(msvg["id"])]
                svgpath = re.sub(r"[\s,@\.-]","",msvg["name"])

                destination = '../output/'+projectname+"/public/"+svgpath+".svg"
                print("\nDownloading image "+svgpath+"...")
                if(not os.path.isfile(destination)):
                    filename = wget.download(svgurl, out=destination)
        elif(images["status"]==403):
            print("something went wrong...")

def addComponentVariable(componentName,var):
    global pageComponents, componentVariables
    for idp in pageComponents:
        for compp in pageComponents[idp]:
            if(compp.getNameComponent()==componentName):
                if(not var in pageComponents[idp]): 
                    pageComponents[idp].addVariable(var)
    componentVariables.setdefault(componentName, []).append(var)

def assignComponentData(component):
    if(component.getNameComponent() in componentVariables):
        for v in componentVariables[component.getNameComponent()]:
            component.addVariable(v)

def getElemId(id):
    elemid = id
    if(str(id).startswith("I")):
        ids = id.split(";")
        elemid = str(ids[len(ids)-1])
    pattern = "[:;]"
    elemid = re.sub(pattern,"",elemid)
    return elemid
