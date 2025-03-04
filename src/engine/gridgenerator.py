grid = []
nrrows = 0
nrcolumns = 0

def generateGridTemplate(rows,columns,allpages):
    global grid,nrrows,nrcolumns
    nrrows = int(rows)
    nrcolumns = int(columns)
    grid = [["." for _ in range(int(nrcolumns))] for _ in range(int(nrrows))]
    for p in allpages:
        for e in allpages[p].elements:
            (columnstart,columnend,rowstart,rowend) = getTemplatePosition(allpages[p].style.height,
                            allpages[p].style.width,
                            e.style.height,
                            e.style.width,
                            e.style.x,
                            e.style.y,
                            e.getName())
            e.style.setgridArea(e.getName())
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
        allpages[p].style.setGap("20")

    #print(allpages[p].style.getGridTemplateArea())
    return allpages

def getTemplatePosition(pageheight,pagewidth,height,width,posx,posy,name):
    global grid,nrrows,nrcolumns
    columnstart = int((posx / pagewidth) * nrcolumns)
    rowstart = int((posy / pageheight) * nrrows )
    columnend = int(min((((width / pagewidth) * nrcolumns) + columnstart ),nrcolumns-1))
    rowend = int(min((((height / pageheight) * nrrows) + rowstart  ),nrrows-1))
    #print(name)
    #print((columnstart,columnend),(rowstart,rowend))


    for i in range(rowstart,rowend+1):
        for j in range(columnstart,columnend+1):
            if(grid[i][j]=='.'): grid[i][j] = name
            else:
                pass
    return (columnstart,columnend,rowstart,rowend)