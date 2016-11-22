#Function to find background level of desired data file
#By Teresa Symons 2016

#Import math and array index adjustment
import numpy as np
from random import randint
from fixindex import fixindex
from scipy import stats

def background(input, length, n):

    #Subarray function returns random subarray of desired nxn size
    def subarray(inputarray, slength):
        a = randint(0,len(inputarray))
        b = randint(0,len(inputarray))
        array = inputarray[a:a+slength, b:b+slength]
        #If random subarray is outside the range of the data array, indices are adjusted
        if array.size == 0:
            #This function takes the proposed edges of a subarray and checks if they fall outside the range of the original array
            #If they do, edges are moved to the edge of the original array
            #Inputs: length of original array (assumed to be square), first row, last row, first column, last column of subarray
            a, b, c, d = fixindex(len(inputarray), a, a+slength, b, b+slength)
            array = inputarray[a:b,c:d]
        return array

    #Determine background sky level
    skyvals = []

    #Take many random subarrays of desired size and find the median value
    for i in range(0,n):
        small = subarray(input,length)
        m = np.nanmedian(small)
        #m = stats.mode(small,axis=None)
        #m = float(m[0])
        skyvals.append(m)

    #Median of all sky values is taken as background level
    back = np.nanmedian(skyvals)
    #back = stats.mode(skyvals,axis=None)
    #back = float(back[0])


    return back, skyvals


