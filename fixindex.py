#This function adjusts edges for a subarray when they fall outside the range of existing data
#Inputs include the length of the data array (assumed to be square), beginning row of subarray, ending row of subarray,
#beginning column of subarray, and ending column of subarray
#By Teresa Symons 2016

def fixindex(length, ra, rb, ca, cb):
    test = [ra, rb, ca, cb]
    new = []

    #For each of the 4 indices, check if any fall outside the array
    #If they do, replace them with the edge of the array
    for i in test:
        if i < 0:
            newindex = 0
        elif i > length:
            newindex = length
        else:
            newindex = i
        new.append(newindex)

    #If these adjustments result in either dimension being only one row or column wide, adjust so that the second index
    #from the edge is used as an inside boundary
    if new[0] == new[1]:
        if new[0] == 0:
            new[1] = 1
        elif new[0] == length:
            new[0] = length - 1
    if new[2] == new[3]:
        if new[2] == 0:
            new[3] = 1
        elif new[2] == length:
            new[2] = length - 1

    #Return new, adjusted indices within the range of the data array
    return new[0], new[1], new[2], new[3]