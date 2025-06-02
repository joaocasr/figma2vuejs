from utils.tools import getName

grid = []
nrrows = 0
nrcolumns = 0

def generateGridTemplate(allpages, nr_rows, nr_columns):
    global grid,nrrows,nrcolumns

    nrrows = int(nr_rows)
    nrcolumns = int(nr_columns)
    grid = [['.' for j in range(int(nr_columns))] for k in range(int(nr_rows))]

    for p in allpages:
        for e in allpages[p].elements:
            name = getName(e)
            getTemplatePosition(allpages[p].style.height,
                            allpages[p].style.width,
                            e.style.height,
                            e.style.width,
                            e.style.x,
                            e.style.y,
                            name)
            e.style.setgridArea(name)
        gridtemplatearea = ""
        for i in range(0,nrrows):
            gridtemplatearea += '"'
            for j in range(0,nrcolumns):
                gridtemplatearea += grid[i][j] + "          "
            gridtemplatearea = gridtemplatearea[:-10]
            gridtemplatearea = gridtemplatearea + '"\n'
        allpages[p].style.setGridTemplateArea(gridtemplatearea[:-1].split("\n"))
        templaterows = ""
        templatecolumns = ""
        for c in range(0,nrcolumns):
            templatecolumns += "1fr "
        for r in range(0,nrrows):
            templaterows += "1fr "
        allpages[p].style.setGridTemplateRows(templaterows)
        allpages[p].style.setGridTemplateColumns(templatecolumns)
        allpages[p].style.setGap("20px")
    #print(allpages[p].style.getGridTemplateArea())
    return allpages

def getTemplatePosition(pageheight,pagewidth,height,width,posx,posy,name):
    global grid,nrrows,nrcolumns

    if(pageheight==0): pageheight+=10
    if(pagewidth==0): pagewidth+=10

    columnstart = int((posx / pagewidth) * nrcolumns)
    rowstart = int((posy / pageheight) * nrrows )
    columnend = int(min(((width / pagewidth) * nrcolumns) + columnstart,nrcolumns-1)) 
    rowend = int(min((((height / pageheight) * nrrows) + rowstart  ),nrrows-1))

    for i in range(rowstart,rowend+1):
        for j in range(columnstart,columnend+1):
            if(grid[i][j]=='.'): grid[i][j] = name
            else:
                pass
        
    return (columnstart,columnend,rowstart,rowend)