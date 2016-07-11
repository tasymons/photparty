import numpy as np
np.set_printoptions(threshold=np.inf)
from astropy.io import fits

image = fits.open('C111221.0077.fits')
print(image.info())

Data = image[0].data
#print(Data)

med = np.median(Data)
print(med)


from photutils import daofind
from astropy.stats import mad_std
bkg_sigma = mad_std(image)
sources = daofind(image, fwhm=4., threshold=3.*bkg_sigma)
print(sources)


import matplotlib.pylab as plt
plt.imshow(Data, cmap='gray_r', origin='lower')


def subarray(inputarray, slength):
    suba = inputarray[0:slength, 0:slength]
    return suba

small = subarray(Data,5)
print(small)
m = np.median(small)
print(m)
