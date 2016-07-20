#Function to find background level of desired data file
#By Teresa Symons 2016

#Import math
import numpy as np
from random import randint
def background(input, length, n):

    #subarray function returns random subarray of desired nxn size
    def subarray(inputarray, slength):
        a = randint(0,len(inputarray))
        b = randint(0,len(inputarray))
        array = inputarray[a:a+slength, b:b+slength]
        return array

    #Determine background sky level
    skyvals = []

    #Take many random subarrays of desired size and find the median value
    for i in range(0,n):
        small = subarray(input,length)
        m = np.nanmedian(small)
        skyvals.append(m)

    #Median of all sky values is taken as background level
    back = np.nanmedian(skyvals)

    return back


