import numpy as np
from astropy.io import fits
np.set_printoptions(threshold=np.inf)
#from photutils import datasets
#hdu = datasets.load_star_image()
#image = hdu.data[500:700, 500:700].astype(float)
#image -= np.median(image)
f = open('phot.txt', 'w')
image = fits.getdata('n30064.fits', ext=0)
from photutils import daofind
from astropy.stats import mad_std
bkg_sigma = mad_std(image)
print(bkg_sigma)
image[:,1102] = 0
image[:,2047] = 0
sources = daofind(image, fwhm=3.5, threshold=25.*bkg_sigma)
#print(sources)
print(len(sources))

from photutils import aperture_photometry, RectangularAperture
positions = (sources['xcentroid'], sources['ycentroid'])
apertures = RectangularAperture(positions,50,50,0)
phot_table = aperture_photometry(image, apertures,method='exact')
phot_table.pprint(max_lines=-1, max_width=-1)
print(phot_table,file = f)
flux = phot_table['aperture_sum']
print(flux, file = f)
mags = [-2.5*np.log10(a)+20 for a in flux]
print(mags,file=f)
import matplotlib.pylab as plt
plt.imshow(image, cmap='gray',vmin=0,vmax=1)
apertures.plot(color='blue', lw=1.5, alpha=0.5)
plt.show()