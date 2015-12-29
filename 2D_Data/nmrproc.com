#!/bin/csh
  nmrPipe -in data.fid                          \
| nmrPipe  -fn SP -off 0.5 -end 0.99 -pow 2 -c 0.5 \
| nmrPipe  -fn ZF -auto                            \
| nmrPipe  -fn FT -auto                                 \
| nmrPipe  -fn PS -p0 87 -p1 0 -di -verb       \
| nmrPipe  -fn EXT -left -sw \
| nmrPipe  -fn TP                                 \
| nmrPipe  -ov -out data.ft1 

nmrPipe -in data.ft1 \
| nmrPipe  -fn SP -off 0.5 -end 0.99  -pow 2 -c 0.5         \
| nmrPipe  -fn ZF -auto                            \
| nmrPipe  -fn FT                                       \
| nmrPipe  -fn PS -p0 -90 -p1 20.0 -di  -verb 0            \
| nmrPipe  -fn POLY -auto -ord 1 \
| nmrPipe  -fn TP                                 \
| nmrPipe  -fn POLY -auto -ord 1 \
| nmrPipe  -ov -out data.ft2

