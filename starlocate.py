#This function takes a desired data array, computed background level, desired sigma detection level, and summed row
#and column vectors and locates indices in those vectors where the summed value is the desired sigma level above the
#computed summed background level
#By Teresa Symons 2016

def starlocate(array,background,sigma,summedrows,summedcols):
    #Import math
    import numpy as np

    #Calculate estimated background level summed over whole row/column
    backsum = background*len(array)

    starrow = []
    starcol = []

    #Calculate standard deviation of desired array
    std = np.std(array)

    #For both the summed row and column values, locate values greater than n sigma above background level
    for k in range(0,len(summedrows)):
        if summedrows[k]>sigma*std+np.abs(backsum):
            starrow.append(summedrows.index(summedrows[k]))
        if summedcols[k]>sigma*std+np.abs(backsum):
            starcol.append(summedcols.index(summedcols[k]))

    return starrow, starcol, backsum, std, sigma