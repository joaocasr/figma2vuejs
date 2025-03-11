from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction
from parser.model.Mcomponent import Mcomponent
import re

def handleBehaviour(elem,allPagesInfo,pageVariables):
    directives = []
    hooks = {}
    elemBehaviour = [[],None]
    # CLICK-NAVIGATION EVENTS
    for interaction in elem.getInteractions():
        if(interaction.getInteractionType()==InteractionElement.Interaction.ONCLICK):
            for action in interaction.actions:
                if(isinstance(action,NavigationAction)):
                    destination = getPageById(action.getDestinationID(),allPagesInfo) 
                    methodName = "goto"+destination
                    insertFunction("methods",hooks,methodName,getNavigationFunction(methodName,destination))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
    # SHOW CONDITIONAL ELEMENTS
    if(isinstance(elem,Mcomponent) and elem.getTypeComponent()=="OVERLAY"):
        pattern = "[:;]"
        idcomponent = re.sub(pattern,"",elem.idComponent)
        myvar = getVisibilityVar(pageVariables,idcomponent)
        if(myvar!=None):
            elemBehaviour[0].append('v-if="'+myvar+'==true"')
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

def getVisibilityVar(pageVariables,idComponent):
    var = None
    print(pageVariables)
    for x in pageVariables:
        for k,v in x.items():
            if("show" in k and k.split("show")[1]==idComponent):
                var = k
    return var


def getNavigationFunction(name,destination):
    function = """\t\t""" + name + "(){" + """
            this.$router.push({path:"/""" + destination.lower() + """"});
        }""" 
    return function
    
def getChangeVisibilityFunction(name,variable):
    function = """\t\t""" + name + "(){" + """
            """ + variable +  "= !"+ variable + """;
        }""" 
    return function
