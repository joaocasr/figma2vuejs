from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction
from parser.model.OverlayAction import OverlayAction 
from parser.model.CloseAction import CloseAction
from parser.model.ScrollAction import ScrollAction
from parser.model.ChangeAction import ChangeAction
from parser.model.Mcomponent import Mcomponent
from parser.model.Melement import Melement
from parser.model.ContainerElement import ContainerElement
import re
import itertools

# id: [vars]
shareableEvents = {}

def handleBehaviour(elem,allPagesInfo,pagename,isPageRender,allvariants):
    global shareableEvents
    directives = []
    hooks = {}
    elemBehaviour = [[],None]
    #if(isinstance(elem,Mcomponent)): currentId = elem.getIdComponent()
    #else: currentId = elem.getIdElement()
    # from component build
    for interaction in elem.getInteractions():
        if(interaction.getInteractionType()==InteractionElement.Interaction.ONHOVER):
            for action in interaction.actions:
                if(isinstance(action,OverlayAction)):
                    destinationid = getElemId(action.getDestinationID())
                    methodName = "changeVisibility"+destinationid
                    elemBehaviour[0].extend(['@mouseenter="'+methodName+'"','@mouseleave="'+methodName+'"'])
                    if(isinstance(elem,Melement) and isfromInstance(elem.getIdElement()) and elem.getupperIdComponent()!=None):
                        shareableEvents.setdefault(elem.getupperIdComponent(), []).append(("show-from"+getElemId(elem.getIdElement())+"-to"+getElemId(action.getDestinationID()),"show"+getElemId(action.getDestinationID())+'=true',''))
                        shareableEvents.setdefault(action.getDestinationID(), []).append((None,None,'v-if="show'+getElemId(action.getDestinationID())+'==true"'))
                        insertFunction("methods",hooks,methodName,showOverlayonHover(methodName,"show"+destinationid))
                        elemBehaviour[1] = hooks
                    
                    elemBehaviour[1] = hooks
        if(interaction.getInteractionType()==InteractionElement.Interaction.ONCLICK):
            for action in interaction.actions:
                # CLICK-NAVIGATION EVENTS
                if(isinstance(action,NavigationAction)):
                    destination = getPageById(action.getDestinationID(),allPagesInfo) 
                    methodName = "goto"+destination
                    insertFunction("methods",hooks,methodName,getNavigationFunction(methodName,destination))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                # SCROLL EVENTS
                if(isinstance(action,ScrollAction)):
                    elemBehaviour = insertScrollBehaviour(elem,action,hooks,elemBehaviour)
                # CLICK-OVERLAY EVENTS
                if(isinstance(action,OverlayAction)):
                    destinationid = getElemId(action.getDestinationID())
                    methodName = "changeVisibility"+destinationid
                    insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+destinationid))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                if(isinstance(action,CloseAction) and isPageRender==False and elem.getupperIdComponent()!=None):#verificar se o elemento tem uma acao close e se pertence a um elemento filho de um componente 
                    destinationid = getElemId(action.getDestinationID())
                    originid = getElemId(elem.getIdElement())
                    # in order to capture the emit signals close-from222310-to22238
                    shareableEvents.setdefault(elem.getupperIdComponent(), []).append(("close-from"+str(originid)+"-to"+str(destinationid),"show"+destinationid+'=false','v-if="show'+destinationid+'==true"'))
                    methodName = "close"+destinationid
                    insertFunction("methods",hooks,methodName,closeOverlay(methodName,"close-from"+str(originid)+"-to"+str(destinationid)))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
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
        elemBehaviour = insertDropdownLogic(getElemId(elem.idComponent),hooks,elemBehaviour)
    # HANDLE CHECKBOX LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Checkbox"):
        elemBehaviour = insertCheckboxLogic(getElemId(elem.idComponent),hooks,elemBehaviour)
    # HANDLE FORM LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Form"):
        elemBehaviour = insertFormLogic(getElemId(elem.idComponent),elem.inputs,hooks,elemBehaviour)
    # HANDLE SLIDER LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Slider"):
        elemBehaviour = insertSliderLogic(getElemId(elem.idComponent),hooks,elemBehaviour)
    # HANDLE CONDITIONAL VISIBLE ELEMENTS
    if(elem.gethascondvisib()==True):
        elemBehaviour[0].append('v-show="show'+getElemId(elem.getIdElement())+'==true"')
    # SHOW CONDITIONAL ELEMENTS | from page
    if(isinstance(elem,Mcomponent) and isPageRender==True):
        idcomponent = getElemId(elem.idComponent)
        if(elem.getIdComponent() in shareableEvents):
            for hook in shareableEvents[elem.getIdComponent()]:
                elemBehaviour[0].append(hook[2])
                if(hook[0]!=None and hook[1]!=None): elemBehaviour[0].append('@'+hook[0]+'="'+hook[1]+'"')
        elemBehaviour[1] = hooks
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
    function = """\t""" + name + "(){" + """
            this.$router.push({path:"/""" + destination.lower() + """"});
        }""" 
    return function
    
def getChangeVisibilityFunction(name,variable):
    function = """\t\t""" + name + "(){" + """
            this.""" + variable +  """ = true;
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
            this.$refs.ref{getElemId(action.getDestinationID())}?.scrollIntoView("""+"{ behavior: 'smooth' });"+"""
        }""" 
    return function

def insertSliderLogic(idSlider,hooks,elemBehaviour):
    sliderFunction = f"""slider{idSlider}"""+"""(newvalue,oldvalue){
            const toastStore = useToastStore();
            let message = "Slider value: "+newvalue            
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
        if(data.valid==true){
            message = "The form was successfully submited!"            
            toastStore.showSuccess(message);
        }
        if(data.valid==false){
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
            bodyfunction += f'this.$router.push('+'{path:"/' + destination.lower() + '"});\n'
            function =f"""        {functionname}()"""+"{"+f"""
               {bodyfunction}"""+"""
            }"""
    return function

def showOverlayonHover(name,variable):
    function = """\t\t""" + name + "(){" + """
            this.""" + variable +  """ = !this.""" + variable +";"+"""
        }""" 
    return function

def insertDropdownLogic(dropdownid,hooks,elemBehaviour):
    
    hooks.setdefault("methods", []).append(('getDropdownOptions'+str(dropdownid),getpopulateDropdownFunction('getDropdownOptions'+str(dropdownid),'allOptionValues'+str(dropdownid),'allOptions'+str(dropdownid))))
    hooks.setdefault("mounted", []).append(('getDropdownOptions'+str(dropdownid),"        this."+'getDropdownOptions'+str(dropdownid)+"();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertCheckboxLogic(checkboxid,hooks,elemBehaviour):
    
    hooks.setdefault("methods", []).append(('getCheckboxOptions'+str(checkboxid),getpopulateCheckboxFunction('getCheckboxOptions'+str(checkboxid),'boxesValues'+str(checkboxid),'boxes'+str(checkboxid))))
    hooks.setdefault("mounted", []).append(('getCheckboxOptions'+str(checkboxid),"        this."+'getCheckboxOptions'+str(checkboxid)+"();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertScrollBehaviour(elem,action,hooks,elemBehaviour):
    elemBehaviour[0].append('v-on:click="'+f"scrollTo{getElemId(elem.getIdElement())}"+'()"')
    hooks.setdefault("methods", []).append((f"scrollTo{getElemId(elem.getIdElement())}",getScrollBehaviourFunction(elem,action)))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertMenuLogic(elem,allPagesInfo,hooks,elemBehaviour):
    hooks.setdefault("methods", []).append((f"selectedItem{getElemId(elem.idComponent)}",getMenuFunction(elem,allPagesInfo,f"selectedItem{getElemId(elem.idComponent)}")))
    elemBehaviour[1] = hooks
    return elemBehaviour

def handleScrollBehaviour(elem,hooks,elemBehaviour):
    mountedFunction = f'        window.addEventListener("mouseup", this.onMouseUp{getElemId(elem.idElement)});'
    destroyedFunction = f'      window.removeEventListener("mouseup", this.onMouseUp{getElemId(elem.idElement)});'

    hooks.setdefault("mounted", []).append((f"getMountedFunction{getElemId(elem.idElement)}",mountedFunction))
    hooks.setdefault("destroyed", []).append((f"getDestroyedFunction{getElemId(elem.idElement)}",destroyedFunction))
    
    mousedownFunction = f'''        onMouseDown{getElemId(elem.idElement)}(ev)'''+'''{
            this.cursorPos = [ev.pageX, ev.pageY];
            this.isDragging = true;

            '''+f'window.addEventListener("mousemove", this.onMouseHold{getElemId(elem.idElement)});'+'''
        }'''
    hooks.setdefault("methods", []).append((f"onMouseDown{getElemId(elem.idElement)}",mousedownFunction))
    
    mouseupFunction = f'''        onMouseUp{getElemId(elem.idElement)}(ev)'''+'''{
            '''+f'window.removeEventListener("mousemove", this.onMouseHold{getElemId(elem.idElement)});'+f'''
            this.isDragging = false;'''+'''
        }'''
    hooks.setdefault("methods", []).append((f"onMouseUp{getElemId(elem.idElement)}",mouseupFunction))
    transition = ""
    if(elem.style.getOverflowDirection()=="HORIZONTAL"):
        transition = "left: -delta[0]"
    else:
        transition = "top: -delta[1]"        
    mouseholdFunction = f'''        onMouseHold{getElemId(elem.idElement)}(ev)'''+'''{
            ev.preventDefault();

            requestAnimationFrame(() => {
                    const delta = [ev.pageX - this.cursorPos[0], ev.pageY - this.cursorPos[1]];

                    this.cursorPos = [ev.pageX, ev.pageY];

                    '''+f'''if (!this.$refs.ref{getElemId(elem.idElement)}) return;
                    this.$refs.ref{getElemId(elem.idElement)}.scrollBy('''+'''{
                    '''+transition+'''});
            });
        }'''
    hooks.setdefault("methods", []).append((f"onMouseHold{getElemId(elem.idElement)}",mouseholdFunction))
    elemBehaviour[1] = hooks
    return elemBehaviour

def getDatatableValuesFunction(tableid,values):
    function = """\t\tgetDatatableValues""" + str(tableid) + "(){" + """
            this.tablevalues""" + str(tableid) +f""" = {values};"""+"""
        }""" 
    return function

def insertTableLogic(elem,allPagesInfo,hooks,elemBehaviour):
    hooks.setdefault("methods", []).append((f'getDatatableValues{getElemId(elem.idComponent)}',getDatatableValuesFunction(getElemId(elem.idComponent),elem.values)))
    hooks.setdefault("mounted", []).append((f'getDatatableValues{getElemId(elem.idComponent)}',f"        this.getDatatableValues{getElemId(elem.idComponent)}();"))
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

def getVariantVariables(elem,id):
    return f"""            this.selectedClass{id} = this.componentclass{id};
            this.currentVariant{id} = '{getFormatedName(elem.getNameComponent()).lower()}';"""
    
def declareMountedVariables(elem,hooks,elemBehaviour):
    hooks.setdefault("mounted", []).append((f'getVariantVariables{getElemId(elem.idComponent)}',getVariantVariables(elem,getElemId(elem.idComponent))))
    elemBehaviour[1] = hooks
    return elemBehaviour
    
def getComponentVariant(id,variants):
    for v in variants:
        for c in v.variantComponents:
            if(id==c.idComponent):
                return c
    return None

def changeToHoveredFunction(elem,destelem):
    function = """\t""" + f"changeToHovered{getElemId(elem.idComponent)}()"+"{" + f"""
            this.selectedClass{getElemId(elem.idComponent)}=this.componentclass{getElemId(destelem.idComponent)};
            this.currentVariant{getElemId(elem.idComponent)}= '{getFormatedName(destelem.getNameComponent()).lower()}'
"""+"\t}"
    return function

def changeToDefaultFunction(elem,destelem):
    function = """\t""" + f"changeToDefault{getElemId(elem.idComponent)}()"+"{" + f"""
            this.selectedClass{getElemId(elem.idComponent)}=this.componentclass{getElemId(elem.idComponent)};
            this.currentVariant{getElemId(elem.idComponent)}= '{getFormatedName(elem.getNameComponent()).lower()}'
"""+"\t}"
    return function

def changeVariantFunction(elem,destinations):
    elsecond = False
    elsecondst = "if"
    function = """\t""" + f"changeVariant{getElemId(elem.idComponent)}()"+"{" 
    for variant in destinations: 
        if(elsecond==True): elsecondst = "else if"      
        function+=f"""
        {elsecondst}(this.selectedClass{getElemId(elem.idComponent)}==this.componentclass{getElemId(variant[0].idComponent)})"""+"{"+f"""
                this.selectedClass{getElemId(elem.idComponent)}=this.componentclass{getElemId(variant[1].idComponent)};
                this.currentVariant{getElemId(elem.idComponent)}= '{getFormatedName(variant[1].getNameComponent()).lower()}'
"""+"""\t}"""
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
                    if(destelem.idComponent==beginid): return destinations
                    return getDestinations(beginid,destelem,variants,destinations)
                
def getVariantNavigationFunction(methodName,beginElem,currentElem,destination):
    if(beginElem==None and currentElem!=None): beginElem = currentElem  
    function = """\t""" + methodName + "(){" + f"""
            if(this.selectedClass{getElemId(beginElem.idComponent)}==this.componentclass{getElemId(currentElem.idComponent)})"""+"{"+"""
                this.$router.push({path:"/""" + destination.lower() + """"});
            }
    \t}""" 
    return function

def handleVariants(elem,variants,hooks,elemBehaviour,allPagesInfo,beginElem=None):
    for i in elem.interactions:
         for a in i.actions:
            destelem = getComponentVariant(a.destinationID,variants)
            if(isinstance(a,ChangeAction) and i.getInteractionType()==InteractionElement.Interaction.ONHOVER):
                elemBehaviour[0].extend([f'@mouseover="changeToHovered{getElemId(elem.idComponent)}"',f'@mouseleave="changeToDefault{getElemId(elem.idComponent)}"'])
                hooks.setdefault("methods", []).append((f'changeToHovered{getElemId(elem.idComponent)}',changeToHoveredFunction(elem,destelem)))
                hooks.setdefault("methods", []).append((f'changeToDefault{getElemId(elem.idComponent)}',changeToDefaultFunction(elem,destelem)))
                if(len(destelem.interactions)>0):
                    handleVariants(destelem,variants,hooks,elemBehaviour,allPagesInfo,elem)
                elemBehaviour[1] = hooks
            if(isinstance(a,ChangeAction) and i.getInteractionType()==InteractionElement.Interaction.ONCLICK and len(destelem.interactions)>=0):
                destinations = getDestinations(elem.idComponent,elem,variants,[])
                elemBehaviour[0].append(f'@click="changeVariant{getElemId(elem.idComponent)}"')
                hooks.setdefault("methods", []).append((f'changeVariant{getElemId(elem.idComponent)}',changeVariantFunction(elem,destinations)))
                elemBehaviour[1] = hooks
            if(isinstance(a,NavigationAction) and i.getInteractionType()==InteractionElement.Interaction.ONCLICK):
                destination = getPageById(a.getDestinationID(),allPagesInfo) 
                methodName = "goto"+destination
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