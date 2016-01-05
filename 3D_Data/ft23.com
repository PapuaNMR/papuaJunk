#!/bin/csh -f

#
# 3D States-Mode HN-Detected Processing.

xyz2pipe -in rec/data%03d.ft1 -x \
| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 1 -c 0.5 \
| nmrPipe  -fn ZF -auto                       \
| nmrPipe  -fn FT -verb                           \
| nmrPipe  -fn PS -p0 0.0 -p1 0.0 -di              \
| nmrPipe -fn REV -verb \
| nmrPipe  -fn TP \
| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5 \
| nmrPipe  -fn ZF -auto  \
| nmrPipe  -fn FT -verb                       \
| nmrPipe  -fn PS -p0 -9  -p1 0.0 -di              \
| nmrPipe  -fn POLY -auto -ord 1 \
| nmrPipe  -fn TP \
| nmrPipe  -fn POLY -auto -ord 1 \
| nmrPipe  -fn ZTP \
#| nmrPipe  -fn POLY -auto -ord 1 \
| pipe2xyz -out rec/HNCO%03d.ft3 -x

xyz2pipe -in rec/HNCO%03d.ft3 > HNCO.pipe
