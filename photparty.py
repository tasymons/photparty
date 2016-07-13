#The goal of this script is to read a fits file, locate stars, and return magnitudes for those stars
#Background sky level is calculated using random median sampling of square arrays
#A specific inset of the data array is taken if desired
#Pixel values are summed row-wise and column-wise (optionally binned) and background level is used to determine which rows and columns contain stars
#A list of matched star coordinates is prepared
#Star magnitudes are obtained using square apertures after being background subtracted for the region specific to the star
#By Teresa Symons 2016

#Import math, plotting, extraneous functions, and fits file handling:
import numpy as np
import os
from astropy.io import fits
from background import background
from binsum import binsum
from starlocate import starlocate
from starmed import starmed
from starphot import starphot
import matplotlib.pylab as plt


files = [line.rstrip() for line in open('files.txt')]
for i in files:
    (name, ext) = os.path.splitext(i)
    newname = name+'mag.txt'
    f = open(newname,'w')
    #Open image file of choice:
    #image = fits.open('C111221.0077.fits')
    image = fits.open(i)

    #Retrieve data and exposure time from file:
    Data = image[0].data
    etime = image[0].header['EXPTIME']

    #Compute background sky level through random median sampling:
    #Inputs: data array, nxn size of random subarray to use for sampling, and number of desired sampling iterations
    back = background(Data,5,100)
    print('Sky background level:',file = f)
    print(back,file = f)

    #Create desired inset of total data array:
    #Find midpoint of image data
    mid = len(Data)/2
    #Take an inset of data that is half of area
    inset = Data[round(mid/2):3*round(mid/2),round(mid/2):3*round(mid/2)]
    #Custom inset for specific chip
    #inset = inset[0:1000,1000:2000]
    #Print data inset
    inset = Data
    print('Shape of inset array:', file = f)
    print(np.shape(inset), file = f)

    #Custom removal of bad columns:
    #inset[0:1016,1995] = -1
    #inset[983:1784,1313:1315] = -1
    #Custom removal for specific chip inset
    #inset[0:1000,995]=-1
    #inset[983:1000,313:315] = -1

    #Blanket removal of bad pixels
    inset[inset>45000] = 0
    inset[inset<-100] = 0

    #Calculate sky background for specific inset:
    #Inputs: inset data array, nxn size of random subarray used for sampling, number of desired sampling iterations
    insetback = background(inset,5,100)
    print('Inset background sky level:',file = f)
    print(insetback,file = f)

    #Compute summed row and column values for desired array by number of bins:
    #Will also display plots of summed row and column values before program continues
    #Figures must be closed for program to procede
    #Inputs: inset data array, number of bins desired
    rowsum, colsum = binsum(inset,1)
    #Print summed row and column values
    #print('Summed row and column vectors:', file = f)
    #print(rowsum, file = f)
    #print(colsum, file = f)

    #Locate values in summed row and column vectors that are greater than desired sigma level above background:
    #Inputs: Data array, background level variable, desired sigma detection level, summed row vector, summed column vector
    starrow, starcol, backsum, std = starlocate(inset,insetback,100,rowsum,colsum)
    print('Summed background value for one row/column:', file = f)
    print(backsum, file = f)
    print('Standard deviation of inset:',file = f)
    print(std, file = f)
    #print('Indices of detected stars:', file = f)
    #print(starrow, file = f)
    #print(starcol, file = f)

    #Take indices of detected star pixels and divide into sublists by individual star:
    #Return sublists of star indices, number of stars, and median pixel of each star
    #Pair star center row with star center column and return total number of pairs found
    #Inputs: vectors containing indices of detected star pixels for row and column and inset data array
    rowloc, colloc, numstarr, numstarc, rowmed, colmed, starpoints = starmed(starrow,starcol,inset)
    #print('Indices of detected stars divided into sublist by star:', file = f)
    #print(rowloc, file = f)
    #print(colloc, file = f)
    print('Number of stars found by row/column:', file = f)
    print(numstarr, file = f)
    print(numstarc, file = f)
    print('Median pixel of each star by row/column:', file = f)
    print(rowmed, file = f)
    print(colmed, file = f)
    print('Paired indices of star centers:',file = f)
    print(starpoints,file = f)
    print('Total number of stars found:',file = f)
    print(len(starpoints),file = f)

    #Take list of star coordinates and find summed pixel values within a square aperture of desired size:
    #Also find background values for each star and subtract them from star values
    #Convert background-subtracted star values into fluxes and then magnitudes
    #Inputs: half-width of nxn square aperture, inset data array, vector containing star coordinates, exposure time
    boxsum, starback, backsub, flux, mags = starphot(25, inset, starpoints, etime)
    print('Pixel sums for boxes around each star:', file = f)
    print(boxsum, file = f)
    print('Background values for each star:', file = f)
    print(starback, file = f)
    print('Background subtracted star values:', file = f)
    print(backsub, file = f)
    print('Flux of stars:', file = f)
    print(flux, file = f)
    print('Magnitudes for each star:',file = f)
    print(mags,file = f)

    # Plot summed row and column values
    plt.plot(rowsum)
    plt.title('Summed Rows')
    plt.show()
    plt.plot(colsum)
    plt.title('Summed Columns')
    plt.show()






