from parser.model.Dropdown import Dropdown
from parser.model.DropdownStyle import DropdownStyle
from parser.model.InputSearch import InputSearch
from parser.model.InputSearchStyle import InputSearchStyle
from parser.model.DatePicker import DatePicker
from parser.model.DatePickerStyle import DatePickerStyle
from parser.model.Rating import Rating
from parser.model.RatingStyle import RatingStyle
from parser.model.Paginator import Paginator
from parser.model.PaginatorStyle import PaginatorStyle
from parser.model.Slider import Slider
from parser.model.SliderStyle import SliderStyle
from parser.model.Form import Form
from parser.model.Menu import Menu
from parser.model.MenuStyle import MenuStyle
from parser.model.Table import Table
from parser.model.TableStyle import TableStyle
from parser.model.FormStyle import FormStyle
from parser.model.Checkbox import Checkbox
from parser.model.CheckboxStyle import CheckboxStyle
from utils.tools import getFormatedName,getElemId

def convertToDropdown(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    placeholder = ""
    selectedcolor = ""
    nonselectedcolor = ""
    borderRadius = 0
    txtcolor = ""
    for c in data["children"]:
        if(c["name"]=="State=Closed"):
            for h in c["children"]:
                if(h["name"]=="Header"):
                    borderRadius = h["cornerRadius"]
                    for m in h["children"]:
                        if(m["name"]=="Menu Label"):
                            placeholder = m["children"][0]["characters"]
                            color = m["children"][0]["fills"][0]["color"]
                            txtcolor = (str(color["r"] * 255) , str(color["g"] * 255) , str(color["b"] * 255) , str(color["a"]))
        if(c["name"]=="State=Opened"):
            for i in c["children"]:
                if(i["name"]=="Items Frame"):
                    options = len(i["children"][0]["children"])
                    alloptions = []
                    nr=0
                    for p in i["children"][0]["children"]:
                        nr+=1
                        option = p["children"][nr]["children"][0]
                        alloptions.append({"label":option["characters"],"value":option["name"]})
        if(c["name"]=="State=Opened-L1"):
            for i in c["children"]:
                if(i["name"]=="Items Frame"):
                    for l in i["children"]:
                        if(l["name"]=="Items List"):
                            selected = l["children"][0]
                            nonselected = l["children"][1]
                            selectedcolor = (str(selected["backgroundColor"]["r"] * 255) , str(selected["backgroundColor"]["g"] * 255) , str(selected["backgroundColor"]["b"] * 255) , str(selected["backgroundColor"]["a"]))
                            nonselectedcolor = (str(nonselected["backgroundColor"]["r"] * 255) , str(nonselected["backgroundColor"]["g"] * 255) , str(nonselected["backgroundColor"]["b"] * 255) , str(nonselected["backgroundColor"]["a"]))
                            break

    style = DropdownStyle(
        "rgba("+selectedcolor[0]+","+selectedcolor[1]+","+selectedcolor[2]+","+selectedcolor[3]+")",
        "rgba("+selectedcolor[0]+","+selectedcolor[1]+","+selectedcolor[2]+","+selectedcolor[3]+")",
        "rgba("+nonselectedcolor[0]+","+nonselectedcolor[1]+","+nonselectedcolor[2]+","+nonselectedcolor[3]+")",
        "rgba("+txtcolor[0]+","+txtcolor[1]+","+txtcolor[2]+","+txtcolor[3]+")",
        "rgba("+nonselectedcolor[0]+","+nonselectedcolor[1]+","+nonselectedcolor[2]+","+nonselectedcolor[3]+")",
        "rgba("+selectedcolor[0]+","+selectedcolor[1]+","+selectedcolor[2]+","+selectedcolor[3]+")",
        "rgba("+txtcolor[0]+","+txtcolor[1]+","+txtcolor[2]+","+txtcolor[3]+")",
        borderRadius,
        nr_columnstart,
        nr_columnend,
        nr_rowstart,
        nr_rowend
    )
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    elemid = getElemId(id)
    melement = Dropdown(id,"",name,"COMPONENT_ASSET","selectedOption"+elemid,alloptions,placeholder,False,style)

    return melement

def convertToSearchInput(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    placeholder = ""
    elemid = getElemId(id)
    vmodel = "inputsearch"+str(elemid)
    backgroundcolor = str(data["backgroundColor"]["r"] * 255)+","+str(data["backgroundColor"]["g"] * 255)+","+str(data["backgroundColor"]["b"] * 255)+","+str(data["backgroundColor"]["a"])
    radius = str(data["cornerRadius"])
    for e in data["children"]:
        if(e["type"]=="TEXT"):
            placeholder = e["characters"]
            color = e["fills"][0]["color"]
            txtcolor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
    style = InputSearchStyle(backgroundcolor,color,radius,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    inputsearchfilter =  InputSearch(id,"",name,"COMPONENT_ASSET",vmodel,placeholder,style)

    return inputsearchfilter

def convertToDatePicker(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    elemid = getElemId(id)
    vmodel = "datepicker"+str(elemid)
    dateinput = None
    dropdowninput = None
    dropdownbackgroundcolor = None
    for d in data["children"]:
        if(d["name"]=="DateInput"):
            dateinput = d
            if(len(dateinput["children"])>0):
                dropdowninput = dateinput["children"][0]
                dropdownbackgroundcolor = "rgba("+str(dropdowninput["backgroundColor"]["r"] * 255)+","+str(dropdowninput["backgroundColor"]["g"] * 255)+","+str(dropdowninput["backgroundColor"]["b"] * 255)+","+str(dropdowninput["backgroundColor"]["a"])+")"
                icon = dropdowninput["children"][0]["children"][0]
                iconcolor = icon["fills"][0]["color"]
                iconrgbacolor =  "rgba("+str(iconcolor["r"] * 255)+","+str(iconcolor["g"] * 255)+","+str(iconcolor["b"] * 255)+","+str(iconcolor["a"])+")"
    backgroundcolor = "rgba("+str(dateinput["backgroundColor"]["r"] * 255)+","+str(dateinput["backgroundColor"]["g"] * 255)+","+str(dateinput["backgroundColor"]["b"] * 255)+","+str(dateinput["backgroundColor"]["a"])+")"
    
    style = DatePickerStyle(backgroundcolor,dropdownbackgroundcolor,iconrgbacolor,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    datepicker =  DatePicker(id,"",name,"COMPONENT_ASSET",vmodel,style)

    return datepicker

def convertToSlider(data,percentage,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    elemid = getElemId(id)
    vmodel = "slider"+str(elemid)
    backgroundtrack =""
    backgroundrange =""
    backgroundcontent =""
    backgroundhover =""
    for s in data["children"]:
        if(s["name"]=="Percent=0, State=Default"):
            for ns in s["children"]:
                if(ns["name"]=="Slider"):
                    backgroundtrack = "rgba("+str(ns["backgroundColor"]["r"] * 255)+","+str(ns["backgroundColor"]["g"] * 255)+","+str(ns["backgroundColor"]["b"] * 255)+","+str(ns["backgroundColor"]["a"])+")"
        if(s["name"]=="Percent=100, State=Active"):
            for ns in s["children"]:
                if(ns["name"]=="Slider"):
                    backgroundrange = "rgba("+str(ns["backgroundColor"]["r"] * 255)+","+str(ns["backgroundColor"]["g"] * 255)+","+str(ns["backgroundColor"]["b"] * 255)+","+str(ns["backgroundColor"]["a"])+")"
                    backgroundcontentcolor = ns["children"][0]["children"][0]["children"][0]["fills"][0]["color"]
                    backgroundcontent = "rgba("+str(backgroundcontentcolor["r"] * 255)+","+str(backgroundcontentcolor["g"] * 255)+","+str(backgroundcontentcolor["b"] * 255)+","+str(backgroundcontentcolor["a"])+")"
                    backgroundhover = backgroundcontent  

    style = SliderStyle(backgroundtrack,backgroundcontent,backgroundrange,backgroundhover,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    slider =  Slider(id,"",name,"COMPONENT_ASSET",vmodel,percentage,style)
    return slider

def convertToRating(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name,readOnly):
    elemid = getElemId(id)
    vmodel = "starsSeletec"+str(elemid)
    nrstars = len(data["children"])
    colorStar = ""
    unselectedStarColor = ""
    selected = 0
    if(readOnly==True):
        for i in range(0,len(data["children"])):        
            star = data["children"][i]
            if(len(star["fills"])>0):
                color = star["fills"][0]["color"]
                colorStar = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
                selected = i + 1
            if(i<len(data["children"])-2):
                star = data["children"][i+1]
                if(len(star["fills"])>0): 
                    color = star["fills"][0]["color"]
                    unselectedStarColor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
                    if(colorStar!=unselectedStarColor): break
    else:
        selected = 0
        if("componentProperties" in data and "Rating" in data["componentProperties"]):
            selected = int(data["componentProperties"]["Rating"]["value"])
        for i in range(0,len(data["children"])):        
            star = data["children"][i]["children"][0]["children"][0]
            if(selected>0 and len(star["fills"])>0):
                color = star["fills"][0]["color"]
                colorStar = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
                break
        for i in range(0,len(data["children"])): 
            if(len(data["children"])>selected):       
                star = data["children"][selected]["children"][0]["children"][0]
                if(len(star["fills"])>0): 
                    unselectedcolor = star["fills"][0]["color"]
                    unselectedStarColor = "rgba("+str(unselectedcolor["r"] * 255)+","+str(unselectedcolor["g"] * 255)+","+str(unselectedcolor["b"] * 255)+","+str(unselectedcolor["a"])+")"
                    if(colorStar!=unselectedStarColor): break
    style = RatingStyle(colorStar,unselectedStarColor,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    rating =  Rating(id,"",name,"COMPONENT_ASSET",nrstars,readOnly,vmodel,selected,style)
    return rating

def convertToPaginator(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    elemid = getElemId(id)
    vmodel = "currentPage"+str(elemid)
    paginationList = None
    backgroundcolor = None
    cornerRadius = None
    length = 0
    visible = 0
    for l in data["children"][0]["children"]:
        if(l["name"]=="Pagination List"):
            for p in l["children"]:
                if(p["name"]!="Pagination Gap"):
                    visible+=1
                else:
                    break

            selectedColor = l["children"][0]["children"][0]["fills"][0]["color"]
            txtselectedColor = "rgba("+str(selectedColor["r"] * 255)+","+str(selectedColor["g"] * 255)+","+str(selectedColor["b"] * 255)+","+str(selectedColor["a"])+")"
            selectedbackgroundColor = l["children"][0]["background"][0]["color"]
            cornerRadius = l["children"][0]["cornerRadius"]
            backgroundcolor = "rgba("+str(selectedbackgroundColor["r"] * 255)+","+str(selectedbackgroundColor["g"] * 255)+","+str(selectedbackgroundColor["b"] * 255)+","+str(selectedbackgroundColor["a"])+")"
            l["children"].reverse()
            length = l["children"][0]["children"][0]['characters']

    style = PaginatorStyle(cornerRadius,txtselectedColor,txtselectedColor,backgroundcolor,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    rating =  Paginator(id,"",name,"COMPONENT_ASSET",vmodel,visible,length,style)
    return rating
    
def convertToForm(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    inputs = []
    buttontxt = None
    inputbackgroundcolor=""
    btnbackgroundcolor=""
    widthInput = ""
    labelColorText = None
    labelSizeText = None
    formname=data["name"]
    placeholder = ""
    label={"for":"","text":""}
    data["children"].reverse()
    for i in data["children"]:
        if(i["name"]!="submitbtn"):
            for j in i["children"]:
                name = ""
                if("label" not in j["name"]):
                    name = j["name"]
                    placeholder = j["children"][0]["characters"]
                    placeholderColor = j["children"][0]["fills"][0]["color"]
                    placeholderTextColor = "rgba("+str(placeholderColor["r"] * 255)+","+str(placeholderColor["g"] * 255)+","+str(placeholderColor["b"] * 255)+","+str(placeholderColor["a"])+")"
                    color = j["background"][0]["color"]
                    inputbackgroundcolor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
                    widthInput = j["absoluteBoundingBox"]["width"] / 1.3
                else:
                    name = j["name"]
                    text = j["characters"]
                    labelColor = j["fills"][0]["color"]
                    labelColorText = "rgba("+str(labelColor["r"] * 255)+","+str(labelColor["g"] * 255)+","+str(labelColor["b"] * 255)+","+str(labelColor["a"])+")"
                    labelSizeText = j["style"]["fontSize"]
                    label = {"for":name,"text":text}      
                    
            inputs.append({"name":getFormatedName(name),"placeholder":placeholder,"label":label})
        else:
            buttontxt = i["children"][0]["characters"]
            color = i["background"][0]["color"]
            btnbackgroundcolor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"

    style = FormStyle(inputbackgroundcolor,btnbackgroundcolor,widthInput,labelSizeText,labelColorText,placeholderTextColor,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    form =  Form(id,"",formname,"COMPONENT_ASSET",inputs,buttontxt,style)
    return form

def convertToCheckbox(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    data["children"].reverse()
    boxes = []
    textColor = ""
    boxRadius = "0"
    for option in data["children"]:
        for b in option["children"]:
            if(b["type"]=="TEXT"):
                boxes.append({"name":b["characters"],"key":getFormatedName(data["name"])})
                colortxt = b["fills"][0]["color"]
                textColor = "rgba("+str(colortxt["r"] * 255)+","+str(colortxt["g"] * 255)+","+str(colortxt["b"] * 255)+","+str(colortxt["a"])+")"
            elif(b["type"]=="FRAME"):
                color = b["fills"][0]["color"]
                boxRadius = b["cornerRadius"]
                boxBackground = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"

    style = CheckboxStyle(textColor,boxBackground,boxRadius, nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    checkbox =  Checkbox(id,"",name,"COMPONENT_ASSET",boxes,style)
    return checkbox

def convertToMenu(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    options = []
    iconImage = None
    menuName = name
    for c in data["children"]:
        if(c["name"]=="iconMenu"):
            name = c["name"]
            if("#" in c["name"]): name = c["name"].split("#")[0]
            iconImage = {"id":c["id"],"name":name}
        if(c["name"]=="optionsMenu"):
            for op in c["children"]:
                option = {"option":op["children"][0]["characters"]}
                for i in op["interactions"]:
                    if(i["trigger"]["type"]=="ON_CLICK" and i["actions"][0]["navigation"]=="NAVIGATE"):
                        option["destination"]=i["actions"][0]["destinationId"]
                options.append(option)
    style = MenuStyle(nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    menu = Menu(id,"",menuName,"COMPONENT_ASSET",options,iconImage,style)
    return menu

def convertToTable(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    values = []
    header = {}
    headerColor = ""
    bodyColor = ""
    headertextColor = ""
    nrrows = 0
    images = []
    for c in data["children"]:
        if("th" in c["name"]):
            for t in c["children"]:
                color = t["fills"][0]["color"]
                headerColor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
                col = "col"+t["name"].split("th")[1]
                header[col] = {"name":t["children"][0]["characters"]}
                txtcolor = t["children"][0]["fills"][0]["color"]
                headertextColor = "rgba("+str(txtcolor["r"] * 255)+","+str(txtcolor["g"] * 255)+","+str(txtcolor["b"] * 255)+","+str(txtcolor["a"])+")"
    for c in data["children"]:
        if("row" in c["name"]):
            nrrows+=1
            value={}
            for col in c["children"]:
                if(col["children"][0]["type"]=="TEXT"):
                    value[header[col["name"]]["name"]] = col["children"][0]["characters"]
                    header[col["name"]]["type"] = "TEXT"
                    color = col["children"][0]["fills"][0]["color"]
                    textColor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
                if(col["children"][0]["type"]=="IMAGE"):
                    value[header[col["name"]]["name"]] = getFormatedName(col["name"])
                    header[col["name"]]["type"] = "IMAGE"
                    images.append({"id":col["id"],"name":getFormatedName(col["name"])})                   
                    
            values.append(value)
    color = data["background"][0]["color"]
    bodyColor = "rgba("+str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])+")"
    style = TableStyle(headerColor,bodyColor,textColor,headertextColor,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)
    (elementwidth,elementheight,xielem,yielem) = getDimensions(data)
    style.setHeight(elementheight)
    style.setWidth(elementwidth)
    style.setX(xielem)
    style.setY(yielem)
    table = Table(id,"",name,"COMPONENT_ASSET",values,header,nrrows,images,style)
    return table

def getDimensions(data):
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
    return (elementwidth,elementheight,xielem,yielem)