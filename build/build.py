#!/usr/bin/env python3
"""Assemble ../index.html from the template + inlined libs + US TopoJSON.
Run from this build/ directory:  python3 build.py"""
import os
here = os.path.dirname(os.path.abspath(__file__))
tpl  = open(os.path.join(here, 'app.template.html')).read()
libs = open(os.path.join(here, 'libs.html')).read().strip()          # inlined d3 v7 + topojson-client
topo = open(os.path.join(here, 'us-states-10m.json')).read().strip() # us-atlas states-10m
out  = tpl.replace('__D3_LIBS__', libs).replace('__US_TOPO_JSON__', topo)
for needle in ('geoAlbersUsa', 'topojson.feature', 'US_TOPO', '"Topology"'):
    assert needle in out, 'sanity check failed: missing ' + needle
dest = os.path.join(here, '..', 'index.html')
open(dest, 'w').write(out)
print('wrote', os.path.realpath(dest), '(%d bytes)' % len(out))
