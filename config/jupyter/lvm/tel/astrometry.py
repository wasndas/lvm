# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: lvm/tel/astrometry.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from lvmtipo.actors import lvm
from logging import DEBUG, INFO
from sdsstools import get_logger

from math import nan
from astropy.io import fits


# TODO: put some real astronomy in here.

class Astrometry:

    @staticmethod
    async def calc(telsubsys, ra, dec, exptime=5, logger = get_logger("lvm_tel_astrometry"), level = INFO):
        try:
            rc = await telsubsys.agc.expose(exptime)
            file_east = rc["east"]["filename"]
            file_west = rc["west"]["filename"]
            
            # do some astrometry :-]
            ra_offset, dec_offset = 0.2, 0.3
            refocus_offset = -42
            km_offset = 0.0
            
            return ra_offset, dec_offset, refocus_offset, km_offset

        except Exception as ex:
           logger.error(ex)
           raise ex


async def main():

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", '--verbose', action='store_true', help="print some notes to stdout")
    parser.add_argument("-t", '--telsubsys', type=str, default="sci", help="Telescope subsystem: sci, skye, skyw or spec")
    parser.add_argument("-e", '--exptime', type=float, default=5.0, help="Expose for for exptime seconds")
    parser.add_argument("-r", '--ra', help="RA J2000 in hours")
    parser.add_argument("-d", '--dec', help="DEC J2000 in degrees")

    args = parser.parse_args()
    
    telsubsys = await lvm.from_string(args.telsubsys)

    await Astrometry.calc(telsubsys, args.ra, args.dec, args.exptime, level = DEBUG if args.verbose else INFO)


if __name__ == '__main__':

    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


