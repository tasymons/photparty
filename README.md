# photparty
**Description:**

This program provides automatic star detection and square-aperture photometry for single-star and un-crowded FITS or FIT frames. 

It contains seven files: 

photparty.py - main script

background.py

binsum.py

fixindex.py

starlocate.py

starmed.py

starphot.py

**How to use:**

The main script, photparty.py, contains all of the user inputs and parameters in the header. Running this script will return separate output files for each FIT or FITS file in the user-specified directory. For each input file, two output files are generated. 'File Name'dat.txt contains a list of located stars with magnitudes and magnitude errors. 'File Name'mag.txt contains a more detailed step-by-step output not needed for regular use, but helpful for calibration in unique or problematic cases. All other scripts are auxiliary functions used by the main script.

**Required packages:**

This program was written in Python 3.5 and has no current compatibility with Python 2. It was developed in PyCharm CE with Anaconda. Required external packages include AstroPy, NumPy, and Matplotlib. 

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

**Acknowledgements:**

This program was developed as part of a thesis project at the University of Kansas. The support of funding from the National Science Foundation, through grant AST 1211621, is gratefully acknowledged.


