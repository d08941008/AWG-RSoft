CALL bptmp3Dscan1.bat
awgutil -postprocess Si14616201303Din.ind prefix=bptmp3D
rsdatabrowser bptmp3D*.pcs &
pause
