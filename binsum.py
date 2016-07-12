#This is a function that takes a desired data array and number of bins and bins the data by both row and column,
#summing for each bin on each axis
#By Teresa Symons 2016

#Import math and plotting
import numpy as np
import matplotlib.pylab as plt

def binsum(array,bins):

    #For a desired bin number, bin data and sum row and column values in bins
    rowsum = []
    colsum = []
    binnum = int(round(len(array)/bins))
    for j in range(0,binnum):
        rowsum.append(np.sum(array[j*bins:j*bins+bins,:]))
        colsum.append(np.sum(array[:,j * bins:j * bins + bins]))

    #Plot summed row and column values
    # plt.plot(rowsum)
    # plt.title('Summed Rows')
    # plt.show()
    # plt.plot(colsum)
    # plt.title('Summed Columns')
    # plt.show()

    return rowsum, colsum