#!/bin/csh

xyz2pipe -in yzx_ist/data%03d.phf | phf2pipe -user 1 -xproj xz.ft1 -yproj yz.ft1 \
| pipe2xyz -out rec/data%03d.ft1

