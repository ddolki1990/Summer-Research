#!/usr/bin/env python

if __name__ == "__main__":
    import sys, sqlite3
    from contextlib import closing
    from pprint import pprint
    ra,dec = map(float,sys.argv[1:3])
    radius = float(sys.argv[3])
    band = int(sys.argv[4])
    # TODO: Do math correctly here, handle singularities
    minra = ra - radius
    mindec = dec - radius
    maxra = ra + radius
    maxdec = dec + radius
    with closing(sqlite3.connect('tidal-flares.db')) as conn:
        cursor = conn.cursor()
        pprint(list(cursor.execute('''
		SELECT SOURCE.RA, 
               SOURCE.DEC,
               OBSERVATION.DATE,
               OBSERVATION.DURATION,
               Flux.Foreground,
               Flux.Background,
               Flux.bandid
          from fluxes as Flux
		        JOIN obsids as OBSERVATION on Flux.obsid = OBSERVATION.id
                JOIN sources as SOURCE on Flux.sourceid = SOURCE.id
                WHERE 
                  FLUX.bandid = ? AND 
                  ? < SOURCE.RA AND 
                  SOURCE.RA < ? AND
                  ? < Source.Dec AND
                  source.dec < ?
                limit 5;
		''', (band,minra,maxra,mindec,maxdec))))
