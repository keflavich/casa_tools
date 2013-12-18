"""
Convert a FITS header to a CASA / imregrid "template" dict
"""
from astropy.io import fits
from warnings import warn
import numpy as np
import tempfile
from taskinit import iatool

def header_to_template(header):
    """
    Convert a FITS Header object into a CASA template dictionary
    """

    if not isinstance(header,fits.Header):
        warn("Header is not a FITS header instance.  There may be crashes due to inconsistency as a result.")

    tf = tempfile.NamedTemporaryFile()

    # Determine the output shape from the NAXIS keywords.  This will fail if
    # there is any inconsistency!
    shape = np.array([header['NAXIS%i'% nax] for nax in xrange(1,header['NAXIS']+1)], dtype='int32')

    hdu = fits.PrimaryHDU(header=header,data=np.empty(shape,dtype='float'))
    hdu.writeto(tf.name)

    td = tempfile.mkdtemp()

    ia = iatool()
    ia.fromfits(infile=tf.name, outfile=td, overwrite=True)

    outheader = ia.regrid(td, 'get')

    ia.close()

    return outheader

