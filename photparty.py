#The goal of this script is to read fits files, locate stars, and return magnitudes for those stars
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
from astropy.table import Table
import matplotlib.pylab as plt

#Define path to folder containing files to be run
#All fits or fit files will be automatically included
#Output files will also be placed into this folder
path = '/Users/Andromeda/PycharmProjects/untitled/files'

#Alternatively, run list of files in a specified text file
#In this case files will output to the location of the main script
#files = [line.rstrip() for line in open('files.txt')]

#Suppress or display plots of summed rows/columns with detection level (on or off)
plotting = 'off'

#Create list of files to run based on defined path, ignoring all files that are not fit or fits
files = [f for f in os.listdir(path) if any([f.endswith('fit'), f.endswith('fits')]) if not f.startswith('.')]
#Run for all files in list
for i in files:
    #Define names for output files based on names of original files
    (name, ext) = os.path.splitext(i)
    newname = path+'/'+name+'mag.txt'
    datname = path+'/'+name+'dat.txt'
    #Open output files
    f = open(newname,'w')
    df = open(datname,'w')
    #Open fits file
    filepath = path+'/'+i
    image = fits.open(filepath)

    #Retrieve data, exposure time, airmass, and filter from fits file:
    Data = image[0].data
    etime = image[0].header['EXP_TIME']
    print('Exposure time:',file = f)
    print(etime, file = f)
    filter = image[0].header['FILTER']
    print('Filter:',file = f)
    print(filter, file = f)
    airmass = image[0].header['AIRMASS']
    print('Airmass:', file = f)
    print(airmass, file = f)

    #Compute background sky level through random median sampling:
    #Inputs: data array, nxn size of random subarray to use for sampling, and number of desired sampling iterations
    back = background(Data,5,1000)
    print('Sky background level:',file = f)
    print(back,file = f)

    #Create desired inset of total data array:
    #Find midpoint of image data
    mid = len(Data)/2
    #Take an inset of data that is half of area
    inset = Data[round(mid/2):3*round(mid/2),round(mid/2):3*round(mid/2)]
    #Custom inset for specific chip
    #inset = inset[0:1000,1000:2000]
    #Use entire data array as inset
    #inset = Data
    #Print data inset size
    print('Shape of inset array:', file = f)
    print(np.shape(inset), file = f)

    #Custom removal of bad columns:
    #inset[0:1016,1995] = -1
    #inset[983:1784,1313:1315] = -1
    #Custom removal for specific chip inset
    #inset[0:1000,995]=-1
    #inset[983:1000,313:315] = -1
    # inset[:,1102] = 0
    # inset[:,2047] = 0

    #Blanket removal of bad pixels above 45000 and 3*standard deviation below 0:
    inset[inset>45000] = 0
    std = np.std(inset)
    inset[inset<-3*std] = 0

    #Calculate sky background for specific inset:
    #Inputs: inset data array, nxn size of random subarray used for sampling, number of desired sampling iterations
    insetback = background(inset,5,1000)
    print('Inset background sky level:',file = f)
    print(insetback,file = f)

    #Compute summed row and column values for desired array by number of bins:
    #Inputs: inset data array, number of bins desired
    rowsum, colsum = binsum(inset,1)
    #Print summed row and column values
    #print('Summed row and column vectors:', file = f)
    #print(rowsum, file = f)
    #print(colsum, file = f)

    #Locate values in summed row and column vectors that are greater than desired sigma level above background:
    #Inputs: Data array, background level variable, desired sigma detection level, summed row vector, summed column vector
    starrow, starcol, backsum, std, sigma = starlocate(inset,insetback,100,rowsum,colsum)
    print('Summed background value for one row/column:', file = f)
    print(backsum, file = f)
    print('Standard deviation of inset:',file = f)
    print(std, file = f)
    print('Detection level in sigma:', file = f)
    print(sigma, file = f)
    print('Indices of detected stars:', file = f)
    print(starrow, file = f)
    print(starcol, file = f)

    #Take indices of detected star pixels and divide into sublists by individual star:
    #Return sublists of star indices, number of stars, and median pixel of each star
    #Pair star center row with star center column and return total number of pairs found
    #Inputs: vectors containing indices of detected star pixels for row and column and inset data array
    rowloc, colloc, numstarr, numstarc, rowmed, colmed, starpoints, adjstarpoints = starmed(starrow,starcol,inset,mid)
    print('Indices of detected stars divided into sublist by star:', file = f)
    print(rowloc, file = f)
    print(colloc, file = f)
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
    print('Coordinates of stars (x,y):', file = f)
    print(adjstarpoints,file = f)

    #Take list of star coordinates and find summed pixel values within a square aperture of desired size:
    #Also find background values for each star and subtract them from star values
    #Convert background-subtracted star values into fluxes and then magnitudes
    #Inputs: half-width of nxn square aperture, inset data array, vector containing star coordinates, exposure time
    boxsum, starback, backsub, flux, mags, hw = starphot(25, inset, starpoints, etime)
    print('Width/Height of boxes:', file = f)
    print(hw*2, file = f)
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

    #Output data table to file:
    n = len(mags)
    tname = [i]*n
    tfilter = [filter]*n
    tairmass = [airmass]*n
    tetime = [etime]*n
    x = [x for [x,y] in adjstarpoints]
    y = [y for [x,y] in adjstarpoints]
    t = Table([tname, tfilter, tairmass, tetime, x, y, mags], names=('File_Name', 'Filter', 'Airmass', 'Exposure_Time', 'X', 'Y', 'Magnitude'))
    print(t)
    t.write(df,format='ascii')

    #Plot summed row and column values with detection level marked:
    if plotting == 'on':
        plt.plot(rowsum)
        plt.plot((0,len(rowsum)),(backsum+sigma*std,backsum+sigma*std))
        plt.title('Summed Rows')
        plt.show()
        plt.plot(colsum)
        plt.plot((0, len(colsum)), (backsum + sigma * std, backsum + sigma * std))
        plt.title('Summed Columns')
        plt.show()






