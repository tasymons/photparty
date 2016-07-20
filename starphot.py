#This function takes a list of star coordinates and finds the sum of the pixel values for each star within a nxn box
#It also finds the background median for each star using four nxn boxes at the corners of each star's box
#The background value is subtracted from each star's value, converted into flux by dividing by exposure time,
# and this is then converted into a magnitude for each star
#By Teresa Symons 2016

def starphot(hw,inset,starpoints, etime):
    #Import math
    import numpy as np

    boxsum = []
    starback = []
    for i in starpoints:
        medsum = []
        #For each star, define a square box around it with the desired half-width
        box = inset[i[0]-hw:i[0]+hw,i[1]-hw:i[1]+hw]
        #Define four boxes of the same size at each corner of the star box
        medboxul = np.nanmedian(inset[i[0]-3*hw:i[0]-hw,i[1]-3*hw:i[1]-hw])
        medboxur = np.nanmedian(inset[i[0] -3*hw:i[0] -hw, i[1] +hw:i[1] +3*hw])
        medboxll = np.nanmedian(inset[i[0] +hw:i[0] +3*hw, i[1] - 3 * hw:i[1] - hw])
        medboxlr = np.nanmedian(inset[i[0] +hw:i[0] +3*hw, i[1] +hw:i[1] +3* hw])
        #Sum up the values in the star box and take the median of the background boxes
        medsum.append(medboxul)
        medsum.append(medboxur)
        medsum.append(medboxll)
        medsum.append(medboxlr)
        #Declare the background for a given star to be the median of the 4 median boxes
        starback.append(np.nanmedian(medsum))
        boxsum.append(np.sum(box))

    #Subtract the background value from each star
    backsub = [a-b for a, b in zip(boxsum,starback)]

    #Convert to flux by dividing by exposure time
    flux = [x/etime for x in backsub]

    #Convert to magnitude
    mags = [-2.5*np.log10(a)+20 for a in flux]

    return boxsum, starback, backsub, flux, mags, hw
