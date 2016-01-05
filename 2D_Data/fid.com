bruk2pipe -in ser \
  -bad 0.0 -noaswap -DMX -decim 24 -dspfvs 12 -grpdly 0  \
  -xN              2048  -yN               128  \
  -xT              1024  -yT                64  \
  -xMODE            DQD  -yMODE  Echo-AntiEcho  \
  -xSW         7002.801  -ySW         1824.568  \
  -xOBS         500.132  -yOBS          50.684  \
  -xCAR           4.769  -yCAR         118.062  \
  -xLAB              HN  -yLAB             15N  \
  -ndim               2  -aq2D          States  \
  -out ./data.fid -verb -ov