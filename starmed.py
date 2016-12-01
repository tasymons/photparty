#This function takes lists of row and column indices where all star exist and divides them into sublists by star
#It also returns the number of stars by row and by column, the median pixel values for each star, and paired coordinates for each star
#By Teresa Symons 2016

def starmed(starrow,starcol,inset,mid):
    #Import math
    import numpy as np

    #Divide all star location indices by star
    rowloc = []
    colloc = []
    starr = []
    starc = []
    starr.append(starrow[0])
    starc.append(starcol[0])
    #Start adding star indices to a list
    #If difference between previous and next index is greater than 1, assume new star begins and start new list of indices
    for i in range(1,len(starrow)):
        if starrow[i] == starrow[i-1] + 1:
            starr.append(starrow[i])
        elif starrow[i] == starrow[i-1] + 2:
            starr.append(starrow[i])
        else:
            rowloc.append(starr)
            starr = []
            starr.append(starrow[i])
    rowloc.append(starr)

    for j in range(1,len(starcol)):
        if starcol[j] == starcol[j-1] + 1:
            starc.append(starcol[j])
        elif starcol[j] == starcol[j-1] + 2:
            starc.append(starcol[j])
        else:
            colloc.append(starc)
            starc = []
            starc.append(starcol[j])
    colloc.append(starc)

    #Calculate number of stars (sublists) found by both row and column
    numstarr = len(rowloc)
    numstarc = len(colloc)

    #Find median pixel value of each star by row and column
    #If a star as only one pixel, include that as median value
    rowmed = []
    colmed = []
    for k in range(0,len(rowloc)):
        if len(rowloc[k]) == 1:
            rowmed.append(rowloc[k][0])
        else:
            rowmed.append(int(round(np.nanmedian(rowloc[k]))))
    for k in range(0,len(colloc)):
        if len(colloc[k]) == 1:
            colmed.append(colloc[k][0])
        else:
            colmed.append(int(round(np.nanmedian(colloc[k]))))


    #Check original data array for maximum column value associated with each star's row coordinate
    #If column value appears within +/- one pixel in list of column coordinates, add coordinate pair to list of star coordinates
    starpoints = []
    for i in rowmed:
        j = np.argmax(inset[i, :])
        if j in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j+1 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j-1 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j+2 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j-2 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j+3 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j-3 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j+4 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j-4 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j+5 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)
        elif j-5 in colmed:
            pt = []
            pt.append(i)
            pt.append(j)
            starpoints.append(pt)

    #Adjust coordinates for original image and python indexing
    adjstarpoints = [[y+round(mid/2)+1,x+round(mid/2)+1] for [x,y] in starpoints]

    return rowloc, colloc, numstarr, numstarc, rowmed, colmed, starpoints, adjstarpoints
