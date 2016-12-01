#The goal of this script is to read fits files, locate stars, and return magnitudes for those stars
#Background sky level is calculated using random median sampling of square arrays
#A specific inset of the data array is taken if desired
#Pixel values are summed row-wise and column-wise and background level is used to determine which rows and columns contain stars
#A list of matched star coordinates is prepared
#Star magnitudes are obtained using square apertures after being background subtracted for the region specific to the star
#By Teresa Symons 2016

#USER-DEFINED PARAMETERS AND SETTINGS:

#Define path to folder containing files to be run
#All fits or fit files will be automatically included
#Output files will also be placed into this folder
path = '/Users/Andromeda/PycharmProjects/files'

#Header key words/values:
#If no keyword exists, enter 'NONE' and define value instead
#Exposure time
exptimekword = 'EXP_TIME'
exptime = 5
#Filter
filterkword = 'FILTER'
filter = 'b'
#Airmass
airmasskword = 'AIRMASS'
airmass = 100
#Gain
gainkword = 'NONE'
gain = 1

#Parameters for background sampling:
#Width/length in pixels of box for random background sampling to determine background value
backsize = 5
#Number of random background samples to take
backnum = 1000

#Selection of area of each frame to analyze:
#If area of interest is in the central 50% of frame, select 'half'
#If area of interest is entire frame, select 'whole'
framearea = 'half'

#Detection level:
#Select number of standard deviations above background required for star detection
sig = 50

#Suppress or display plots of summed rows/columns with detection level marked (on or off)
plotdetect = 'on'

#Suppress or display plots of fits image with detected star apertures overlaid (on or off)
plotstars = 'on'

#Square-aperture size:
#Select the half-width of the box used for photometry
boxhw = 25

#END USER-DEFINED PARAMETERS

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
import matplotlib.patches as patches
import matplotlib.pylab as plt

#Create list of files to run based on defined path, ignoring all files that are not fit or fits
files = [f for f in os.listdir(path) if any([f.endswith('fit'), f.endswith('fits')]) if not f.startswith('.')]

#Alternatively, run list of files in a specified text file
#In this case files will output to the location of the main script
#files = [line.rstrip() for line in open('files.txt')]

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
    if exptimekword == 'NONE':
        etime = exptime
    else:
        etime = image[0].header[exptimekword]
    if filterkword == 'NONE':
        filter = filter
    else:
        filter = image[0].header[filterkword]
    if airmasskword == 'NONE':
        airmass = airmass
    else:
        airmass = image[0].header[airmasskword]
    if gainkword == 'NONE':
        gain = gain
    else:
        gain = image[0].header[gainkword]

    #Compute background sky level through random median sampling:
    #Inputs: data array, nxn size of random subarray to use for sampling, and number of desired sampling iterations
    back, skyvals = background(Data,backsize,backnum)

    #Create desired inset of total data array:
    if framearea == 'half':
        #Find midpoint of image data
        mid = len(Data)/2
        #Take an inset of data that is half of area
        inset = Data[round(mid/2):3*round(mid/2),round(mid/2):3*round(mid/2)]
    if framearea == 'whole':
        #Use entire data array as inset
        inset = Data
        mid = 0

    #Blanket removal of bad pixels above 45000 and 3*standard deviation below 0:
    inset[inset>45000] = 0
    std = np.std(inset)
    inset[inset<-3*std] = 0

    #Calculate sky background for specific inset:
    #Inputs: inset data array, nxn size of random subarray used for sampling, number of desired sampling iterations
    insetback, insetskyvals = background(inset,backsize,backnum)

    #Compute summed row and column values for desired array by number of bins:
    #Inputs: inset data array, number of bins desired
    rowsum, colsum = binsum(inset,1)

    #Locate values in summed row and column vectors that are greater than desired sigma level above background:
    #Inputs: Data array, background level variable, desired sigma detection level, summed row vector, summed column vector
    starrow, starcol, backsum, std, sigma = starlocate(inset,insetback,sig,rowsum,colsum)

    #Take indices of detected star pixels and divide into sublists by individual star:
    #Return sublists of star indices, number of stars, and median pixel of each star
    #Pair star center row with star center column and return total number of pairs found
    #Inputs: vectors containing indices of detected star pixels for row and column and inset data array
    rowloc, colloc, numstarr, numstarc, rowmed, colmed, starpoints, adjstarpoints = starmed(starrow,starcol,inset,mid)

    #Take list of star coordinates and find summed pixel values within a square aperture of desired size:
    #Also find background values for each star and subtract them from star values
    #Convert background-subtracted star values into fluxes and then magnitudes
    #Inputs: half-width of nxn square aperture, inset data array, vector containing star coordinates, exposure time
    boxsum, starback, backsub, flux, mags, hw, magerr = starphot(boxhw, inset, starpoints, etime, gain, name)

    #Output data table to file:
    n = len(mags)
    tname = [i]*n
    tfilter = [filter]*n
    tairmass = [airmass]*n
    tetime = [etime]*n
    x = [x for [x,y] in adjstarpoints]
    y = [y for [x,y] in adjstarpoints]
    t = Table([tname, tfilter, tairmass, tetime, x, y, mags, magerr], names=('File_Name', 'Filter', 'Airmass', 'Exposure_Time', 'X', 'Y', 'Magnitude', 'Mag_Err'))
    t.write(df,format='ascii')

    #Plot summed row and column values with detection level marked:
    if plotdetect == 'on':
        plt.plot(rowsum)
        plt.plot((0,len(rowsum)),(backsum+sigma*std,backsum+sigma*std))
        plt.title('Summed Rows'+'-'+name)
        plt.xlabel('Row Index in Data Inset')
        plt.ylabel('Summed Row Value')
        plt.show()
        plt.plot(colsum)
        plt.plot((0, len(colsum)), (backsum + sigma * std, backsum + sigma * std))
        plt.title('Summed Columns'+'-'+name)
        plt.xlabel('Column Index in Data Inset')
        plt.ylabel('Summed Column Value')
        plt.show()

    #Plot fits image with square apertures for detected stars overlaid
    if plotstars == 'on':
        fig, ax = plt.subplots(1)
        ax.imshow(Data, cmap='Greys',vmin=0,vmax=10)
        for i in range(0,len(x)):
            rect = patches.Rectangle(((x[i]-hw),(y[i]-hw)), 2*hw, 2*hw, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        plt.title(name)
        plt.show()

    #Printing of values to check program function to file
    print('Exposure time:', file=f)
    print(etime, file=f)
    print('Filter:', file=f)
    print(filter, file=f)
    print('Airmass:', file=f)
    print(airmass, file=f)
    print('Sky background level:', file=f)
    print(back, file=f)
    print('Shape of inset array:', file=f)
    print(np.shape(inset), file=f)
    print('Inset background sky level:', file=f)
    print(insetback, file=f)
    print('Summed background value for one row/column:', file=f)
    print(backsum, file=f)
    print('Standard deviation of inset:', file=f)
    print(std, file=f)
    print('Detection level in sigma:', file=f)
    print(sigma, file=f)
    print('Indices of detected stars:', file=f)
    print(starrow, file=f)
    print(starcol, file=f)
    print('Indices of detected stars divided into sublist by star:', file=f)
    print(rowloc, file=f)
    print(colloc, file=f)
    print('Number of stars found by row/column:', file=f)
    print(numstarr, file=f)
    print(numstarc, file=f)
    print('Median pixel of each star by row/column:', file=f)
    print(rowmed, file=f)
    print(colmed, file=f)
    print('Paired indices of star centers:', file=f)
    print(starpoints, file=f)
    print('Total number of stars found:', file=f)
    print(len(starpoints), file=f)
    print('Coordinates of stars (x,y):', file=f)
    print(adjstarpoints, file=f)
    print('Width/Height of boxes:', file=f)
    print(hw * 2, file=f)
    print('Pixel sums for boxes around each star:', file=f)
    print(boxsum, file=f)
    print('Background values for each star:', file=f)
    print(starback, file=f)
    print('Background subtracted star values:', file=f)
    print(backsub, file=f)
    print('Flux of stars:', file=f)
    print(flux, file=f)
    print('Magnitudes for each star:', file=f)
    print(mags, file=f)