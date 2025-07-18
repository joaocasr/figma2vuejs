import re,os,requests,wget
from parser.model.Mpage import Mpage
from parser.model.Melement import Melement
from parser.model.ContainerElement import ContainerElement
from parser.model.VectorElement import VectorElement
from parser.model.VectorStyle import VectorStyle
from parser.model.ImageElement import ImageElement
from parser.model.ShapeElement import ShapeElement
from parser.model.ShapeStyle import ShapeStyle
from parser.model.Mcomponent import Mcomponent
from parser.model.VariantComponent import VariantComponent
from parser.model.TextElement import TextElement
from parser.model.ContainerStyle import ContainerStyle
from parser.model.ImageStyle import ImageStyle
from parser.model.ComponentStyle import ComponentStyle
from parser.model.TextStyle import TextStyle
from parser.model.VideoElement import VideoElement
from parser.model.VideoStyle import VideoStyle
from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction 
from parser.model.OpenLinkAction import OpenLinkAction 
from parser.model.BackAction import BackAction 
from parser.model.SwapAction import SwapAction 
from parser.model.CloseAction import CloseAction
from parser.model.OverlayAction import OverlayAction
from parser.model.ScrollAction import ScrollAction
from parser.model.ChangeAction import ChangeAction
from parser.model.Transition import Transition
from engine.stylegenerator import calculate_lineargradientDegree, calculate_radialgradientDegree,calculate_angulargradientDegree
from engine.datagenerator import buildPageEntities,parseEntity,getObjectsDL
from parser.assetsconverter import convertToDropdown, convertToSearchInput, convertToDatePicker, convertToSlider, convertToRating, convertToPaginator, convertToForm, convertToCheckbox, convertToMenu, convertToTable
from utils.tools import getFormatedName,getElemId

allpages = {}
allimages = []
allsvgs = []
refs = {}
componentVariables = {}
componentProps = {}
variants = []
scrollElements = {}
# key: component_id ; value: MComponent
allcomponents = {}
pageComponents = {}
assetComponents = ["InputSearch","DatePicker","Dropdown","ReadOnlyRating","InteractiveRating","Paginator","Form","Checkbox","Video","Menu","Table"]
pageWidth = -1
tags = ["nav","footer","main","section","aside","article","p","header","h1","h2","h3","h4","h5","h6","ul","li"]
notPageElems = {}
overlayInsideInstances = {}
closeIds = []
pageOverlays = {}
event_EmissionPaths = {}
overlayTriggers = []
transition_nodeIds = []
logicDependentComponents = {}
figmadata = {}

batchi=0
batchf=50

def getFigmaData(data):
    global allpages, allcomponents,pageComponents, figmadata, refs, overlayInsideInstances, pageOverlays, overlayTriggers, variants, scrollElements, allimages, allsvgs, event_EmissionPaths, closeIds, logicDependentComponents
    if(data!=None):
        figmadata=data
    figmadata["name"] = getFormatedName(figmadata["name"])
    project_name = figmadata["name"]
    allpages = {}
    allcomponents = {}
    pageComponents = {}
    overlayInsideInstances = {}
    pageOverlays = {}
    overlayTriggers = []
    scrollElements = {}
    logicDependentComponents = {}
    transition_nodeIds = []
    event_EmissionPaths = {}
    variants = []
    closeIds = []
    allimages = []
    allsvgs = []
    parsePageEntities(figmadata)

    #update overlay components coordinates
    for p in pageComponents:
        for c in pageComponents[p]:
            if(c.getTypeComponent()=="OVERLAY" and p in allpages):
                updateOverlayPosition(c,c.style.getOverlayVector()[0],c.style.getOverlayVector()[1],allpages[p].style.getWidth(),allpages[p].style.getHeight())
                allpages[p].addElement(c)
            elif(c.getTypeComponent()=="OVERLAY" and p not in allpages):
                pass
                #print(c.getIdComponent())
            if(c.getIdComponent() in overlayInsideInstances):
                for i in overlayInsideInstances[c.getIdComponent()]:
                    if(i[0]==c.getIdComponent()):
                        c.addChildren(i[1])
                    manipulateComponentDom(c.children,i)
    # insert overlay frame elements on page
    for p in pageOverlays:
        for el in pageOverlays[p]:
            if p in allpages:
                if(el[0]==None):
                    allpages[p].addElement(el[1])
                else:
                    manipulateComponentDom(allpages[p].elements,el)
                
    # assign the components for each page
    for p in pageComponents:
        if(p in allpages):
            allpages[p].components = pageComponents[p]

    # update inner scroll elements
    for page in scrollElements:
        for el in scrollElements[page]:
            updateInnerChildren(allpages[page].elements,el)
    
    orphanComponents = []
    for id in allcomponents:
        l = []
        for p in pageComponents:
            filtered = list(map(lambda x : x.getNameComponent(),pageComponents[p]))
            l.extend(filtered)
        if(allcomponents[id].getNameComponent() not in l and allcomponents[id] not in orphanComponents):
            orphanComponents.append(allcomponents[id])

    #print(logicDependentComponents)
    for k in logicDependentComponents:
        el = logicDependentComponents[k]
        interactions = setLogic(el["melement"],
                 el["pagename"],el["data"],el["parent_data"],
                 el["firstlevelelem"],el["xielem"],el["yielem"],
                 el["elementwidth"],el["elementheight"],
                 el["page_width"],el["page_height"],el["pageX"],
                 el["pageY"],el["nr_columnstart"],el["nr_columnend"],
                 el["nr_rowstart"],el["nr_rowend"],[])
        for p in pageComponents:
            for c in pageComponents[p]:
                if(c.getIdComponent()==el["firstlevelelem"]["id"]): 
                    updateElement(c,el["data"]["id"],interactions)
                    updateComponentPage(p,c,allpages)

    closePaths = getClosePaths(closeIds,event_EmissionPaths)

    return (project_name, allpages, orphanComponents, refs, variants, transition_nodeIds, event_EmissionPaths, closePaths)

def parsePageEntities(data):
    global allpages
    for page in data["document"]["children"][0]["children"]:
        if(page["type"]=="FRAME" and "#Page" in page["name"]):
            pagina = Mpage(page["name"],page["name"],page["id"])
            if(pagina.getPagename() not in allpages):
                allpages[pagina.getPagename()] = pagina
            else:
                page["name"] = page["name"]+getElemId(page["id"])
                pagina = Mpage(page["name"],page["name"],page["id"])
                allpages[pagina.getPagename()] = pagina                
    iterate_nestedElements(data)
    return allpages

def iterate_nestedElements(data):    
    global allpages, pageWidth, primeVueComponents, notPageElems, variants
    
    # iterate the frames and groups on first level of the whiteboard which are NOT PAGES
    for page in data["document"]["children"][0]["children"]:
        if((page["type"]=="FRAME" or page["type"]=="GROUP") and "children" in page and "#Page" not in page["name"]):
            notPageElems[page["id"]]=page

    #iterate first for all the components nodes (except primevue & vuetify components)
    #l =orderComponents(data["document"]["children"][0]["children"])
    for melement in data["document"]["children"][0]["children"]:
        elements = []
        if((melement["type"]=="COMPONENT" or isComponentVariant(melement,variants)==True) and "children" in melement and melement["name"] not in assetComponents):
            pageWidth = melement["absoluteRenderBounds"]["width"]*1.2
            interactions = []
            for element in melement["children"]:
                component_width = melement["absoluteRenderBounds"]["width"]
                component_height = melement["absoluteRenderBounds"]["height"]
                componentX = melement["absoluteRenderBounds"]["x"]
                componentY = melement["absoluteRenderBounds"]["y"]
                #try:
                p = processElement(melement["name"],element["name"],element,component_width,component_height,componentX,componentY,melement)
                if(p!=None): elements.append(p)
                #except:
                #    raise Exception("Error while converting "+element["name"]+". Correct your prototype!")
            if(len(melement["interactions"])>0):
                interactions = setLogic(melement,melement["name"],melement,None,melement,melement["absoluteRenderBounds"]["x"],melement["absoluteRenderBounds"]["y"],melement["absoluteRenderBounds"]["width"],melement["absoluteRenderBounds"]["height"],melement["absoluteRenderBounds"]["width"],melement["absoluteRenderBounds"]["height"],0,0,0,0,0,0,[])
            tag = getElementTag(melement)
            if(isComponentVariant(melement,variants)!=True):
                comp=Mcomponent(melement["id"],melement["name"],tag,"",elements)
                comp.addInteractionsList(interactions)
                allcomponents[melement["id"]] = comp
            if(isComponentVariant(melement,variants)==True):
                v = VariantComponent(melement["id"],tag,melement["name"],"",elements)
                setVariantProperties(v,melement["componentPropertyDefinitions"])
                addVariant(variants,v)
            setComponentStyle(melement)

    #iterate the frame nodes which represent PAGES
    for page in data["document"]["children"][0]["children"]:
        if(page["type"]=="FRAME" and "children" in page and "#Page" in page["name"]):
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
                #    raise Exception("Error while converting "+element["name"]+". Correct your prototype!")
        else:
            continue    
        setPageStyle(page["name"],page)


def processElement(pagename,name,data,page_width,page_height,pageX,pageY,firstlevelelem,parent_data=None):
    global allcomponents,pageComponents,allpages,pageWidth,figmadata,allimages,allsvgs,refs,overlayInsideInstances,pageOverlays,variants,scrollElements,overlayTriggers,transition_nodeIds
    children = []    
    if(data["absoluteRenderBounds"]!=None):
        elementwidth = data["absoluteRenderBounds"]["width"]
        elementheight = data["absoluteRenderBounds"]["height"]
        xielem = data["absoluteRenderBounds"]["x"]
        yielem = data["absoluteRenderBounds"]["y"]
    elif(data["absoluteBoundingBox"]!=None):
        elementwidth = data["absoluteBoundingBox"]["width"]
        elementheight = data["absoluteBoundingBox"]["height"]
        xielem = data["absoluteBoundingBox"]["x"]
        yielem = data["absoluteBoundingBox"]["y"]

    nrrows = 64

    # normalize the referencial coordinates
    if(parent_data!=None and parent_data["absoluteRenderBounds"]!=None):
        xielem -= parent_data["absoluteRenderBounds"]["x"]
        yielem -= parent_data["absoluteRenderBounds"]["y"]
    elif(parent_data!=None and parent_data["absoluteBoundingBox"]!=None):
        xielem -= parent_data["absoluteBoundingBox"]["x"]
        yielem -= parent_data["absoluteBoundingBox"]["y"]

    else:
        if(pageX!=0):
            xielem -= pageX
        if(pageY!=0):
            yielem -= pageY
              
        nrrows = 128 #if it is first level element, then position it in the grid of 48 rows
    if(firstlevelelem!=None and firstlevelelem["type"]=="COMPONENT"): nrrows=64
    (nr_columnstart,nr_columnend,nr_rowstart,nr_rowend) = getPosition(xielem,yielem,elementwidth,elementheight,page_width,page_height,nrrows)

    if(parent_data==None and nr_columnend==64):
        nrcolumn = nr_columnend
    if(parent_data==None and nr_rowend==128):
        nrrow = nr_rowend
        if(data["type"]=="INSTANCE"): nr_rowend= 129

    tag = getElementTag(data)
    scrollBehaviour = None
    isComponentInstance = False
    melement = None
    if(data["name"].lower().endswith("#data")):
        if(parent_data!=None):
            parentId = parent_data["id"]
        else: parentId = ""
        buildPageEntities(getElemId(parentId),getFormatedName(pagename))
        parseEntity(data,getFormatedName(data["name"].lower()),getElemId(data["id"]),getFormatedName(pagename),getElemId(parentId),True)
        objList=getObjectsDL(getFormatedName(pagename))
        if(pagename in allpages):
            allpages[pagename].setobjectDL(objList)
        if(data["type"]=="INSTANCE" or data["type"]=="COMPONENT"):
            for l in objList:
                for i in objList[l]:
                    if("name" in i and i["name"]==getFormatedName(data["name"].lower())):
                        addComponentProps(data["name"],i["atributes"])
    if(data["type"]=="COMPONENT"):
        elements = []
        for element in data["children"]:
            component_width = data["absoluteRenderBounds"]["width"]
            component_height = data["absoluteRenderBounds"]["height"]
            componentX = data["absoluteRenderBounds"]["x"]
            componentY = data["absoluteRenderBounds"]["y"]
                
            p = processElement(data["name"],element["name"],element,component_width,component_height,componentX,componentY,data)
            if(p!=None): elements.append(p)

        tag = getElementTag(data)
        style = setComponentStyle(data)
        allcomponents[data["id"]] = Mcomponent(data["id"],data["name"],tag,"",elements)
        allcomponents[data["id"]].setComponentStyle(style)
        melement = allcomponents[data["id"]]
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
    elif((data["name"]=="ReadOnlyRating" or data["name"]=="InteractiveRating") and data["type"]=="INSTANCE"):
        readOnly = False
        if(data["name"]=="ReadOnlyRating"): readOnly = True
        melement = convertToRating(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"],readOnly)
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
        if(not pagename in allpages):
            addComponentVariable(pagename,{melement.vmodel:'""'})
        else:
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
        if(not pagename in allpages):
            addComponentVariable(pagename,{melement.vmodel:'""'})
        else:
            allpages[pagename].addVariable({melement.vmodel:'""'})
        return melement
    elif((data["name"]=="Slider" or data["name"]=="DualSlider") and data["type"]=="INSTANCE"):
        componentsetId = figmadata["components"][data["componentId"]]["componentSetId"]
        componentset = None
        percent = 0
        if("componentProperties" in data and "Percent" in data["componentProperties"]):
            percent = int(data["componentProperties"]["Percent"]["value"])
        for c in figmadata["document"]["children"][0]["children"]:
            if(c["id"]==componentsetId):
                componentset = c
                break
        melement = convertToSlider(componentset,percent,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        if(not pagename in allpages):
            addComponentVariable(pagename,{melement.vmodel:melement.percentage})
        else:
            allpages[pagename].addVariable({melement.vmodel:melement.percentage})
        return melement        
    elif(data["name"]=="Paginator" and data["type"]=="INSTANCE"):
        melement = convertToPaginator(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        if(not pagename in allpages):
            addComponentVariable(pagename,{melement.vmodel:1})
        else:
            allpages[pagename].addVariable({melement.vmodel:1})
        return melement
    elif(data["name"]=="Form" and data["type"]=="INSTANCE"):
        melement = convertToForm(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        return melement
    elif(data["name"]=="Checkbox" and data["type"]=="INSTANCE"):
        elemid = getElemId(data["id"])
        melement = convertToCheckbox(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        if(not pagename in allpages):
            addComponentVariable(pagename,{"boxes"+elemid:[]})
            addComponentVariable(pagename,{"boxesValues"+elemid:melement.boxes})
            addComponentVariable(pagename,{"selectedBoxes"+elemid:[]})
        else:
            allpages[pagename].addVariable({"boxes"+elemid:[]})
            allpages[pagename].addVariable({"boxesValues"+elemid:melement.boxes})
            allpages[pagename].addVariable({"selectedBoxes"+elemid:[]})
        return melement
    elif(data["name"]=="Video" and data["type"]=="INSTANCE"):
        style = VideoStyle(data["absoluteRenderBounds"]["width"],data["absoluteRenderBounds"]["height"],
                                nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
        melement = VideoElement(data["id"],tag,data["name"],"https://www.youtube.com/embed/9ZIgQFKaK4Y",style)
        return melement
    elif(data["name"]=="Menu" and data["type"]=="INSTANCE"):
        melement = convertToMenu(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        if(melement.iconImage!=None): allimages.extend([melement.iconImage])
        menuid = getElemId(data["id"])
        if(not pagename in allpages):
            addComponentVariable(pagename,{f"menuoptions{menuid}":melement.options})
        else:
            allpages[pagename].addVariable({f"menuoptions{menuid}":melement.options})
        return melement
    elif(data["name"]=="Table" and data["type"]=="INSTANCE"):
        melement = convertToTable(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,data["id"],data["name"])
        allimages.extend(melement.images)
        tableid = getElemId(data["id"])
        if(not pagename in allpages):
            addComponentVariable(pagename,{f"tablevalues{tableid}":[]})
        else:
            allpages[pagename].addVariable({f"tablevalues{tableid}":[]})
        return melement
    # handling VectorElements
    elif(data["type"]=="VECTOR"):
        style = VectorStyle(xielem,
                        yielem,
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
        mvectorelement = VectorElement(data["id"],"img",data["name"],"/"+getFormatedName(svgpath)+getElemId(data["id"])+".svg",style)
        melement = mvectorelement
    # handling ImageElement
    elif(data["type"]=="RECTANGLE" and any(("imageRef" in x) for x in data["fills"])):
        
        data["type"] = "IMAGE"
        style = ImageStyle(xielem,
                        yielem,
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
        mimagelement.setimgpath("/"+getFormatedName(imgpath)+getElemId(data["id"])+".png")
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
        gradient=None    
        for fill in data[colorData]:
            if(fill["type"]=="SOLID"):
                if("color" in fill):
                    color = fill["color"]
                    a = color["a"]
                    if("opacity" in fill): a = fill["opacity"]
                    rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , a)
            if(fill["type"]=="GRADIENT_LINEAR"):
                gradient = calculate_lineargradientDegree(fill["gradientHandlePositions"],fill["gradientStops"])
            if(fill["type"]=="GRADIENT_RADIAL"):
                gradient = calculate_radialgradientDegree(fill["gradientHandlePositions"],fill["gradientStops"])
            if(fill["type"]=="GRADIENT_ANGULAR"):
                gradient = calculate_angulargradientDegree(fill["gradientHandlePositions"],fill["gradientStops"])
        shapestyle = ShapeStyle(xielem,
                        yielem,
                        elementwidth,
                        elementheight,
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend)
        if(rgba!=None): shapestyle.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
        if(gradient!=None): shapestyle.setBackground(gradient)
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
        if("visible" in data and data["visible"]==False): shapestyle.setDisplay("none")
        if("opacity" in data): shapestyle.setOpacity(str(data["opacity"]*100)+"%")
        if(shapestyle.getDisplay()==None and elementheight>100 and elementwidth>100):
            shapestyle.setDisplay("grid")
            shapestyle.setGridTemplateColumns("repeat(64,1fr)")
            shapestyle.setGridTemplateRows("repeat(64,1fr)")

        mshapeelement = ShapeElement(data["id"],tag,data["name"],data["type"],shapestyle)
        melement = mshapeelement
                  
    # handles TextElement
    elif(data["type"]=="TEXT"):
        fontsize = str((data["style"]["fontSize"]) / (pageWidth / 100)) + "vw"
        #print(data["characters"])
        #print(firstlevelelem["type"])
        if(firstlevelelem["type"]=="COMPONENT" or firstlevelelem["type"]=="COMPONENT_SET"): 
            fontsize = str(data["style"]["fontSize"]/1.1) + "px"
            #pageWidth = firstlevelelem["absoluteRenderBounds"]["width"] * 4
        lineheight = (round(data["style"]["lineHeightPx"])) 
        color = data["fills"][0]["color"]
        rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
        autoresize = None
        if("textAutoResize" in data["style"]):
            autoresize = data["style"]["textAutoResize"]
        style = TextStyle(xielem,
                        yielem,
                        elementwidth,
                        elementheight,
                        data["style"]["textAlignHorizontal"],
                        str(lineheight)+"px",
                        autoresize,
                        data["style"]["fontStyle"],
                        data["style"]["fontWeight"],
                        fontsize,
                        data["style"]["fontFamily"],
                        "rgba("+','.join(str(val) for val in rgba)+")",
                        nr_columnstart,
                        nr_columnend,
                        nr_rowstart,
                        nr_rowend)
        if("visible" in data and data["visible"]==False): style.setDisplay("none")
        if("opacity" in data): style.setOpacity(str(data["opacity"]*100)+"%")
        mtextelement = TextElement(data["id"],tag,data["name"],data["characters"],style)
        melement = mtextelement
    
    elif(data["type"]=="INSTANCE"):
        isComponentInstance = True
        scrollBehaviour = None
        if(data["scrollBehavior"]=="FIXED"): scrollBehaviour = "sticky"
        componentelement = Mcomponent(data["id"],data["name"],tag,"")
        componentStyle = setComponentStyle(data)
        componentStyle.setGridcolumnStart(nr_columnstart)
        componentStyle.setGridcolumnEnd(nr_columnend)
        componentStyle.setGridrowStart(nr_rowstart)
        componentStyle.setGridrowEnd(nr_rowend)
        componentStyle.setPosition(scrollBehaviour)
        componentStyle.setinstanceFromComponentId(data["componentId"])
        if(isComponentVariant(data,variants)):
            componentelement.setisVariant(True)
            componentelement.setVariantName(getFormatedName(data["name"]))
        componentelement.setisComponentInstance(isComponentInstance)
        resolveNameConflit(componentelement,componentStyle,pagename)
        assignComponentData(componentelement)
        assignComponentProps(componentelement)
        componentelement.setComponentStyle(componentStyle)            
        pageComponents.setdefault(pagename, []).append(componentelement)
        melement = componentelement

    # handles ContainerElement
    elif(data["type"]=="FRAME" or data["type"]=="GROUP"):

        gradient = None
        rgba = None
        for background in data["background"]:

            if("color" in background):
                color = data["background"][0]["color"]
                rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
            elif(background["type"] == "GRADIENT_LINEAR"):
                gradient = calculate_lineargradientDegree(background["gradientHandlePositions"],background["gradientStops"])
            elif(background["type"] == "GRADIENT_RADIAL"):
                gradient = calculate_radialgradientDegree(background["gradientHandlePositions"],background["gradientStops"])
            elif(background["type"]=="GRADIENT_ANGULAR"):
                gradient = calculate_angulargradientDegree(background["gradientHandlePositions"],background["gradientStops"])

            if("color" in background and "visible" in data["background"][0] and data["background"][0]["visible"]==False): rgba=None
            if((background["type"] == "GRADIENT_LINEAR" or background["type"] == "GRADIENT_RADIAL" or background["type"] == "GRADIENT_ANGULAR") and "visible" in background and background["visible"]==False): gradient=None
        style = ContainerStyle()
        
        if(rgba!=None): style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
        if(gradient!=None): style.setBackground(gradient)
        if("overflowDirection" in data and data["overflowDirection"]=="HORIZONTAL_SCROLLING"): style.setOverflowDirection("HORIZONTAL")
        if("overflowDirection" in data and data["overflowDirection"]=="VERTICAL_SCROLLING"): style.setOverflowDirection("VERTICAL")

        style.setX(xielem)
        style.setY(yielem)
        style.setHeight(elementheight)
        style.setWidth(elementwidth)
        style.setGridcolumnStart(nr_columnstart)
        style.setGridcolumnEnd(nr_columnend)
        style.setGridrowStart(nr_rowstart)
        style.setGridrowEnd(nr_rowend)

        if("overflowDirection" in data):
            style.setHeight(elementheight)
            style.setDisplay("flex")
            style.setMarginLeft("200px")
            scrollElements.setdefault(pagename,[]).append(data["id"])
            if(not pagename in allpages):
                addComponentVariable(pagename,{"isDragging":"false"})
                addComponentVariable(pagename,{"cursorPos":[0, 0]})
            else:
                allpages[pagename].addVariable({"isDragging":"false"})
                allpages[pagename].addVariable({"cursorPos":[0, 0]})
            
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
                spread = "0px "
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
    element_interactions = setLogic(melement,pagename,data,parent_data,firstlevelelem,xielem,yielem,elementwidth,elementheight,page_width,page_height,pageX,pageY,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,element_interactions)

    if(melement!=None):
        melement.addInteractionsList(element_interactions)
        if(firstlevelelem["type"]=="COMPONENT" or firstlevelelem["type"]=="INSTANCE"):
            melement.setupperIdComponent(firstlevelelem["id"])

    myparent_data = data
    # Iterates for all nested children of each element
    if("children" in data):
        if(data["type"]=="FRAME" or data["type"]=="GROUP"):
            if(style.getDisplay()==None): style.setDisplay("grid")
            style.setGridTemplateColumns("repeat(64,1fr)")
            style.setGridTemplateRows("repeat(64,1fr)")
        for element in data["children"]:
            nestedelem = processElement(pagename,element["name"],element,elementwidth,elementheight,pageX,pageY,firstlevelelem,myparent_data)
            children.append(nestedelem)

        if(melement!=None): melement.setChildren(children)

    if(data["type"]=="INSTANCE" and isComponentInstance==True): 
        for index,c in enumerate(pageComponents[pagename]):
            if(c.getIdComponent()==melement.getIdComponent()): pageComponents[pagename][index]=melement 
    if(data["type"]=="INSTANCE" and isComponentVariant(data,variants)):
        #update the default variant instances
        updateDefaultVariants(data,melement,data["componentId"],variants)
        if(pagename in allpages):
            for v in variants:
                for (index,c) in enumerate(v.variantComponents):
                    allpages[pagename].addVariable({f"componentclass{getElemId(c.getIdComponent())}":f'"grid-item-{getElemId(c.getIdComponent())} component{getElemId(c.getIdComponent())}"'})
            allpages[pagename].addVariable({f"selectedClass{getElemId(melement.getIdComponent())}":"''"})
            allpages[pagename].addVariable({f"currentVariant{getElemId(melement.getIdComponent())}":"''"})
        else:                  
            for v in variants:
                for (index,c) in enumerate(v.variantComponents):
                    addComponentVariable(pagename,{f"componentclass{getElemId(c.getIdComponent())}":f'"grid-item-{getElemId(c.getIdComponent())} component{getElemId(c.getIdComponent())}"'})
            addComponentVariable(pagename,{f"selectedClass{getElemId(melement.getIdComponent())}":"''"})
            addComponentVariable(pagename,{f"currentVariant{getElemId(melement.getIdComponent())}":"''"})

    return melement

# auxiliar function to calculate element positioning
def getPosition(xielem,yielem,elementwidth,elementheight,page_width,page_height, nrrows):

    if(page_height==0): page_height+=10
    if(page_width==0): page_width+=10
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

    gradient = None
    rgba = None
    for background in pagedata["background"]:

        if("color" in background):
            color = pagedata["background"][0]["color"]
            rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
        elif(background["type"] == "GRADIENT_LINEAR"):
            gradient = calculate_lineargradientDegree(background["gradientHandlePositions"],background["gradientStops"])
        elif(background["type"] == "GRADIENT_RADIAL"):
            gradient = calculate_radialgradientDegree(background["gradientHandlePositions"],background["gradientStops"])
        elif(background["type"]=="GRADIENT_ANGULAR"):
            gradient = calculate_angulargradientDegree(background["gradientHandlePositions"],background["gradientStops"])

    style = ContainerStyle()
    style.setWidth(pagedata["absoluteRenderBounds"]["width"])
    style.setHeight(pagedata["absoluteRenderBounds"]["height"])
    if(rgba!=None): style.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
    if(gradient!=None): style.setBackground(gradient)
    style.setDisplay("grid")
    style.setMargin("0")
    style.setPadding("0")
    style.setGridTemplateColumns("repeat(64,1fr)")
    
    allpages[pagename].assignPageStyle(style)

def setComponentStyle(component):
    global allcomponents
    gradient = None
    rgba = None
    if(len(component["background"])>0):
        for background in component["background"]:

            if("color" in background):
                color = component["background"][0]["color"]
                if("visible" in background and background["visible"]==False): color["a"] = 0
                rgba = (color["r"] * 255 , color["g"] * 255 , color["b"] * 255 , color["a"])
            elif(background["type"] == "GRADIENT_LINEAR"):
                gradient = calculate_lineargradientDegree(background["gradientHandlePositions"],background["gradientStops"])
            elif(background["type"] == "GRADIENT_RADIAL"):
                gradient = calculate_radialgradientDegree(background["gradientHandlePositions"],background["gradientStops"])
            elif(background["type"]=="GRADIENT_ANGULAR"):
                gradient = calculate_angulargradientDegree(background["gradientHandlePositions"],background["gradientStops"])
    else:
        rgba = (component["backgroundColor"]["r"] * 255 , component["backgroundColor"]["g"] * 255 , component["backgroundColor"]["b"] * 255 , component["backgroundColor"]["a"])
    id = component["id"]

    if(component["absoluteRenderBounds"]!=None):
        elementwidth = component["absoluteRenderBounds"]["width"]
        elementheight = component["absoluteRenderBounds"]["height"]
        xielem = component["absoluteRenderBounds"]["x"]
        yielem = component["absoluteRenderBounds"]["y"]
    elif(component["absoluteBoundingBox"]!=None):
        elementwidth = component["absoluteBoundingBox"]["width"]
        elementheight = component["absoluteBoundingBox"]["height"]
        xielem = component["absoluteBoundingBox"]["x"]
        yielem = component["absoluteBoundingBox"]["y"]

    componentStyle = ComponentStyle()
    componentStyle.setX(xielem)
    componentStyle.setY(yielem)
    componentStyle.setWidth(elementwidth)
    componentStyle.setHeight(elementheight)
    if(rgba!=None): componentStyle.setBackgroundColor("rgba("+','.join(str(val) for val in rgba)+")")
    if(gradient!=None): componentStyle.setBackground(gradient)
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
    componentStyle.setinstanceFromComponentId(component["id"])

    if(id in allcomponents): allcomponents[id].setComponentStyle(componentStyle)

    return componentStyle

def updateOverlayPosition(component, vx, vy, page_width, page_height):
    if isinstance(component, Mcomponent):

        nrrows = 128 
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

def extractImages(projectname,FIGMA_API_KEY,FILE_KEY):
    global allimages,batchi,batchf
    
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}

    resultingImages = []
    for mimage in allimages:
        imgpath = re.sub(r"[\s,@\.-]","",mimage["name"])
        destination = '../output/'+projectname+"/public/"+getFormatedName(imgpath)+getElemId(mimage["id"])+".png"

        if(not os.path.isfile(destination)):
            filteredImages = list(filter(lambda x: x["name"]==mimage["name"] and x["id"]==mimage["id"],allimages))
            resultingImages.extend(filteredImages)
    print("Resulting Images:"+str(len(resultingImages)))
    if(len(resultingImages)>0):
        for it in range(0,len(resultingImages),50):
            if(batchi<len(resultingImages)):
                l = resultingImages[batchi:batchf]
                myimageids = ','.join(x["id"] for x in l)
                url = f"https://api.figma.com/v1/images/"+FILE_KEY+"/?ids="+myimageids+"&format=png"

                response = requests.get(url, headers=headers)
                images = response.json()
                print(images)
                if("err" in images and images["err"]==None):
                    for mimage in l:
                        if(str(mimage["id"]) in images["images"] and images["images"][str(mimage["id"])]!=None):
                            imgurl = images["images"][str(mimage["id"])]
                            imgpath = re.sub(r"[\s,@\.-]","",mimage["name"])

                            destination = '../output/'+projectname+"/public/"+getFormatedName(imgpath)+getElemId(mimage["id"])+".png"
                            print("\nDownloading image "+destination+"...")
                            print(imgurl,destination)
                            if not os.path.exists(destination):
                                filename = wget.download(imgurl, out=destination)
                        else:
                            destination = '../output/'+projectname+"/public/"+getFormatedName(imgpath)+getElemId(mimage["id"])+".png"
                            wget.download("https://demofree.sirv.com/nope-not-here.jpg",out=destination)
                elif(images["status"]==403):
                    print("something went wrong...")
                
                batchi+=50
                batchf+=50
    batchi=0
    batchf=50

def extractSVGs(projectname,FIGMA_API_KEY,FILE_KEY):
    global allsvgs,batchi,batchf

    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", 'X-FIGMA-TOKEN': FIGMA_API_KEY}

    resultingSvgs = []
    for msvg in allsvgs:
        svgpath = re.sub(r"[\s,@\.-]","",msvg["name"])
        destination = '../output/'+projectname+"/public/"+getFormatedName(svgpath)+getElemId(msvg["id"])+".svg"
        if(not os.path.isfile(destination)):
            filteredSvgs = list(filter(lambda x: x["name"]==msvg["name"] and x["id"]==msvg["id"],allsvgs))
            resultingSvgs.extend(filteredSvgs)
    print("Resulting Svgs:"+str(len(resultingSvgs)))
    if(len(resultingSvgs)>0):
        for it in range(0,len(resultingSvgs),50):
            if(batchi<len(resultingSvgs)):
                l = resultingSvgs[batchi:batchf]
                mysvgsids = ','.join(x["id"] for x in l)
    
                url = f"https://api.figma.com/v1/images/"+FILE_KEY+"/?ids="+mysvgsids+"&format=svg"

                response = requests.get(url, headers=headers)
                svgs = response.json()
                print(svgs)
                if("err" in svgs and svgs["err"]==None):
                    for msvg in l:
                        if(str(msvg["id"]) in svgs["images"] and svgs["images"][str(msvg["id"])]!=None):
                            svgurl = svgs["images"][str(msvg["id"])]
                            svgpath = re.sub(r"[\s,@\.-]","",msvg["name"])
                            
                            destination = '../output/'+projectname+"/public/"+getFormatedName(svgpath)+getElemId(msvg["id"])+".svg"
                            print("\nDownloading image "+destination+"...")
                            print(svgurl,destination)
                            if not os.path.exists(destination):
                                filename = wget.download(svgurl, out=destination)                            
                        else:
                            destination = '../output/'+projectname+"/public/"+getFormatedName(svgpath)+getElemId(msvg["id"])+".svg"
                            wget.download("https://placehold.co/300x200.svg?text=PLACEHOLDER",out=destination)
                elif(svgs["status"]==403):
                    print("something went wrong...")
                    
                batchi+=50
                batchf+=50
    batchi=0
    batchf=50

def addComponentProps(componentName,props):
    global pageComponents, componentProps
    for idp in pageComponents:
        for compp in pageComponents[idp]:
            if(compp.getNameComponent()==componentName):
                compp.setProps(props)
    componentProps[componentName] = props
   
def addComponentVariable(componentName,var):
    global pageComponents, componentVariables
    for idp in pageComponents:
        for compp in pageComponents[idp]:
            if(compp.getNameComponent()==componentName):
                if(not var in compp.getData()): 
                    compp.addVariable(var)
    if(componentName in componentVariables and var not in componentVariables[componentName]):
        componentVariables[componentName].append(var)
    elif(componentName not in componentVariables):
        componentVariables[componentName]=[var]

def assignComponentProps(component):
    if(component.getNameComponent() in componentProps):
        component.setProps(componentProps[component.getNameComponent()])

def assignComponentData(component):
    if(component.getNameComponent() in componentVariables):
        for v in componentVariables[component.getNameComponent()]:
            component.addVariable(v)
            
def assignComponentDataById(id):
    global pageComponents
    for p in pageComponents:
        for c in pageComponents[p]:
            if(id==c.getIdComponent()):
                assignComponentData(c)

def manipulateComponentDom(elems,i):
    for el in elems:
        if(isinstance(el,Melement) and i[0]==el.idElement):
            el.addChildren(i[1])
        manipulateComponentDom(el.children,i)

def resolveNameConflit(componentelement,style,pagename):
    global pageComponents
    if(pagename in pageComponents):
        for c in pageComponents[pagename]:
            if(c.getNameComponent()==componentelement.getNameComponent() and 
                c.style.getinstanceFromComponentId()!=style.getinstanceFromComponentId()):
                componentelement.setNameComponent(componentelement.getNameComponent()+getElemId(componentelement.getIdComponent()))
    return componentelement

def setHoverProperties(overlayElem,melement,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend):
    overlaps=True
    if((overlayElem.style.getGridcolumnStart()<nr_columnstart and overlayElem.style.getGridcolumnEnd()<nr_columnstart)
       or 
       (overlayElem.style.getGridrowStart()<nr_rowstart and overlayElem.style.getGridrowEnd()<nr_rowstart)
       or
       (overlayElem.style.getGridcolumnStart()>nr_columnend and overlayElem.style.getGridcolumnEnd()>nr_columnend)
       or
       (overlayElem.style.getGridrowStart()>nr_rowend and overlayElem.style.getGridrowEnd()>nr_rowend)):
            overlaps=False
    if(overlaps==True):
        overlayElem.style.sethashoverProperty(True)
        melement.style.sethashoverProperty(True)
        overlayElem.style.setOpacity(1)
        overlayElem.setinitialOpacity(0)
        melement.style.setOpacity(0)
    return overlaps

def resetHoverProperties(el1,el2):
    el1.style.sethashoverProperty(False)
    el2.style.sethashoverProperty(False)
    el1.setinitialOpacity(1)
    el2.setinitialOpacity(1)
    el1.style.setOpacity(1)
    el2.style.setOpacity(1)

def insertVariantComponents(elements,variants):
    for variant in variants:
        for el in elements:
            if(isinstance(el,Melement) and el.getIdElement()==variant[0]):
                el.addChildren(variant[1])
            if(len(el.children)>0):
                insertVariantComponents(el.children,variants)
    
def getVariantElement(id,data):
    if(data["id"]==id):
        return data
    if("children" in data):
        for c in data["children"]:
            elem = getVariantElement(id, c)
            if(elem): return elem

def isComponentVariant(elem,variants):
    r = False
    if((elem["type"]=="COMPONENT_SET" or elem["type"]=="COMPONENT" or elem["type"]=="INSTANCE") and 
       ("componentPropertyDefinitions" in elem or "componentProperties" in elem)):
        return True
    if(elem["type"]=="INSTANCE" and r==True and len(variants)>0):
        if(not any(elem["componentId"]==c.getIdComponent() or elem["id"]==c.getIdComponent() for v in variants for c in v.variantComponents)):
            return False
    return r

def isAllImages(elem):
    allVectors = True
    for ch in elem["children"]:
        if(ch["type"]!="VECTOR" or ch["type"]!="IMAGE"): allVectors=False
    return allVectors

def hasCloseAction(interactions):
    hasclose = False
    for i in interactions:
        for a in i.actions:
            if(a.getActionType()=="CLOSE"):
                hasclose=True
                break
    return hasclose

def updateInnerChildren(elements,el):
    for element in elements:
        if(isinstance(element,ContainerElement) and element.getIdElement()==el):
            for innerchildren in element.children:
                innerchildren.style.setGridcolumnEnd(None)
                innerchildren.style.setGridcolumnStart(None)
                innerchildren.style.setGridrowStart(None)
                innerchildren.style.setGridrowEnd(None)
                innerchildren.style.setMinHeight(innerchildren.style.getHeight())
                innerchildren.style.setMinWidth(innerchildren.style.getWidth())
                innerchildren.style.setMargin("1em")
        if(len(element.children)>0): updateInnerChildren(element.children,el)
        
def setVariantProperties(component,properties):
    cproperties = {}
    for property in properties:
        val = properties[property]["variantOptions"]
        cproperties[property] = val
    component.setVariantProperties(cproperties)
    
def addVariant(variants,v):
    exists = False
    for (index,variant) in enumerate(variants):
        if variant.getIdComponent()==v.getIdComponent():
            exists = True
            variants[index] = v
    if(exists==False): variants.append(v)

def updateElement(c,elemid,interactions):
    if(isinstance(c,Melement) and elemid==c.getIdElement()): 
        c.addInteractionsList(interactions)
    if(isinstance(c,Mcomponent) and elemid==c.getIdComponent()):
        c.addInteractionsList(interactions)
    else:
        for ch in c.children:
            updateElement(ch,elemid,interactions)


def belongsToElem(elem,id):
    if(elem and elem["id"]==id):
        return True
    if("children" in elem):
        for ch in elem["children"]:
            r = belongsToElem(ch,id)
            if r:
                return True
    return False
     
def getClosePaths(closeIds,event_EmissionPaths):
    closePaths = {}
    for pair in closeIds:
        for ee in event_EmissionPaths:
            if(pair[1]==ee[1]): 
                if((pair[0],pair[1],getElemId(ee[0])) in closePaths and len(event_EmissionPaths[ee])>0 or
                   not (pair[0],pair[1],getElemId(ee[0])) in closePaths and len(event_EmissionPaths[ee])>=0): 
                    l = list(filter(lambda x: "#Page" in x[0] or x[2]=="INSTANCE",event_EmissionPaths[ee]))
                    l.append(pair)
                    l.reverse()
                    closePaths[(pair[0],pair[1],getElemId(ee[0]))] = l
    return closePaths
                
def getCompTopPath(elem,ids,path=None):
    if path is None:
        path = []

    current_path = path + [(elem.get("name"),getElemId(elem.get("id")),elem.get("type"), getElemId(elem.get("componentId", "_")))]
    
    if "children" in elem and "componentId" in elem and len(elem["children"]) == 0 and getElemId(elem.get("componentId")) not in ids:
        return False, []
    else:
        if("children" in elem):
            for el in elem["children"]:
                if("componentId" in el and getElemId(el["componentId"]) in ids):
                    return True, current_path + [(el.get("name"),getElemId(el.get("id")),el.get("type"), getElemId(el.get("componentId")))]
                else:
                    r, res_path = getCompTopPath(el, ids, current_path)
                    if r:
                        return True, res_path
        return False, []
         
def getElemTopPath(elem,ids,path=None):
    if path is None:
        path = []

    current_path = path + [(elem.get("name"),getElemId(elem.get("id")),elem.get("type"), getElemId(elem.get("id")))]
    
    if "children" in elem and len(elem["children"]) == 0 and getElemId(elem.get("id")) not in ids:
        return False, []
    else:
        if("children" in elem):
            for el in elem["children"]:
                if(getElemId(el["id"]) in ids):
                    return True, current_path + [(el.get("name"),getElemId(el.get("id")),el.get("type"), getElemId(el.get("id")))]
                else:
                    r, res_path = getElemTopPath(el, ids, current_path)
                    if r:
                        return True, res_path
        return False, []

def getTopLayer_pagename(elem,data,parentelem,overlayId):
    global figmadata, event_EmissionPaths
    childids = []
    iscomponent = False
    if(elem["type"]=="COMPONENT" or elem["type"]=="COMPONENT_SET"):
        iscomponent = True
        for ch in elem["children"]:
            childids.append(getElemId(ch["id"]))
    else: childids = [getElemId(elem["id"])]
    for el in figmadata["document"]["children"][0]["children"]:
        if("#Page" in el["name"]):
            name = el["name"]
            r, path = False, {}
            if(iscomponent==True): r, path =getCompTopPath(el, childids)
            else: r, path =getElemTopPath(el, childids)
            #print("Matched Path:", " -> ", path)
            if(elem["type"]!="COMPOENNT" and elem["type"]!="COMPONENT_SET"):
                event_EmissionPaths[(data["id"],overlayId)] = path
            elif(parentelem!=None):
                elid = parentelem["id"]
                if(parentelem["type"]=="COMPONENT" and "children" in parentelem): elid = parentelem["children"][0]["id"]
                event_EmissionPaths[(elid,overlayId)] = path
            else:
                elid = data["id"]
                if(data["type"]=="COMPONENT" and "children" in data): elid = data["children"][0]["id"]
                event_EmissionPaths[(elid,overlayId)] = path
            if(r==True):
                return name

def getToppage(elem,id):
    if("transitionNodeID" in elem and elem["transitionNodeID"]==id):
        return True
    if("children" in elem):
        for ch in elem["children"]:
            r = getToppage(ch,id)
            if r:
                return True
    return False
     
def getPageoftrigger(id):
    global figmadata
    for el in figmadata["document"]["children"][0]["children"]:
        if("#Page" in el["name"]):
            r = getToppage(el,id)
            if(r==True):
                return el["name"]
            
def updateDefaultVariants(data,melement,componentId,variants):
    global figmadata
    found = False
    for v in variants:
        for (index,c) in enumerate(v.variantComponents):
            if(componentId==c.getIdComponent()):
                found = True
                melement.setNameComponent(c.getNameComponent())
                v.variantComponents[index] = melement
                v.setDefaultComponent(getFormatedName(melement.getNameComponent()))
    if(found==False):
        id = data["componentId"]
        componentsetid=""
        for cid in figmadata["components"]:
            if(cid==id):
                componentsetid = figmadata["components"][cid]["componentSetId"]
        chcomponents = []
        componentsinvolved = []
        for element in figmadata["document"]["children"][0]["children"]:
            if(element["id"]==componentsetid):
                for ch in element["children"]:
                    chcomponents.append(ch)
        for (idx,chcomp) in enumerate(chcomponents):
            if(data["componentId"]==chcomp["id"]):
               chcomponents[idx]=data
        
        v = VariantComponent(data["id"],"",data["name"],"",[])
        for ch in chcomponents:                    
            name = ch["name"]
            if(ch["type"]=="INSTANCE"): name = figmadata["components"][ch["componentId"]]["name"]
            c = Mcomponent(ch["id"],name,"","",[])
            style = setComponentStyle(ch)
            c.setComponentStyle(style)
            componentsinvolved.append(c)
        name = v.getNameComponent()
        for c in componentsinvolved:
            if(data["id"]==c.getIdComponent()):
                name = c.getNameComponent()
        v.setVariantComponents(componentsinvolved)    
        melement.setNameComponent(name)
        v.setDefaultComponent(getFormatedName(name))
        addVariant(variants,v)
        

def updateComponentPage(pagename,comp,allpages):
    if pagename in allpages:
        for (idx,c) in enumerate(allpages[pagename].components):
            if(c.getIdComponent()==comp.getIdComponent()):
                allpages[pagename].components[idx] = comp

def setLogic(melement,pagename,data,parent_data,firstlevelelem,xielem,yielem,elementwidth,elementheight,page_width,page_height,pageX,pageY,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,element_interactions):
    global allpages, allcomponents,pageComponents, logicDependentComponents, refs, overlayInsideInstances, pageOverlays, overlayTriggers, variants, scrollElements, allimages, allsvgs, event_EmissionPaths, closeIds
    for interaction in data["interactions"]:
        type = interaction["trigger"]["type"]
        interactionelement = InteractionElement()
        if(type == "ON_CLICK"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONCLICK)
        if(type == "ON_HOVER"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONHOVER)
        if(type == "DRAG"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONDRAG)
        if(type == "MOUSE_DOWN"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONMOUSEDOWN)
            interactionelement.setTimeout(interaction["trigger"]["delay"])
        if(type == "MOUSE_UP"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONMOUSEUP)
            interactionelement.setTimeout(interaction["trigger"]["delay"])
        if(type == "MOUSE_ENTER"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONMOUSEENTER)
            interactionelement.setTimeout(interaction["trigger"]["delay"])
        if(type == "MOUSE_LEAVE"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONMOUSELEAVE)
            interactionelement.setTimeout(interaction["trigger"]["delay"])
        if(type == "ON_KEY_DOWN"):
            interactionelement.setInteractionType(InteractionElement.Interaction.ONKEYDOWN)
            interactionelement.setKeyCodes(interaction["trigger"]["keyCodes"])
        if(type == "AFTER_TIMEOUT"):
            interactionelement.setInteractionType(InteractionElement.Interaction.AFTERTIMEOUT)
            interactionelement.setTimeout(interaction["trigger"]["timeout"])
  
        for action in interaction["actions"]:
            transition = None
            if(action != None and "transition" in action and action["transition"]!=None and "direction" in action["transition"] and "duration" in action["transition"]):
                transition = Transition(action["transition"]["type"],action["transition"]["direction"],action["transition"]["easing"]["type"],action["transition"]["duration"])
                if(not pagename in allpages): addComponentVariable(pagename,{"animationName":'""'})
                else: allpages[pagename].addVariable({"animationName":'""'})
                melement.sethasAnimation(True)
                transition_nodeIds.append(action["destinationId"])
            if(action!=None and action["type"]=="URL"):
                openlinkaction = OpenLinkAction(action["url"],action["openInNewTab"],transition)
                interactionelement.addAction(openlinkaction)
            if(action!=None and action["type"]=="BACK"):
                backaction = BackAction(transition)
                interactionelement.addAction(backaction)
            if(action!=None and action["type"]=="NODE" and action["navigation"]=="NAVIGATE"):
                navigateAction = NavigationAction(action["destinationId"],transition)
                interactionelement.addAction(navigateAction)
            if(action!=None and action["type"]=="NODE" and (action["navigation"]=="OVERLAY" or action["navigation"]=="SWAP")):
                offsetx = 0
                offsety = 0
                if("overlayRelativePosition" in action):
                    offsetx = action["overlayRelativePosition"]["x"]
                    offsety = action["overlayRelativePosition"]["y"]
                #verificar se o elemento overlay se encontra no notPageElems
                if(action["destinationId"] in notPageElems):
                    notPageElems[action["destinationId"]]["absoluteRenderBounds"]["x"] = data["absoluteRenderBounds"]["x"]+offsetx
                    notPageElems[action["destinationId"]]["absoluteRenderBounds"]["y"] = data["absoluteRenderBounds"]["y"]+offsety
                    isonPageLevel = False
                    overlayElem = None
                    # construir o elemento overlay tendo em conta que o elemento atual será o seu parent
                    if(data["id"] not in overlayTriggers):
                        overlayTriggers.append(data["id"]) # evitar recursividade infinita
                        if(parent_data!=None):
                            overlayElem = processElement(parent_data["name"],notPageElems[action["destinationId"]]["name"],notPageElems[action["destinationId"]],parent_data["absoluteRenderBounds"]["width"],parent_data["absoluteRenderBounds"]["height"],parent_data["absoluteRenderBounds"]["x"],parent_data["absoluteRenderBounds"]["y"],firstlevelelem,parent_data)
                            if(not firstlevelelem["name"] in allpages):
                                addComponentVariable(firstlevelelem["name"],{"show"+getElemId(overlayElem.getIdElement()):"false"})
                            else:
                                allpages[firstlevelelem["name"]].addVariable({"show"+getElemId(overlayElem.getIdElement()):"false"})   
                        else:
                            overlayElem = processElement(pagename,notPageElems[action["destinationId"]]["name"],notPageElems[action["destinationId"]],page_width,page_height,pageX,pageY,firstlevelelem,parent_data)                        
                            isonPageLevel = True
                            if(not pagename in allpages):
                                addComponentVariable(pagename,{"show"+getElemId(overlayElem.getIdElement()):"false"})
                            else:
                                allpages[pagename].addVariable({"show"+getElemId(overlayElem.getIdElement()):"false"})
                    if(type=="ON_HOVER" and overlayElem!=None or (type=="ON_CLICK" and overlayElem!=None and action["navigation"]!="SWAP")): #or type=="ON_CLICK"
                        # caso exista overlaping sao adicionadas as propriedades de hovering
                        overlaps = setHoverProperties(overlayElem,melement,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
                        if(not overlaps):
                            overlayElem.sethascondvisib(True)
                            overlayAction = OverlayAction(action["destinationId"],transition)
                            interactionelement.addAction(overlayAction)
                            resetHoverProperties(melement,overlayElem)
                    if(type=="ON_CLICK" and overlayElem!=None and action["navigation"]=="SWAP"): 
                        swapaction = SwapAction(action["destinationId"],transition)
                        interactionelement.addAction(swapaction)
                        elid = getElemId(data["id"])
                        visibility = "true"
                        if(data["id"] in notPageElems): visibility = "false"
                        melement.settopmostnode(pagename)
                        if(not pagename in allpages):
                            addComponentVariable(pagename,{"showswaped"+elid:visibility})
                        else:
                            allpages[pagename].addVariable({"showswaped"+elid:visibility})
                    if(overlayElem!=None):
                        if(isonPageLevel==True): pageOverlays.setdefault(pagename, []).append((None,overlayElem))
                        elif(isonPageLevel==False and parent_data!=None): pageOverlays.setdefault(pagename, []).append((parent_data["id"],overlayElem))
                        if(firstlevelelem["type"]=="INSTANCE" and parent_data!=None):
                            overlayInsideInstances.setdefault(firstlevelelem["id"], []).append((parent_data["id"],overlayElem)) # só fazer isto se a posicao do overlay estiver contida numa instance/component
                    if(action["navigation"]=="OVERLAY" and overlayElem!=None): overlayElem.settypeElement("OVERLAY")
                #verificar se o elemento overlay é uma instancia(componente)
                elif(action["destinationId"] in allcomponents): 
                    compstyle = allcomponents[data["transitionNodeID"]].getComponentStyle()
                    (xe,ye) = (xielem,yielem)
                    (rx,ry) = (int(offsetx),int(offsety))
                    (px,py) = (rx+xe,ry+ye)
                    (vx,vy) = (px-compstyle.getX(),py-compstyle.getY())
                    compstyle.setOverlayVector(vx,vy)
                    if(action["navigation"]=="SWAP"): 
                        melement.settopmostnode(pagename)
                        style = allcomponents[firstlevelelem["id"]].getComponentStyle()
                        compstyle.setGridcolumnStart(style.getGridcolumnStart())
                        compstyle.setGridcolumnEnd(style.getGridcolumnEnd())
                        compstyle.setGridrowStart(style.getGridrowStart())
                        compstyle.setGridrowEnd(style.getGridrowEnd())
                    compstyle.setinstanceFromComponentId(data["transitionNodeID"])
                    if(firstlevelelem!=None and "isFixed" in firstlevelelem and firstlevelelem["isFixed"]==True):
                        allcomponents[data["transitionNodeID"]].setzindex(6)
                    else:
                        allcomponents[data["transitionNodeID"]].setzindex(2)
                    topname = ""
                    if(firstlevelelem!=None): topname = getTopLayer_pagename(firstlevelelem,data,parent_data,data["transitionNodeID"])
                    if(topname!="" and topname!=None): 
                        pagename=topname
                    if(type=="ON_CLICK" and action["navigation"]=="SWAP"): 
                        pagename = getPageoftrigger(firstlevelelem["id"])
                        closeaction=False
                        if(data["transitionNodeID"] in allcomponents): closeaction = hasCloseAction(allcomponents[data["transitionNodeID"]].interactions)
                        if(closeaction==True): allpages[pagename].addVariable({"show"+getElemId(data["transitionNodeID"]):"false"})

                    allcomponents[data["transitionNodeID"]].setComponentStyle(compstyle)
                    allcomponents[data["transitionNodeID"]].setTypeComponent("OVERLAY")
                    pageComponents.setdefault(pagename, []).append(allcomponents[data["transitionNodeID"]])
                    if(pagename in allpages): allpages[pagename].addElement(allcomponents[data["transitionNodeID"]])

                    if(type=="ON_CLICK" and action["navigation"]=="SWAP"):
                        swapaction = SwapAction(action["destinationId"],transition)
                        interactionelement.addAction(swapaction)
                        allpages[pagename].addVariable({"showswaped"+getElemId(firstlevelelem["id"]):"true"})
                        allpages[pagename].addVariable({"showswaped"+getElemId(data["transitionNodeID"]):"false"})   
                    else:
                        #adicionar variavel na pagina visto que o componente não estará visivel no imediato
                        idcomponent = getElemId(action["destinationId"])
                        if(not pagename in allpages):
                            addComponentVariable(pagename,{"show"+idcomponent:"false"})
                        else:
                            allpages[pagename].addVariable({"show"+idcomponent:"false"})

                        overlayAction = OverlayAction(action["destinationId"],transition)
                        interactionelement.addAction(overlayAction)
                if(action["destinationId"] not in notPageElems and action["destinationId"] not in allcomponents):
                    logicDependentComponents[firstlevelelem["id"]] = {"melement":melement,"pagename":pagename,"data":data,"parent_data":parent_data,"firstlevelelem":firstlevelelem,"xielem":xielem,"yielem":yielem,"elementwidth":elementwidth,"elementheight":elementheight,"page_width":page_width,"page_height":page_height,"pageX":pageX,"pageY":pageY,"nr_columnstart":nr_columnstart,"nr_columnend":nr_columnend,"nr_rowstart":nr_rowstart,"nr_rowend":nr_rowend}
            if(action!=None and action["type"]=="NODE" and action["navigation"]=="CHANGE_TO"):
                changeAction = ChangeAction(action["destinationId"],transition)
                interactionelement.addAction(changeAction)
            if(action!=None and action["type"]=="NODE" and action["navigation"]=="SCROLL_TO"):
                refs.setdefault(pagename, []).append(getElemId(action["destinationId"]))
                scrollAction = ScrollAction(action["destinationId"],transition)
                interactionelement.addAction(scrollAction)
            if(action!=None and action["type"]=="CLOSE"):
                closeAction = CloseAction(firstlevelelem["id"],transition)
                interactionelement.addAction(closeAction)
                closeIds.append((data["id"],firstlevelelem["id"],firstlevelelem["type"],firstlevelelem["id"]))

        element_interactions.append(interactionelement)
    return element_interactions
    