__author__ = 'donald'
'''
basic fits file i/o, along with a sample fits image.
'''

#numpy is the python package that adds array support to python - python does not have arrays by default
#these arrays are basically the same as any other language - fixed type, can be indexed over etc.
import numpy as np

#package that allows for handling of fits data
from astropy.io import fits

#define function to return square of side slength in upper left portion of input array
def subarray(inputarray,slength):
      suba = inputarray[0:slength,0:slength]
      return suba



#it's as easy as this to open a fits image: just assign the opened file to a variable
sample_image=fits.open('uds-18-G141_23096.2D.fits')

print('\nyou can find out info on the image you just opened')
print(sample_image.info())
input("\nPress Enter")

#you'll notice that table indexing starts from 0, which is the pythonic way of indexing

print('\nto get to the header of the image you can just print it if you want')
print(sample_image[0].header)

print('\nthe output is generally in terrible format, but if you want ' \
      'to access a specific header line, you can get by keyword or index:')
print(sample_image[0].header['RA'])
#or address it by its index:
print(sample_image[0].header[8])

print('\nyou can modify headers or add keywords if youd like:')
head = sample_image[0].header
head.set('fruit','strawberries')
print(sample_image[0].header['fruit'])

head.set('fruit','bananas')
print(sample_image[0].header['fruit'])

Data=sample_image[1].data
#get the dimensions of the array:
vlength = len(Data[0,:])
hlength = len(Data[:,0])

#alternately you can just call:
size = np.shape(Data)
# will give rows,columns as a tuple (r,c)

#loop over the rows and store the summed values (rowwise) into hvals using append
hvals=[]
for h in range(hlength):
      hsum=np.sum(Data[h,:])
      hvals.append(hsum)

#call previously defined function to return a 5x5 subarray in upper left corner of Data
small = subarray(Data,5)
print(small)






