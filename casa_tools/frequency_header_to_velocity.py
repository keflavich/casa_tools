from astropy.io import fits
from astropy import units as u
from astropy import constants
import argparse

def get_reference_frequency(filename):

    h = fits.getheader(filename)

    keys = ['CTYPE','CRVAL','CDELT','CRPIX','CUNIT']

    for k in keys:
        if not k+'3' in h:
            raise KeyError("Keyword "+k+"3 not in header; not a valid CASA-produced FITS cube header")

    c3 = h['CTYPE3']
    if 'FREQ' not in c3:
        raise ValueError("CTYPE3 was {}, which is not of type FREQUENCY".format(c3))

    unit = u.Unit(h['CUNIT3'])

    f0 = ((h['CRPIX3']-1)*h['CDELT3'] + h['CRVAL3']) * unit

    return f0

def get_frequencies(filename):

    f0 = get_reference_frequency(filename)
    h = fits.getheader(filename)

    freqs = np.arange(h['NAXIS3']) * h['CDELT3'] * unit + f0

    return freqs

def get_reference_velocity(filename,
                           rest_frequency=None,
                           equivalency=u.doppler_radio):

    f0 = get_reference_frequency(filename)
    h = fits.getheader(filename)

    unit = u.Unit(h['CUNIT3'])

    if rest_frequency is None:
        rf = h['RESTFRQ'] * unit
    else:
        if hasattr(rf,'unit'):
            rf = rest_frequency
        else:
            raise ValueError("User-specified rest frequencies must have units, e.g. 1.5e10*u.Hz")

    if rf is None:
        raise ValueError("Must specify a rest frequency if one is not included in the header as RESTFRQ")

    v0 = f0.to(u.km/u.s, equivalency(rf))

    return v0

def get_velo_header(filename, **kwargs):

    h = fits.getheader(filename)
    v0 = get_reference_velocity(filename, **kwargs)
    f0 = get_reference_frequency(filename)
    unit = u.Unit(h['CUNIT3'])

    
    cdelt = (h['CDELT3']*unit / f0)*constants.c

    refframes = {1:'LSR',2:'HEL',3:'OBS'}
    refframe = refframes[h['VELREF'] % 256]

    h['CTYPE3'] = 'VELO-'+refframe
    h['CDELT3'] = cdelt.to(u.km/u.s).value
    h['CRVAL3'] = v0.to(u.km/u.s).value
    h['CUNIT3'] = 'km/s'
    # remains unchanged h['CRPIX3']

    return h

def replace_freqheader_with_veloheader(filename, **kwargs):

    vheader = get_velo_header(filename, **kwargs)

    f = fits.open(filename)

    keys = ['CTYPE','CRVAL','CDELT','CRPIX','CUNIT']

    # Replace header keywords while backing up old ones
    for k in keys:
        f[0].header[k+'3F'] = f[0].header[k+'3']
        f[0].header[k+'3'] = vheader[k+'3']

    # must overwrite
    f.writeto(filename,clobber=True)

def main():

    parser = argparse.ArgumentParser(description='Replace frequency header with velocity header')

    parser.add_argument('filename', type=str, help='the FITS file name')

    parser.add_argument('--rest-frequency',
                        type=float,
                        default=None,
                        help='rest frequency for velocity conversion in Hz')

    args = parser.parse_args()

    replace_freqheader_with_veloheader(args.filename, rest_frequency=args.rest_frequency*u.Hz)
