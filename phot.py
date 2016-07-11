import numpy as np
from astropy.io import fits
#from photutils import datasets
#hdu = datasets.load_star_image()
#image = hdu.data[500:700, 500:700].astype(float)
#image -= np.median(image)
image = fits.getdata('Ty111221.0145.fits', ext=0)
from photutils import daofind
from astropy.stats import mad_std
bkg_sigma = mad_std(image)
sources = daofind(image, fwhm=3.5, threshold=10.*bkg_sigma)
#print(sources)

from photutils import aperture_photometry, CircularAperture
positions = (sources['xcentroid'], sources['ycentroid'])
apertures = CircularAperture(positions, r=50.)
phot_table = aperture_photometry(image, apertures)
#print(phot_table)

import matplotlib.pylab as plt
plt.imshow(image, cmap='gray',vmin=0,vmax=1)
apertures.plot(color='blue', lw=1.5, alpha=0.5)
plt.show()