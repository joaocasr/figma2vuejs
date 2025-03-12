from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction
from parser.model.OverlayAction import OverlayAction 
from parser.model.CloseAction import CloseAction
from parser.model.Mcomponent import Mcomponent
import re

# id: [vars]
shareableHooks = {}

def handleBehaviour(elem,allPagesInfo):
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
                # CLICK-OVERLAY EVENTS
                if(isinstance(action,OverlayAction)):
                    pattern = "[:;]"
                    destination = action.getDestinationID()
                    destinationid = re.sub(pattern,"",destination)
                    methodName = "changeVisibility"+destinationid
                    insertFunction("methods",hooks,methodName,getChangeVisibilityFunction(methodName,"show"+destinationid))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
                if(isinstance(action,CloseAction) and elem.getupperIdComponent()!=None):#verificar se o elemento tem uma acao close e se pertence a um componente 
                    pattern = "[:;]"
                    destination = action.getDestinationID()
                    destinationid = re.sub(pattern,"",destination)
                    originid = re.sub(pattern,"",elem.getIdElement())
                    # in order to capture the emit signals
                    shareableHooks.setdefault(elem.getupperIdComponent(), []).append(("closeFrom"+str(originid)+"To"+str(destinationid),"show"+destinationid+'=false'))
                    methodName = "close"+destinationid
                    insertFunction("methods",hooks,methodName,closeOverlay(methodName,"closeFrom"+str(originid)+"To"+str(destinationid)))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks

    # SHOW CONDITIONAL ELEMENTS | from page
    if(isinstance(elem,Mcomponent) and elem.getTypeComponent()=="OVERLAY"):
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
