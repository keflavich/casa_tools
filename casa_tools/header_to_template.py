"""
Convert a FITS header to a CASA / imregrid "template" dict
"""
from astropy.io import fits
from warnings import warn
import numpy as np
import tempfile
# requires CASA!
from taskinit import iatool

def header_to_template(header):
    """
    Convert a FITS Header object into a CASA template dictionary

    The FITS header should be a FITS Header instance.  If you have a FITS file,
    use `fits_to_template` instead
    """

    if isinstance(header,str):
        header = fits.Header.fromtextfile(header)
    elif not isinstance(header,fits.Header):
        warn("Header is not a FITS header instance.  There may be crashes due to inconsistency as a result.")

    tf = tempfile.NamedTemporaryFile()

    # Determine the output shape from the NAXIS keywords.  This will fail if
    # there is any inconsistency!
    shape = np.array([header['NAXIS%i'% nax] for nax in xrange(1,header['NAXIS']+1)], dtype='int32')

    hdu = fits.PrimaryHDU(header=header,data=np.empty(shape,dtype='float'))
    hdu.writeto(tf.name)

    return fits_to_template(tf.name)


def fits_to_template(fitsfilename):
    """
    Extract a CASA "template" header from a FITS file
    """
    
    if not isinstance(fitsfilename,str):
        raise ValueError("FITS file name must be a filename string")

    ia = iatool()
    ia.fromfits(infile=fitsfilename, outfile=td, overwrite=True)

    td = tempfile.mkdtemp()

    ia.open(td)
    csys = ia.coordsys()
    shape = ia.shape()

    ia.close()

    outheader = {'csys':csys.torecord(),
                 'shap':shape}

    return outheader
