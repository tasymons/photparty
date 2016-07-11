#This script imports a fits file, determines the background level, and finds columns and rows where stars exist
#By Teresa Symons 2016

#Import math, plotting, and fits file handling
import numpy as np
from astropy.io import fits
from background import background
from binsum import binsum
from starlocate import starlocate

#Open image file of choice
image = fits.open('C111221.0077.fits')
#image = fits.open('Ty111221.0145.fits')

#Retrieve data from file
Data = image[0].data

#Compute background sky level by inputting data array,
# nxn size of random subarray to use for sampling,
# and number of desired sampling iterations
back = background(Data,5,100)
print('Sky background level:')
print(back)


#Find midpoint of image data
mid = len(Data)/2
#Take an inset of data that is half of area
inset = Data[round(mid/2):3*round(mid/2),round(mid/2):3*round(mid/2)]
#custom inset for specific chip
inset = inset[0:1000,1000:2000]
#Print data inset
print('Shape of inset array:')
print(np.shape(inset))

#Custom removal of bad columns
#inset[0:1016,1995] = -1
#inset[983:1784,1313:1315] = -1
#custom removal for specific chip inset
inset[0:1000,995]=-1
inset[983:1000,313:315] = -1

#Calculate sky background for specific inset
insetback = background(inset,5,100)
print('Inset background sky level:')
print(insetback)

#Compute summed row and column values for desired array by number of bins
#Will also display plots of summed row and column values
rowsum, colsum = binsum(inset,1)
#Print summed row and column values
print('Summed row and column vectors:')
print(rowsum)
print(colsum)

#Locate values in summed row and column vectors that are greater than desired sigma level above background
#Inputs: Data array, background level variable, desired sigma detection level, summed row vector, summed column vector
starrow, starcol, backsum, std = starlocate(inset,back,100,rowsum,colsum)
print('Summed background value for one row/column:')
print(backsum)
print('Standard deviation of inset:')
print(std)
print('Indices of detected stars:')
print(starrow)
print(starcol)