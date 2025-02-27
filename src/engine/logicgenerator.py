from parser.model.InteractionElement import InteractionElement
from parser.model.NavigationAction import NavigationAction

def handleBehaviour(elem,cssclass,allPagesInfo):
    directives = []
    hooks = {}
    elemBehaviour = [[],None]
    for interaction in elem.getInteractions():
        if(interaction.getInteractionType()==InteractionElement.Interaction.ONCLICK):
            for action in interaction.actions:
                if(isinstance(action,NavigationAction)):
                    destination = getPageById(action.getDestinationID(),allPagesInfo) 
                    methodName = "goto"+destination
                    hooks.setdefault("methods", []).append(getNavigationFunction(methodName,destination)) 
                    elemBehaviour[0].append('v-on:click="'+methodName+'()"')
                    elemBehaviour[1] = hooks
    return elemBehaviour


def getPageById(id,allPages):
    for pagename in allPages:
        if(allPages[pagename]["id"]==id): return allPages[pagename]["name"]
    return ""

def getNavigationFunction(name,destination):
    function = """\t\t""" + name + "(){" + """
            this.$router.push({path:"/""" + destination.lower() + """"});
        }""" 
    return function
    