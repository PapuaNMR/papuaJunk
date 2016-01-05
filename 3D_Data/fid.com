#!/bin/csh

bruk2pipe -in ./ser \
  -bad 0.0 -noaswap -DMX -decim 24 -dspfvs 12 -grpdly -1  \
  -xN              2048  -yN                 4  -zN               204  \
  -xT              1024  -yT                 2  -zT               102  \
  -xMODE            DQD  -yMODE           Real  -zMODE           Real  \
  -xSW         7183.908  -ySW         1947.269  -zSW         1510.144  \
  -xOBS         600.473  -yOBS          60.852  -zOBS         151.014  \
  -xCAR           4.703  -yCAR         115.987  -zCAR         172.970  \
  -xLAB              HN  -yLAB             15N  -zLAB             13C  \
  -ndim               3  -aq2D          States                         \
| nmrPipe -fn MAC -macro $NMRTXT/ranceY.M -noRd -noWr   \
| pipe2xyz -x -out ./fid/test%03d.fid -verb -ov -to 0

