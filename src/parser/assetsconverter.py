from parser.model.Vue3SelectComponent import Vue3SelectComponent
from parser.model.Vue3SelectComponentStyle import Vue3SelectComponentStyle
from parser.model.InputSearchFilter import InputSearchFilter
from parser.model.InputSearchFilterStyle import InputSearchFilterStyle
from parser.model.DatePicker import DatePicker
from parser.model.DatePickerStyle import DatePickerStyle

import re 

def convertToVueSelect(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):

    placeholder = ""
    selectedcolor = ""
    nonselectedcolor = ""
    txtcolor = ""
    for c in data["children"]:
        if(c["name"]=="State=Closed"):
            for h in c["children"]:
                if(h["name"]=="Header"):
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

    style = Vue3SelectComponentStyle(
        "rgba("+selectedcolor[0]+","+selectedcolor[1]+","+selectedcolor[2]+","+selectedcolor[3]+")",
        "rgba("+selectedcolor[0]+","+selectedcolor[1]+","+selectedcolor[2]+","+selectedcolor[3]+")",
        "rgba("+nonselectedcolor[0]+","+nonselectedcolor[1]+","+nonselectedcolor[2]+","+nonselectedcolor[3]+")",
        "rgba("+txtcolor[0]+","+txtcolor[1]+","+txtcolor[2]+","+txtcolor[3]+")",
        "rgba("+nonselectedcolor[0]+","+nonselectedcolor[1]+","+nonselectedcolor[2]+","+nonselectedcolor[3]+")",
        "rgba("+selectedcolor[0]+","+selectedcolor[1]+","+selectedcolor[2]+","+selectedcolor[3]+")",
        "rgba("+txtcolor[0]+","+txtcolor[1]+","+txtcolor[2]+","+txtcolor[3]+")",
        nr_columnstart,
        nr_columnend,
        nr_rowstart,
        nr_rowend
    )
    pattern = "[:;]"
    elemid = re.sub(pattern,"",str(id))
    melement = Vue3SelectComponent(id,"",name,"COMPONENT_ASSET","selectedOption"+elemid,alloptions,placeholder,False,style)

    return melement

def convertToSearchInputFilter(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    placeholder = ""
    pattern = "[:;]"
    elemid = re.sub(pattern,"",str(id))
    vmodel = "inputsearch"+str(elemid)
    backgroundcolor = str(data["backgroundColor"]["r"] * 255)+","+str(data["backgroundColor"]["g"] * 255)+","+str(data["backgroundColor"]["b"] * 255)+","+str(data["backgroundColor"]["a"])
    radius = str(data["cornerRadius"])
    for e in data["children"]:
        if(e["type"]=="TEXT"):
            placeholder = e["characters"]
            color = e["fills"][0]["color"]
            txtcolor = str(color["r"] * 255)+","+str(color["g"] * 255)+","+str(color["b"] * 255)+","+str(color["a"])
    style = InputSearchFilterStyle(backgroundcolor,color,radius,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)

    inputsearchfilter =  InputSearchFilter(id,"",name,"COMPONENT_ASSET",vmodel,placeholder,style)

    return inputsearchfilter

def convertToDatePicker(data,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend,id,name):
    pattern = "[:;]"
    elemid = re.sub(pattern,"",str(id))
    vmodel = "datepicker"+str(elemid)
    dateinput = None
    dropdowninput = None
    dropdownbackgroundcolor = None
    for d in data["children"]:
        if(d["name"]=="DateInput"):
            dateinput = d
            if(len(dateinput["children"])>0):
                dropdowninput = dateinput["children"][0]
                dropdownbackgroundcolor = str(dropdowninput["backgroundColor"]["r"] * 255)+","+str(dropdowninput["backgroundColor"]["g"] * 255)+","+str(dropdowninput["backgroundColor"]["b"] * 255)+","+str(dropdowninput["backgroundColor"]["a"])
    backgroundcolor = str(dateinput["backgroundColor"]["r"] * 255)+","+str(dateinput["backgroundColor"]["g"] * 255)+","+str(dateinput["backgroundColor"]["b"] * 255)+","+str(dateinput["backgroundColor"]["a"])
    
    style = DatePickerStyle(backgroundcolor,dropdownbackgroundcolor,nr_columnstart,nr_columnend,nr_rowstart,nr_rowend)

    datepicker =  DatePicker(id,"",name,"COMPONENT_ASSET",vmodel,style)

    return datepicker
