#!/bin/csh -f

set com = $1

if ($com == 'xyz') then

rm -rf xyz #clean up

xyz2pipe -in fid/test%03d.fid -x \
| nmrPipe -fn SOL \
| nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5  \
| nmrPipe  -fn ZF -auto                         \
| nmrPipe  -fn FT -verb                             \
| nmrPipe  -fn PS -p0 0 -p1 0.0 -di              \
| nmrPipe -fn POLY -auto -ord 1 -x1 11.5ppm -xn 5ppm \
| nmrPipe -fn EXT -x1 11ppm -xn 5.5ppm -sw -round 2 \
| pipe2xyz -ov -out xyz/data%03d.dat -x

endif

if ($com == 'yzx') then

rm -rf yzx # clean up
rm -rf yzx_ist # clean up
mkdir yzx
mkdir yzx_ist

xyz2pipe -in fid/test%03d.fid -x \
| nmrPipe -fn SOL \
| nmrPipe  -fn SP -off 0.35 -end 0.98 -pow 2 -c 0.5   \
| nmrPipe  -fn ZF -auto                      \
| nmrPipe  -fn FT -verb                             \
| nmrPipe  -fn PS -p0 -60 -p1 0.0 -di              \
| nmrPipe -fn POLY -auto -ord 1 -x1 12ppm -xn 5ppm \
| nmrPipe -fn EXT -x1 11ppm -xn 6ppm -sw -round 2 \
| pipe2xyz -ov -out yzx/data%03d.dat -z

endif

