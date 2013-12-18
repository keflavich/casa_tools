CASA Tools
==========

Tools for CASA by Adam Ginsburg.

FITS tools
----------

 * `hdr_freqtovel` is a script to convert a header written in Frequency units
   to Velocity units.  `exportfits` can do this properly with `velocity=True`,
   but this script does not require CASA.
 * `header_to_template` and `fits_to_template` are tools to extract a CASA
   template from a FITS header HDU or a FITS file.  It uses an ugly hack that
   requires writing an image of the expected size to disk as an intermediate
   step.
