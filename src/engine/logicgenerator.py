from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction
from parser.model.OverlayAction import OverlayAction 
from parser.model.CloseAction import CloseAction
from parser.model.ScrollAction import ScrollAction
from parser.model.Mcomponent import Mcomponent
import re

# id: [vars]
shareableHooks = {}

def handleBehaviour(elem,allPagesInfo,isPageRender):
    global shareableHooks
    directives = []
    hooks = {}
    elemBehaviour = [[],None]
    # from component build
    for interaction in elem.getInteractions():
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
                    pattern = "[:;]"
                    destination = action.getDestinationID()
                    destinationid = re.sub(pattern,"",destination)
                    methodName = "changeVisibility"+destinationid
                    insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+destinationid))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                if(isinstance(action,CloseAction) and isPageRender==False and elem.getupperIdComponent()!=None):#verificar se o elemento tem uma acao close e se pertence a um elemento filho de um componente 
                    pattern = "[:;]"
                    destination = action.getDestinationID()
                    destinationid = re.sub(pattern,"",destination)
                    originid = re.sub(pattern,"",elem.getIdElement())
                    # in order to capture the emit signals close-from222310-to22238
                    shareableHooks.setdefault(elem.getupperIdComponent(), []).append(("close-from"+str(originid)+"-to"+str(destinationid),"show"+destinationid+'=false'))
                    methodName = "close"+destinationid
                    insertFunction("methods",hooks,methodName,closeOverlay(methodName,"close-from"+str(originid)+"-to"+str(destinationid)))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
    # HANDLE MENU LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Menu"):
        elemBehaviour = insertMenuLogic(elem,allPagesInfo,hooks,elemBehaviour)
    # HANDLE DROPDOWN LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Dropdown"):
        elemBehaviour = insertDropdownLogic(getElemId(elem.idComponent),hooks,elemBehaviour)
    # HANDLE CHECKBOX LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Checkbox"):
        elemBehaviour = insertCheckboxLogic(getElemId(elem.idComponent),hooks,elemBehaviour)
    # HANDLE FORM LOGIC
    if(isinstance(elem,Mcomponent) and elem.getNameComponent()=="Form"):
        elemBehaviour = insertFormLogic(getElemId(elem.idComponent),elem.inputs,hooks,elemBehaviour)
    # SHOW CONDITIONAL ELEMENTS | from page
    if(isinstance(elem,Mcomponent) and elem.getTypeComponent()=="OVERLAY" and isPageRender==True):
        pattern = "[:;]"
        idcomponent = re.sub(pattern,"",elem.idComponent)
        elemBehaviour[0].append('v-if="show'+idcomponent+'==true"')
        if(elem.getIdComponent() in shareableHooks):
            for hook in shareableHooks[elem.getIdComponent()]:
                elemBehaviour[0].append('@'+hook[0]+'="'+hook[1]+'"')
        elemBehaviour[1] = hooks
    return elemBehaviour

# in order to avoid method duplication in vue pages
def insertFunction(hook,hooks,functioname,function):
    if(not hook in hooks):
        hooks.setdefault(hook, []).append((functioname,function))
    elif((hook in hooks) and (not any(x[0]==functioname for x in hooks[hook]))):
        hooks[hook].append((functioname,function))

def getPageById(id,allPages):
    for pagename in allPages:
        if(allPages[pagename]["id"]==id): return allPages[pagename]["name"]
    return ""

def getNavigationFunction(name,destination):
    function = """\t\t""" + name + "(){" + """
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

def insertFormLogic(idform,inputs,hooks,elemBehaviour):
    elemBehaviour[0] = []
    function = f"""
        const initialValues{idform} = ref("""+'{\n'
    for i in inputs:
        function += "           "+i["name"]+": '',\n"
    function=function[:-1]+"""
        });
    """
    function+=f"""
        const resolver{idform} = ("""+"{ values }) => {"+"""
            const errors = {};
        """
    for i in inputs:
        function += f"""    if (!values.{i["name"]})"""+ "{"+f"""
                errors.{i["name"]} = ["""+"{ message: "+f"""'{i["placeholder"]} is required.'"""+ "}];"+"""
            }
        
        """
    function=function[:-1]+"""
            return {
                errors
            };
        };
    """
    if(not "setup" in hooks):
        hooks.setdefault("setup", []).append(([f"initialValues{idform}",f"resolver{idform}"],function))
    else:
        hooks[hook].append(("",function))
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

def insertDropdownLogic(dropdownid,hooks,elemBehaviour):
    elemBehaviour[0] = []
    
    hooks.setdefault("methods", []).append(('getDropdownOptions'+str(dropdownid),getpopulateDropdownFunction('getDropdownOptions'+str(dropdownid),'allOptionValues'+str(dropdownid),'allOptions'+str(dropdownid))))
    hooks.setdefault("mounted", []).append(('getDropdownOptions'+str(dropdownid),"        this."+'getDropdownOptions'+str(dropdownid)+"();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertCheckboxLogic(checkboxid,hooks,elemBehaviour):
    elemBehaviour[0] = []
    
    hooks.setdefault("methods", []).append(('getCheckboxOptions'+str(checkboxid),getpopulateCheckboxFunction('getCheckboxOptions'+str(checkboxid),'boxesValues'+str(checkboxid),'boxes'+str(checkboxid))))
    hooks.setdefault("mounted", []).append(('getCheckboxOptions'+str(checkboxid),"        this."+'getCheckboxOptions'+str(checkboxid)+"();"))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertScrollBehaviour(elem,action,hooks,elemBehaviour):
    elemBehaviour[0] = []
    elemBehaviour[0].append('v-on:click="'+f"scrollTo{getElemId(elem.getIdElement())}"+'()"')
    hooks.setdefault("methods", []).append((f"scrollTo{getElemId(elem.getIdElement())}",getScrollBehaviourFunction(elem,action)))
    elemBehaviour[1] = hooks
    return elemBehaviour

def insertMenuLogic(elem,allPagesInfo,hooks,elemBehaviour):
    elemBehaviour[0] = []
    hooks.setdefault("methods", []).append((f"selectedItem{getElemId(elem.idComponent)}",getMenuFunction(elem,allPagesInfo,f"selectedItem{getElemId(elem.idComponent)}")))
    elemBehaviour[1] = hooks
    return elemBehaviour


def getElemId(id):
    elemid = id
    if(str(id).startswith("I")):
        ids = id.split(";")
        elemid = str(ids[len(ids)-1])
    pattern = "[:;]"
    elemid = re.sub(pattern,"",elemid)
    return elemid