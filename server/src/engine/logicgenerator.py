from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction
from parser.model.OverlayAction import OverlayAction 
from parser.model.CloseAction import CloseAction
from parser.model.ScrollAction import ScrollAction
from parser.model.OpenLinkAction import OpenLinkAction 
from parser.model.BackAction import BackAction 
from parser.model.SwapAction import SwapAction 
from parser.model.ChangeAction import ChangeAction
from parser.model.Mcomponent import Mcomponent
from parser.model.Melement import Melement
from parser.model.ContainerElement import ContainerElement
import re
import itertools

# id: [vars]
shareableEvents = {}
keyEvents = {}
swapDestinationIds = []
swapComponentTriggerIds = {}
alldata = {}
allEmissions = {}

def handleBehaviour(elem,allPagesInfo,pagename,isPageRender,allvariants,data,allEmissionpaths,allclosePaths):
    global shareableEvents,keyEvents,swapDestinationIds, alldata, allEmissions, swapComponentTriggerIds
    alldata = data
    allEmissions = allEmissionpaths
    hooks = {}
    if(pagename not in keyEvents): keyEvents[pagename] = {}
    elemBehaviour = [[],None]
    elementid = elem.getIdElement() if isinstance(elem,Melement) else elem.getIdComponent()
    methodName = ""
    # SWAP ACTIONS
    if(elementid in swapDestinationIds):
        elemBehaviour[0].append(f'v-if="showswaped{getElemId(elementid)}"')
    # ACTION ANIMATIONS
    elemAnimation = elem.gethasAnimation()
    for interaction in elem.getInteractions():
        if(interaction.getInteractionType()==InteractionElement.Interaction.ONHOVER):
            for action in interaction.actions:
                if(isinstance(action,OverlayAction)):
                    destinationid = getElemId(action.getDestinationID())
                    methodName = "changeVisibility"+destinationid
                    elemBehaviour[0].extend(['@mouseenter="'+methodName+'"','@mouseleave="'+methodName+'"'])
                    if(isinstance(elem,Melement) and isfromInstance(elem.getIdElement()) and elem.getupperIdComponent()!=None):
                        shareableEvents.setdefault(elem.getupperIdComponent(), []).append(("show-from"+getElemId(elem.getIdElement())+"-to"+getElemId(action.getDestinationID()),"show"+getElemId(action.getDestinationID())+'=true',''))
                        shareableEvents.setdefault(action.getDestinationID(), []).append((None,None,'v-if="show'+getElemId(action.getDestinationID())+'"'))
                        insertFunction("methods",hooks,methodName,showOverlayonHover(methodName,"show"+destinationid))
                        elemBehaviour[1] = hooks
                    
                    elemBehaviour[1] = hooks
        else:
            for action in interaction.actions:
                # SWAP ACTIONS
                if(isinstance(action,SwapAction)):
                    destinationid = action.getDestinationID()
                    methodName = "swap"+getElemId(elementid)+getElemId(destinationid)
                    swapDestinationIds.append(destinationid)
                    if(elem.getupperIdComponent()!=None and "#Page" not in elem.gettopmostnode()):
                        elemBehaviour[0].append(f'v-on:click="{methodName}"')                        
                        insertFunction("methods",hooks,methodName,swapTopmostOverlay(methodName,f'swapfrom{getElemId(elementid)}to{getElemId(destinationid)}'))
                        swapComponentTriggerIds.setdefault(getElemId(elem.getupperIdComponent()), []).append((getElemId(elementid),getElemId(destinationid)))
                    if(isinstance(elem,Melement) and elem.gettypeElement()=="OVERLAY"):
                        pass
                    else:
                        pass
                    elemBehaviour[1] = hooks
                # NAVIGATION ACTIONS
                if(isinstance(action,NavigationAction)):
                    destination = getPageById(action.getDestinationID(),allPagesInfo) 
                    methodName = "goto"+destination+getElemId(elementid)
                    insertFunction("methods",hooks,methodName,getNavigationFunction(methodName,destination))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                # OPEN LINK ACTIONS
                if(isinstance(action,OpenLinkAction)):
                    methodName = "openLink"+getElemId(elementid)
                    insertFunction("methods",hooks,methodName,getOpenLinkFunction(methodName,action))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                # BACK ACTIONS
                if(isinstance(action,BackAction)):
                    methodName = "goBack"+getElemId(elementid)
                    insertFunction("methods",hooks,methodName,getBackFunction(methodName))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                # SCROLL ACTIONS
                if(isinstance(action,ScrollAction)):
                    elemBehaviour = insertScrollBehaviour(elem,action,hooks,elemBehaviour)
                # OVERLAY ACTIONS
                if(isinstance(action,OverlayAction)):
                    destinationid = getElemId(action.getDestinationID())
                    methodName = "changeVisibility"+destinationid
                    if(checkOverlayTrigger(elementid)!=None): 
                        pair = checkOverlayTrigger(elementid)
                        methodName = "openOverlay"+getElemId(pair[0])+"_"+getElemId(pair[1])
                        if(pair[2]==True):
                            methodName = "changeVisibility"+getElemId(pair[1])
                            insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+getElemId(pair[1]),getElemId(pair[0]),elemAnimation))
                            elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                        else:
                            insertFunction("methods",hooks,methodName,openTopOverlay(methodName,"openoverlay"+getElemId(pair[0])+getElemId(pair[1])))
                            elemBehaviour[0].append("@click"+'="'+methodName+'"')
                    else:
                        insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+destinationid,elementid,elemAnimation))
                        elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                # CLOSE ACTIONS
                if(isinstance(action,CloseAction)):
                    #check if it's inside a component
                    insidecomponent = checkcloseinsideComponent(elementid,allclosePaths)
                    if(insidecomponent[0]==True):
                        originid = getElemId(insidecomponent[1][0])
                        destinationid = getElemId(insidecomponent[1][1])
                        methodName = "close"+originid+destinationid
                        if(isPageRender==False): insertFunction("methods",hooks,methodName,closeOverlay(methodName,"close-from"+str(originid)+"-to"+str(destinationid)))
                        else: insertFunction("methods",hooks,methodName,getCloseFunction(methodName,"show"+destinationid,destinationid))
                        elemBehaviour[0].append('@click="'+methodName+'"')
                        elemBehaviour[1] = hooks
                if(interaction.getInteractionType()==InteractionElement.Interaction.ONMOUSEDOWN):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    if(interaction.getTimeout()>0):
                        insertFunction("methods",hooks,"delayed"+methodName,getdelayedFunction(methodName,interaction.getTimeout())) 
                        methodName="delayed"+methodName                   
                    elemBehaviour[0].append('v-on:mousedown="'+methodName+'()"')                    
                    elemBehaviour[1] = hooks
                if(interaction.getInteractionType()==InteractionElement.Interaction.ONMOUSEUP):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    if(interaction.getTimeout()>0):
                        insertFunction("methods",hooks,"delayed"+methodName,getdelayedFunction(methodName,interaction.getTimeout())) 
                        methodName="delayed"+methodName                   
                    elemBehaviour[0].append('v-on:mouseup="'+methodName+'()"')                    
                    elemBehaviour[1] = hooks
                if(interaction.getInteractionType()==InteractionElement.Interaction.ONMOUSEENTER):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    if(interaction.getTimeout()>0):
                        insertFunction("methods",hooks,"delayed"+methodName,getdelayedFunction(methodName,interaction.getTimeout())) 
                        methodName="delayed"+methodName                   
                    elemBehaviour[0].append('v-on:mouseenter="'+methodName+'()"')                    
                    elemBehaviour[1] = hooks
                if(interaction.getInteractionType()==InteractionElement.Interaction.ONMOUSELEAVE):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    if(interaction.getTimeout()>0):
                        insertFunction("methods",hooks,"delayed"+methodName,getdelayedFunction(methodName,interaction.getTimeout())) 
                        methodName="delayed"+methodName                   
                    elemBehaviour[0].append('v-on:mouseleave="'+methodName+'()"')                    
                    elemBehaviour[1] = hooks
                if(interaction.getInteractionType()==InteractionElement.Interaction.AFTERTIMEOUT):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    insertFunction("created",hooks,methodName,getTimeoutFunction(methodName,interaction))
                    elemBehaviour[1] = hooks                    
                if(interaction.getInteractionType()==InteractionElement.Interaction.ONDRAG):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    elemBehaviour[0].append('draggable="true" @dragstart="'+methodName+'()"')                    
                    elemBehaviour[1] = hooks                    
                if(interaction.getInteractionType()==InteractionElement.Interaction.ONKEYDOWN):
                    if(len(elemBehaviour[0])>0): elemBehaviour[0].pop()
                    if("mounted" not in hooks or getKeyEventListenerMounted() not in hooks["mounted"]): hooks.setdefault("mounted", []).append(getKeyEventListenerMounted())
                    if("beforeUnmount" not in hooks or getKeyEventListenerUnMounted() not in hooks["beforeUnmount"]): hooks.setdefault("beforeUnmount", []).append(getKeyEventListenerUnMounted())
                    setKeyCodesMethods(interaction.getKeyCodes(),pagename,"this."+methodName+"();")
        # HANDLE EVENTS ON VARIANT COMPONENTS
        if(isinstance(elem, Mcomponent) and elem.getisVariant()==True):
            elemBehaviour = handleVariants(elem,allvariants,hooks,elemBehaviour,allPagesInfo)
    # HANDLE COMPONENT VARIANT INSTANCES IN VIEW PAGES
    if(isinstance(elem, Mcomponent) and elem.getisVariant()==True):
        elemBehaviour = declareMountedVariables(elem,hooks,elemBehaviour)
    # HANDLE SCROLL BEHAVIOUR
    if(isinstance(elem,ContainerElement) and elem.style.getOverflowDirection()!=None):
        elemBehaviour = handleScrollBehaviour(elem,hooks,elemBehaviour)        
    # HANDLE MENU LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Menu"):
        elemBehaviour = insertMenuLogic(elem,allPagesInfo,hooks,elemBehaviour)
    # POPULATE DATATABLE
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Table"):
        elemBehaviour = insertTableLogic(elem,allPagesInfo,hooks,elemBehaviour)
    # POPULATE DROPDOWN
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Dropdown"):
        elemBehaviour = insertDropdownLogic(getElemId(elem.getIdComponent()),hooks,elemBehaviour)
    # HANDLE CHECKBOX LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Checkbox"):
        elemBehaviour = insertCheckboxLogic(getElemId(elem.getIdComponent()),hooks,elemBehaviour)
    # HANDLE FORM LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Form"):
        elemBehaviour = insertFormLogic(getElemId(elem.getIdComponent()),elem.inputs,hooks,elemBehaviour)
    # HANDLE SLIDER LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Slider"):
        elemBehaviour = insertSliderLogic(getElemId(elem.getIdComponent()),hooks,elemBehaviour)
    # HANDLE CONDITIONAL VISIBLE ELEMENTS
    if(elem.gethascondvisib()==True):
        elemBehaviour[0].append('v-show="show'+getElemId(elem.getIdElement())+'==true"')
    # SHOW CONDITIONAL ELEMENTS | from page
    if(isinstance(elem,Mcomponent) and isPageRender==True):
        idclosepath = checkIDinClosepath(elem.getIdComponent(), allclosePaths)
        if(idclosepath[0]==True and idclosepath[2]==True):
            originid = getElemId(idclosepath[1][0])
            destinationid = getElemId(idclosepath[1][1])
            methodName = "closefrom"+originid+"to"+destinationid
            insertFunction("methods",hooks,methodName,getCloseFunction(methodName,"show"+destinationid,destinationid))
            elemBehaviour[0].append('v-if="show'+destinationid+'"')
            elemBehaviour[0].append('@close-from'+originid+'-to'+destinationid+'="'+methodName+'"')
            elemBehaviour[1] = hooks
        if(idclosepath[0]==True and idclosepath[2]==False):
            originid = getElemId(idclosepath[1][0])
            destinationid = getElemId(idclosepath[1][1])
            methodName = "closefrom"+originid+"to"+destinationid
            insertFunction("methods",hooks,methodName,getCloseFunction(methodName,"show"+destinationid,destinationid))
            elemBehaviour[0].append('v-if="show'+destinationid+'"')
            elemBehaviour[0].append('@close-from'+originid+'-to'+destinationid+'="'+methodName+'"')
            elemBehaviour[1] = hooks
        if(checkIDinEventspath(elem.getIdComponent())!=None): 
            pair = checkIDinEventspath(elem.getIdComponent())
            methodName = "openOverlay"+getElemId(pair[0])+"_"+getElemId(pair[1])
            if(pair[2]==True):
                methodName = "changeVisibility"+getElemId(pair[1])
                insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+getElemId(pair[1]),getElemId(pair[0]),elemAnimation))
            else:
                insertFunction("methods",hooks,methodName,openTopOverlay(methodName,"openoverlay"+getElemId(pair[0])+getElemId(pair[1])))
            elemBehaviour[0].append('@'+"openoverlay"+getElemId(pair[0])+getElemId(pair[1])+'="'+methodName+'"')

        if(elem.getIdComponent() in shareableEvents):
            for event in shareableEvents[elem.getIdComponent()]:
                elemBehaviour[0].append(event[2])
                if(event[0]!=None and event[1]!=None): elemBehaviour[0].append('@'+event[0]+'="'+event[1]+'"')
        #if(elem.getisComponentInstance()==False and elem.getIdComponent() not in swapDestinationIds):
        #    elemBehaviour[0].append('v-if="show'+getElemId(elem.getIdComponent())+'"')
        if(elem.getisComponentInstance()==False and elem.getIdComponent() in swapDestinationIds):
            elemBehaviour[0].append('v-if="showswaped'+getElemId(elem.getIdComponent())+'"')
        if(getElemId(elem.getIdComponent()) in swapComponentTriggerIds and elem.getTypeComponent()=="OVERLAY"):
            for (originid,destinationid) in swapComponentTriggerIds[getElemId(elem.getIdComponent())]:
                methodName = "swap"+getElemId(elem.getIdComponent())+destinationid
                insertFunction("methods",hooks,methodName,getSwapFunction(methodName,getElemId(elem.getIdComponent()),destinationid))
                elemBehaviour[0].append(f'v-if="showswaped{getElemId(elem.getIdComponent())}"')
                elemBehaviour[0].append(f'@swapfrom{originid}to{destinationid}="{methodName}"')
        elemBehaviour[1] = hooks
    processVifs(elemBehaviour[0])
    return elemBehaviour

# METHOD TO CHECK IF ELEMENTS INVOLVED ARE IN THE SAME PAGE
# METHOD TO HANDLE mouseover EVENTS when elements are not overlaping 
def isParentChildRelationship(id1,id2,pagename,allpagesInfo):
    if(pagename not in allpagesInfo): return False
    elementos = []
    allElements = list(itertools.chain(*([x] + x.children for x in allpagesInfo[pagename]["pageElements"])))
    for el in allElements:
        if((isinstance(el,Melement) and el.getIdElement()==id1) or (isinstance(el,Melement) and el.getIdElement()==id2) and
           (isinstance(el,Mcomponent) and el.getIdComponent()==id1) or (isinstance(el,Mcomponent) and el.getIdComponent()==id2)):
            elementos.append(el)
    if(len(elementos)==2 and type(elementos[0])!=type(elementos[1])): return True 

def insertFunction(hook,hooks,functioname,function):
    if(hook not in hooks): hooks[hook]=[]
    if((not any(x[0]==functioname for x in hooks[hook]))):
        hooks.setdefault(hook, []).append((functioname,function))

def getPageById(id,allPages):
    for pagename in allPages:
        if(allPages[pagename]["id"]==id): return getFormatedName(allPages[pagename]["name"])
    return ""

def getNavigationFunction(name,destination):
    function = """        """ + name + "(){" + """
            this.$router.push({path:"/""" + destination.lower() + """"});
        }""" 
    return function
    
def getChangeVisibilityFunction(name,variable,elementid,elemAnimation):
    global alldata
    changeswaped = ""
    setanimationvar = ""
    for x in alldata:
        if("showswaped"+variable[4:] in x):
            changeswaped = "this.showswaped"+variable[4:]+"= true"+"\n"
    if(elemAnimation==True):
        setanimationvar = f"this.setAnimationName('el{getElemId(elementid)}')"+"\n"
    function = """\t\t""" + name + "(){" + """
            this.""" + variable +  """ = true;"""+f"""
            {changeswaped}{setanimationvar}"""+"""
        }""" 
    return function

def swapTopmostOverlay(name,event):
    function = """\t\t""" + name + "(){" + """
            this.$emit('""" + event +  """');
        }""" 
    return function

def openTopOverlay(name,event):
    function = """\t\t""" + name + "(){" + """
            this.$emit('""" + event +  """');
        }""" 
    return function

def getCloseFunction(name,variable,elementid):
    global alldata
    changeswaped = ""
    for x in alldata:
        if("showswaped"+getElemId(elementid) in x):
            changeswaped = "this.showswaped"+getElemId(elementid)+"= false"+"\n"
    function = """\t\t""" + name + "(){" + """
            this.""" + variable +  """ = false;"""+f"""
            {changeswaped}"""+"""
        }""" 
    return function

def closeOverlay(name,event):
    function = """\t\t""" + name + "(){" + """
            this.$emit('""" + event +  """');
        }""" 
    return function

def getpopulateDropdownFunction(functionname,values,options):
    function =f"""        {functionname}()"""+"{"+f"""
            /*Here you can adapt to fetch the data from an API*/
            this.{values} = this.{options}.map(x => x.value);"""+"""
        }""" 
    return function

def getpopulateCheckboxFunction(functionname,values,boxes):
    function =f"""        {functionname}()"""+"{"+f"""
            /*Here you can adapt to fetch the data from an API*/
            this.{boxes} = this.{values};"""+"""
        }""" 
    return function

def getScrollBehaviourFunction(elem,action):
    function =f"""        scrollTo{getElemId(elem.getIdElement())}()"""+"{"+f"""
            this.$refs.ref{getElemId(action.getDestinationID())}?.scrollIntoView("""+"{ behavior: 'smooth', block: 'nearest', inline: 'center' });"+"""
        }""" 
    return function

def insertSliderLogic(idSlider,hooks,elemBehaviour):
    sliderFunction = f"""slider{idSlider}"""+"""(newvalue,oldvalue){
            const toastStore = useToastStore();
            let message = "Slider value: "+newvalue            
            /* Here we are displaying the value changed from the Slider component into the Toast from our toast pinia store.*/   
            toastStore.showInfo(message);
        }
"""
    hooks.setdefault("watch", []).append((f"slider{idSlider}",sliderFunction))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertFormLogic(idform,inputs,hooks,elemBehaviour):
    elemBehaviour[0] = []
    function = f"""
        const initialValues{idform} = ref("""+'{\n'
    nr_input = 0
    for i in inputs:
        nr_input+=1
        function += "           "+f"input{nr_input}{idform}"+": '',\n"
    function=function[:-1]+"""
        });
    """
    function+=f"""
        const resolver{idform} = ("""+"{ values }) => {"+"""
            const errors = {};
            /*Here you can adapt the code to check if the input text fulfills some criteria and show the error message. */
        """
    nr_input = 0
    for i in inputs:
        nr_input+=1
        function += f"""    if (!values.input{nr_input}{idform})"""+ "{"+f"""
                errors.input{nr_input}{idform} = ["""+"{ message: "+f"""'{i["placeholder"]} is required.'"""+ "}];"+"""
            }
        
        """
    function=function[:-1]+"""
            return {
                errors
            };
        };
    """
    toastFunction =f"""onFormSubmit{idform}(data)"""+""" {
        const toastStore = useToastStore();
        let message = ""
        /*Here you can adapt the code to change the toast message or you can send data to the backend by doing a POST or PUT request. */
        if(data.valid){
            message = "The form was successfully submited!"            
            toastStore.showSuccess(message);
        }
        if(!data.valid){
            message = "Error in form submission!"            
            toastStore.showError(message);
        }
    }
    """
    hooks.setdefault("setup", []).append(([f"initialValues{idform}",f"resolver{idform}"],function))
    hooks.setdefault("methods", []).append((f"onFormSubmit{idform}",toastFunction))
    elemBehaviour[1] = hooks
    return elemBehaviour

def getMenuFunction(elem,allPagesInfo,functionname):
    bodyfunction=""
    function=""
    for option in elem.options:
        if("destination" in option):
            destination = getPageById(option["destination"],allPagesInfo) 
            if(destination!="" and destination!=None):
                bodyfunction += f'    if (item.option == "{option["option"]}") ' + '{ ' + f'this.$router.push({{ path: "/{destination.lower()}" }});' + '}\n'
    function =f"""        {functionname}(item)"""+"{"+f"""
        {bodyfunction}"""+"""        }"""
    return function

def showOverlayonHover(name,variable):
    function = """\t\t""" + name + "(){" + """
            this.""" + variable +  """ = !this.""" + variable +";"+"""
        }""" 
    return function

def insertDropdownLogic(dropdownid,hooks,elemBehaviour):
    
    hooks.setdefault("methods", []).append(('getDropdownOptions'+str(dropdownid),getpopulateDropdownFunction('getDropdownOptions'+str(dropdownid),'allOptionValues'+str(dropdownid),'allOptions'+str(dropdownid))))
    hooks.setdefault("mounted", []).append(('getDropdownOptions'+str(dropdownid),"          this."+'getDropdownOptions'+str(dropdownid)+"();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertCheckboxLogic(checkboxid,hooks,elemBehaviour):
    
    hooks.setdefault("methods", []).append(('getCheckboxOptions'+str(checkboxid),getpopulateCheckboxFunction('getCheckboxOptions'+str(checkboxid),'boxesValues'+str(checkboxid),'boxes'+str(checkboxid))))
    hooks.setdefault("mounted", []).append(('getCheckboxOptions'+str(checkboxid),"          this."+'getCheckboxOptions'+str(checkboxid)+"();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertScrollBehaviour(elem,action,hooks,elemBehaviour):
    elemBehaviour[0].append('v-on:click="'+f"scrollTo{getElemId(elem.getIdElement())}"+'()"')
    hooks.setdefault("methods", []).append((f"scrollTo{getElemId(elem.getIdElement())}",getScrollBehaviourFunction(elem,action)))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertMenuLogic(elem,allPagesInfo,hooks,elemBehaviour):
    hooks.setdefault("methods", []).append((f"selectedItem{getElemId(elem.getIdComponent())}",getMenuFunction(elem,allPagesInfo,f"selectedItem{getElemId(elem.getIdComponent())}")))
    elemBehaviour[1] = hooks
    return elemBehaviour

def handleScrollBehaviour(elem,hooks,elemBehaviour):
    mountedFunction = f'          window.addEventListener("mouseup", this.onMouseUp{getElemId(elem.getIdElement())});'
    destroyedFunction = f'          window.removeEventListener("mouseup", this.onMouseUp{getElemId(elem.getIdElement())});'

    hooks.setdefault("mounted", []).append((f"getMountedFunction{getElemId(elem.getIdElement())}",mountedFunction))
    hooks.setdefault("destroyed", []).append((f"getDestroyedFunction{getElemId(elem.getIdElement())}",destroyedFunction))
    
    mousedownFunction = f'''        onMouseDown{getElemId(elem.getIdElement())}(ev)'''+'''{
            this.cursorPos = [ev.pageX, ev.pageY];
            this.isDragging = true;

            '''+f'window.addEventListener("mousemove", this.onMouseHold{getElemId(elem.getIdElement())});'+'''
        }'''
    hooks.setdefault("methods", []).append((f"onMouseDown{getElemId(elem.getIdElement())}",mousedownFunction))
    
    mouseupFunction = f'''        onMouseUp{getElemId(elem.getIdElement())}(ev)'''+'''{
            '''+f'window.removeEventListener("mousemove", this.onMouseHold{getElemId(elem.getIdElement())});'+f'''
            this.isDragging = false;'''+'''
        }'''
    hooks.setdefault("methods", []).append((f"onMouseUp{getElemId(elem.getIdElement())}",mouseupFunction))
    transition = ""
    if(elem.style.getOverflowDirection()=="HORIZONTAL"):
        transition = "left: -delta[0]"
    else:
        transition = "top: -delta[1]"        
    mouseholdFunction = f'''        onMouseHold{getElemId(elem.getIdElement())}(ev)'''+'''{
            ev.preventDefault();

            requestAnimationFrame(() => {
                    const delta = [ev.pageX - this.cursorPos[0], ev.pageY - this.cursorPos[1]];

                    this.cursorPos = [ev.pageX, ev.pageY];

                    '''+f'''if (!this.$refs.ref{getElemId(elem.getIdElement())}) return;
                    this.$refs.ref{getElemId(elem.getIdElement())}.scrollBy('''+'''{
                    '''+transition+'''});
            });
        }'''
    hooks.setdefault("methods", []).append((f"onMouseHold{getElemId(elem.getIdElement())}",mouseholdFunction))
    elemBehaviour[1] = hooks
    return elemBehaviour

def getDatatableValuesFunction(tableid,values):
    function = """\t\tgetDatatableValues""" + str(tableid) + "(){" + """
            this.tablevalues""" + str(tableid) +f""" = {values};"""+"""
        }""" 
    return function

def insertTableLogic(elem,allPagesInfo,hooks,elemBehaviour):
    hooks.setdefault("methods", []).append((f'getDatatableValues{getElemId(elem.getIdComponent())}',getDatatableValuesFunction(getElemId(elem.getIdComponent()),elem.values)))
    hooks.setdefault("mounted", []).append((f'getDatatableValues{getElemId(elem.getIdComponent())}',f"          this.getDatatableValues{getElemId(elem.getIdComponent())}();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def addPropsFunction(allhooks,pagename):
    function = "\tgetProps(l){" + """
        let f = {}
        l.forEach((item) => {
        for (const [key, value] of Object.entries(item)) {
            let mvalue = value;
            if(key==='atributes'){
                for (const [key, value] of Object.entries(mvalue)) {
                    f[key]=value;
                }
            }
        }
        });
        return f;
    }
    """ 
    lhooks = {}
    lhooks.setdefault("methods", []).append(("getProps",function))
    if("methods" not in allhooks[pagename]): allhooks[pagename]["methods"] = []
    if(("getProps",function) not in allhooks[pagename]["methods"]):
        allhooks[pagename].setdefault("methods", []).extend(lhooks["methods"])
    return function

def addSetAnimationVarFunction(allhooks,pagename):
    function = getAnimationVarFunction()
    lhooks = {}
    lhooks.setdefault("methods", []).append(("setAnimationName",function))
    if("methods" not in allhooks[pagename]): allhooks[pagename]["methods"] = []
    if(("setAnimationName",function) not in allhooks[pagename]["methods"]):
        allhooks[pagename].setdefault("methods", []).extend(lhooks["methods"])
    return function

def getVariantVariables(elem,id):
    return f"""          this.selectedClass{id} = this.componentclass{id};
          this.currentVariant{id} = '{getFormatedName(elem.getNameComponent()).lower()}';"""
    
def declareMountedVariables(elem,hooks,elemBehaviour):
    hooks.setdefault("mounted", []).append((f'getVariantVariables{getElemId(elem.getIdComponent())}',getVariantVariables(elem,getElemId(elem.getIdComponent()))))
    elemBehaviour[1] = hooks
    return elemBehaviour
    
def getComponentVariant(id,variants):
    for v in variants:
        for c in v.variantComponents:
            if(id==c.getIdComponent()):
                return c
    return None

def changeToHoveredFunction(elem,destelem):
    function = ""
    if(destelem!=None):
        function = """\t\t""" + f"changeToHovered{getElemId(elem.getIdComponent())}()"+"{" + f"""
                this.selectedClass{getElemId(elem.getIdComponent())}=this.componentclass{getElemId(destelem.getIdComponent())};
                this.currentVariant{getElemId(elem.getIdComponent())}= '{getFormatedName(destelem.getNameComponent()).lower()}'
    """+"\t\t}"
    return function

def changeToDefaultFunction(elem,destelem):
    function = """\t\t""" + f"changeToDefault{getElemId(elem.getIdComponent())}()"+"{" + f"""
            this.selectedClass{getElemId(elem.getIdComponent())}=this.componentclass{getElemId(elem.getIdComponent())};
            this.currentVariant{getElemId(elem.getIdComponent())}= '{getFormatedName(elem.getNameComponent()).lower()}'
"""+"\t\t}"
    return function

def changeVariantFunction(elem,destinations):
    elsecond = False
    elsecondst = "if"
    function = """\t\t""" + f"changeVariant{getElemId(elem.getIdComponent())}()"+"{" 
    for variant in destinations: 
        if(elsecond==True): elsecondst = "else if"      
        function+=f"""
        {elsecondst}(this.selectedClass{getElemId(elem.getIdComponent())}==this.componentclass{getElemId(variant[0].getIdComponent())})"""+"{"+f"""
                this.selectedClass{getElemId(elem.getIdComponent())}=this.componentclass{getElemId(variant[1].getIdComponent())};
                this.currentVariant{getElemId(elem.getIdComponent())}= '{getFormatedName(variant[1].getNameComponent()).lower()}'
"""+"""\t\t}"""
        elsecond = True
    function+="}"
    return function

def getDestinations(beginid,elem,variants,destinations):
    if(len(elem.interactions)==0): return destinations
    for i in elem.interactions:
         for a in i.actions:
            if(isinstance(a,ChangeAction) and i.getInteractionType()==InteractionElement.Interaction.ONCLICK):
                destelem = getComponentVariant(a.destinationID,variants)
                if(destelem!=None): 
                    destinations.append((elem,destelem))
                    if(destelem.getIdComponent()==beginid): return destinations
                    return getDestinations(beginid,destelem,variants,destinations)
                
def getVariantNavigationFunction(methodName,beginElem,currentElem,destination):
    if(beginElem==None and currentElem!=None): beginElem = currentElem  
    function = """\t\t""" + methodName + "(){" + f"""
            if(this.selectedClass{getElemId(beginElem.getIdComponent())}==this.componentclass{getElemId(currentElem.getIdComponent())})"""+"{"+"""
                this.$router.push({path:"/""" + destination.lower() + """"});
            }
    \t}""" 
    return function

def getdelayedFunction(methodName,timeout):
    function = f"        delayed{methodName}"+"""(){
            setTimeout(() => """ +f"""this.{methodName},"""+f"""{str(timeout)})
        """+"""}"""
    return function    
    
def getOpenLinkFunction(methodName,action):            
    function =f"        {methodName}"+"""(){
       """
    if(action.getopenInNewTab()==True):
        function+="            window.open('"+action.getUrl()+"', '_blank'); "
    else:
        function+="            window.location.href = '"+ action.getUrl() + "'"
    function += "\n\t\t}"
    return function

def getSwapFunction(methodName,elementid,destinationid):
    global alldata
    changedestinationshow = ""
    for x in alldata:
        if("show"+getElemId(destinationid) in x):
            changedestinationshow = "this.show"+getElemId(destinationid)+"= true"+"\n"
    function =f"        {methodName}"+"""(){
            """+ f"""this.showswaped{getElemId(elementid)}=false""" + """
            """+ f"""this.showswaped{getElemId(destinationid)}=true"""+f"""
            {changedestinationshow}"""
    function += "\n        }"
    return function

def getBackFunction(methodName):
    function =f"    {methodName}"+"""(){
        """+ f"""this.$router.back()"""
    function += "\n\t}"
    return function

def getTimeoutFunction(methodName,interaction):
    timeout = str(interaction.getTimeout()*1000)
    function ="""
        setTimeout(()=>{"""+f"""
            this.{methodName}()
        """+"""}, """+f"""{timeout})
        """
    if(methodName==""): function=""
    return function    

def replaceDefault(comp,originid,destname):
    if hasattr(comp, 'getIdComponent'): 
        if(getElemId(comp.getIdComponent())==getElemId(originid)):
            comp.setNameComponent(destname)
    if hasattr(comp, 'getIdElement'): 
        if(getElemId(comp.getIdElement())==getElemId(originid)):
            comp.setName(destname)
    for ch in comp.children:
        replaceDefault(ch,originid,destname)

def handleVariants(elem,variants,hooks,elemBehaviour,allPagesInfo,beginElem=None):
    if(checkIDinEventspath(getElemId(elem.getIdComponent()))!=None): 
        pair = checkIDinEventspath(getElemId(elem.getIdComponent()))
        methodName = "openOverlay"+getElemId(pair[0])+"_"+getElemId(pair[1])
        if(pair[2]==True):
            methodName = "changeVisibility"+getElemId(pair[1])
            insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+getElemId(pair[1]),getElemId(pair[0]),False))
        else:
            insertFunction("methods",hooks,methodName,openTopOverlay(methodName,"openoverlay"+getElemId(pair[0])+getElemId(pair[1])))
        elemBehaviour[0].append('@'+"openoverlay"+getElemId(pair[0])+getElemId(pair[1])+'="'+methodName+'"')
    for i in elem.interactions:
         for a in i.actions:
            destelem = getComponentVariant(a.destinationID,variants)
            if(isinstance(a,ChangeAction) and i.getInteractionType()==InteractionElement.Interaction.ONHOVER):
                elemBehaviour[0].extend([f'@mouseover="changeToHovered{getElemId(elem.getIdComponent())}"',f'@mouseleave="changeToDefault{getElemId(elem.getIdComponent())}"'])
                hooks.setdefault("methods", []).append((f'changeToHovered{getElemId(elem.getIdComponent())}',changeToHoveredFunction(elem,destelem)))
                hooks.setdefault("methods", []).append((f'changeToDefault{getElemId(elem.getIdComponent())}',changeToDefaultFunction(elem,destelem)))
                if(destelem!=None and len(destelem.interactions)>0):
                    handleVariants(destelem,variants,hooks,elemBehaviour,allPagesInfo,elem)
                elemBehaviour[1] = hooks
            if(isinstance(a,ChangeAction) and i.getInteractionType()==InteractionElement.Interaction.ONCLICK and len(destelem.interactions)>=0):
                destinations = getDestinations(elem.getIdComponent(),elem,variants,[])
                elemBehaviour[0].append(f'@click="changeVariant{getElemId(elem.getIdComponent())}"')
                hooks.setdefault("methods", []).append((f'changeVariant{getElemId(elem.getIdComponent())}',changeVariantFunction(elem,destinations)))
                elemBehaviour[1] = hooks
            if(isinstance(a,NavigationAction) and i.getInteractionType()==InteractionElement.Interaction.ONCLICK):
                destination = getPageById(a.getDestinationID(),allPagesInfo) 
                methodName = "goto"+destination+getElemId(elem.getIdComponent())
                insertFunction("methods",hooks,methodName,getVariantNavigationFunction(methodName,beginElem,elem,destination))
                elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                elemBehaviour[1] = hooks
    return elemBehaviour            

def getTextDestination(elem,allPagesInfo):
    destination = None
    for interaction in elem.getInteractions():
        for action in interaction.actions:
            if(isinstance(action,NavigationAction)):
                destination = getPageById(action.getDestinationID(),allPagesInfo) 
    return destination 

def getKeyEventListenerMounted():
    return ("mountedKeyEventListener","       document.addEventListener('keydown', this.onKeyDown)")
    
def getKeyEventListenerUnMounted():
    return ("unmountedKeyEventListener","       document.removeEventListener('keydown', this.onKeyDown)")

def setKeyCodesMethods(keyCodes,pagename,funtion):
    global keyEvents
    for k in keyCodes:
        if str(k) not in keyEvents[pagename]:
            keyEvents[pagename][str(k)] = [funtion]
        else: keyEvents[pagename][str(k)].append(funtion)

def getKeyEventsFunction(pagename):
    global keyEvents
    function = "    onKeyDown(event){\n"
    for k in keyEvents[pagename]:
        function+=f"        if (event.keyCode == {k})"+"{\n"
        for f in keyEvents[pagename][k]:
            function+=f"            {f}"+"\n"
        function+="     }\n"
    function+="     }"
    if(len(keyEvents[pagename].keys())==0): function=None
    return function

def isAllFrame(l):
    allframe = True
    for el in l:
        if(el[2]!="FRAME"): allframe = False
    if(len(l)==0): return False
    return allframe


def checkcloseinsideComponent(elemenid,allclosePaths):
    inside = False
    r = None
    for pair in allclosePaths:
        if(int(getElemId(pair[0]))+1==int(getElemId(elemenid)) and len(allclosePaths[pair])==1 and allclosePaths[pair][0][2]=="COMPONENT"):
            inside = True
            r= (pair[0],pair[1])
            break
        if((getElemId(pair[0])==getElemId(elemenid) or getElemId(pair[1])==getElemId(elemenid)) and allclosePaths[pair][0][2]=="COMPONENT"):
            inside = True
            r= (pair[0],pair[1])
            break
    return (inside,r)
    
def checkIDinClosepath(id,allclosePaths):
    catchemitevent = False
    pagelevel = False
    r = None
    for pair in allclosePaths:
        for p in allclosePaths[pair]:
            if(getElemId(p[1])==getElemId(id) and p[2]=="COMPONENT"):
                catchemitevent = True   
                if(len(allclosePaths[pair])>=2 and getElemId(allclosePaths[pair][0][0])==getElemId(id) or getElemId(allclosePaths[pair][0][1])==getElemId(id)):
                    pagelevel = True 
                r = (pair[0],pair[1])
    return (catchemitevent,r,pagelevel)    

def checkOverlayTrigger(id):
    global allEmissions
    for pair in allEmissions:
        if(id==pair[0] and isAllFrame(allEmissions[pair])==True):
            return(getElemId(pair[0]),getElemId(pair[1]),True)
        if(getElemId(id)==getElemId(pair[0]) and len(allEmissions[pair])>0 and len(allEmissions[pair])==2 and getElemId(allEmissions[pair][len(allEmissions[pair])-1][3])==getElemId(id)):
            return(getElemId(pair[0]),getElemId(pair[1]),True)
        if(getElemId(id)==getElemId(pair[0]) and len(allEmissions[pair])>0 and len(allEmissions[pair])>=2):
            return(getElemId(pair[0]),getElemId(pair[1]),False)
        if(getElemId(id)==getElemId(pair[0]) and len(allEmissions[pair])>0 and len(allEmissions[pair])<2):
            return(getElemId(pair[0]),getElemId(pair[1]),True)
    return None    

def checkIDinEventspath(id):
    global allEmissions
    isOnPageLevel = False
    for pair in allEmissions:
        for (idx,s) in enumerate(allEmissions[pair]):
            if((getElemId(id)==s[1] or getElemId(id)==s[3]) and s[2]=="INSTANCE"):
                if(idx-1>=0 and "#Page"in allEmissions[pair][idx-1][0]): isOnPageLevel=True
                return (getElemId(pair[0]),getElemId(pair[1]),isOnPageLevel)
    return None    

def processVifs(lista):
    conditions = []
    for (idx,v) in enumerate(lista):
        if("v-if" in v):
            var = v.replace('"',"")
            cond = var.split("=")[1]
            if(cond not in conditions): conditions.append(cond) 
            lista.pop(idx)
    if(len(conditions)>0):
        lista.append('v-if="'+r' && '.join(x for x in conditions)+'"')

def getAnimationVarFunction():
    function = """        setAnimationName(name){
            this.animationName = name
        }"""
    return function

def hasAnimationVar(data):
    has = False
    for x in data:
        for y in x.keys():
            if("animationName"==y):
                has = True
                break
    return has

def getElemId(id):
    elemid = id
    if(str(id).startswith("I")):
        ids = id.split(";")
        elemid = str(ids[len(ids)-1])
    pattern = "[:;]"
    elemid = re.sub(pattern,"",elemid)
    return elemid

def isfromInstance(id):
    return "I" in id

def getFormatedName(name):
    pattern = "[\s\.\-;#,=:]"
    name = re.sub(pattern,"",name)
    return name

def LogicGenerator():
    global shareableEvents,keyEvents,swapDestinationIds, alldata, allEmissions, swapComponentTriggerIds
    shareableEvents = {}
    keyEvents = {}
    swapDestinationIds = []
    swapComponentTriggerIds = {}
    alldata = {}
    allEmissions = {}