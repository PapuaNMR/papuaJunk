nmrPipe -in 13C.1H.dat \
| nmrPipe  -fn ZTP \
| nmrPipe -out test.ft2 -ov -verb 
