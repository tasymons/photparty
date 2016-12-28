#This function takes a list of star coordinates and finds the sum of the pixel values for each star within a nxn box
#It also finds the background median for each star using four nxn boxes at the corners of each star's box
#The background value is subtracted from each star's value, converted into flux by dividing by exposure time,
# and this is then converted into a magnitude for each star
#By Teresa Symons 2016

def starphot(hw,inset,starpoints,etime,gain, name):
    #Import math and array index adjustment
    import numpy as np
    from fixindex import fixindex

    boxsum = []
    starback = []
    for i in starpoints:
        medsum = []
        #For each star, define a square box around it with the desired half-width
        box = inset[i[0]-hw:i[0]+hw,i[1]-hw:i[1]+hw]
        #If part of box extends outside of inset range, adjust size of box
        if box.size == 0:
            # This function takes the proposed edges of a subarray and checks if they fall outside the range of the original array
            # If they do, edges are moved to the edge of the original array
            # Inputs: length of original array (assumed to be square), first row, last row, first column, last column of subarray
            a, b, c, d = fixindex(len(inset), i[0]-hw,i[0]+hw,i[1]-hw,i[1]+hw)
            box = inset[a:b,c:d]

        #Define four boxes of the same size at each corner of the star box, making similar adjustments where necessary
        ul = inset[i[0]-3*hw:i[0]-hw,i[1]-3*hw:i[1]-hw]
        if ul.size == 0:
            a, b, c, d = fixindex(len(inset), i[0]-3*hw, i[0]-hw, i[1]-3*hw, i[1]-hw)
            ul = inset[a:b, c:d]
        ur = inset[i[0] -3*hw:i[0] -hw, i[1] +hw:i[1] +3*hw]
        if ur.size == 0:
            a, b, c, d = fixindex(len(inset), i[0] -3*hw, i[0] -hw, i[1] +hw, i[1] +3*hw)
            ur = inset[a:b, c:d]
        ll = inset[i[0] +hw:i[0] +3*hw, i[1] - 3 * hw:i[1] - hw]
        if ll.size == 0:
            a, b, c, d = fixindex(len(inset), i[0] +hw, i[0] +3*hw, i[1] - 3 * hw, i[1] - hw)
            ll = inset[a:b, c:d]
        lr = inset[i[0] +hw:i[0] +3*hw, i[1] +hw:i[1] +3* hw]
        if lr.size == 0:
            a, b, c, d = fixindex(len(inset), i[0] +hw, i[0] +3*hw, i[1] +hw, i[1] +3* hw)
            lr = inset[a:b, c:d]

        #Record medians of values inside boxes
        medboxul = np.nanmedian(ul)
        medboxur = np.nanmedian(ur)
        medboxll = np.nanmedian(ll)
        medboxlr = np.nanmedian(lr)

        #Sum up the values in the star box and take the median of all the background boxes
        medsum.append(medboxul)
        medsum.append(medboxur)
        medsum.append(medboxll)
        medsum.append(medboxlr)

        #Declare the background for a given star to be the median of the 4 median boxes
        starback.append(((2*hw)*(2*hw))*(np.nanmedian(medsum)))
        boxsum.append(np.sum(box))

    #Subtract the background value from each star
    backsub = [a-b for a, b in zip(boxsum,starback)]

    #Error message for stars with negative values after background subtraction
    if any(x<0 for x in backsub):
        print('Error: '+name+' contains a star with negative background-subtracted value - no magnitude calculated.')

    #Calculate mag errors
    magerr = [1/np.sqrt(gain*x) for x in backsub]

    #Convert to flux by dividing by exposure time
    flux = [x/etime for x in backsub]

    #Convert to magnitude
    mags = [-2.5*np.log10(a)+20 for a in flux]

    return boxsum, starback, backsub,flux, mags, hw, magerr
