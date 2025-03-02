from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction

def handleBehaviour(elem,allPagesInfo):
    directives = []
    hooks = {}
    elemBehaviour = [[],None]
    for interaction in elem.getInteractions():
        if(interaction.getInteractionType()==InteractionElement.Interaction.ONCLICK):
            for action in interaction.actions:
                if(isinstance(action,NavigationAction)):
                    destination = getPageById(action.getDestinationID(),allPagesInfo) 
                    methodName = "goto"+destination
                    insertFunction("methods",hooks,methodName,getNavigationFunction(methodName,destination))
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
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
    