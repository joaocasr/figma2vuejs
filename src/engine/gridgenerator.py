import json


def generateGridTemplate(file,allpages):
    template = {}
    with open('/home/joao/figma2vuejs/tests/'+file+'.json') as f:
        template = json.load(f)
    for t in template:
        for p in allpages:
            if(p==t["page"]):
                grid = t["grid-template-areas"]
                for i in grid:
                    for j in i:
                        for e in allpages[p].elements:
                            if(j!="." and e.getName().lower()==j.lower()):
                                e.style.setgridArea(j.lower())

                gridtemplatearea = ""
                for i in grid:
                    gridtemplatearea += '"'
                    for j in i:
                        gridtemplatearea += j + "          "
                
                    gridtemplatearea = gridtemplatearea[:-10]
                    gridtemplatearea = gridtemplatearea + '"\n'
                allpages[p].style.setGridTemplateArea(gridtemplatearea[:-1].split("\n"))

                templatecolumns = " ".join(t["grid-template-columns"])
                templaterows = " ".join(t["grid-template-rows"])
                allpages[p].style.setGridTemplateRows(templaterows)
                allpages[p].style.setGridTemplateColumns(templatecolumns)
                allpages[p].style.setGap(t["gap"])

    #print(allpages[p].style.getGridTemplateArea())
    return allpages
