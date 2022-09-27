bsimw32 Si14616201303Dmode prefix=mode mode_set=0 import_list=@Si14616201303Dimpmode.txt,@Si14616201303Dimpmodecalc.txt import_symbol_file_auto=1 wait=0 free_space_wavelength=%1
python phasecorfat.py -h
bsimw32 Si14616201303Din prefix=port1%1 free_space_wavelength=%1 lambda=%1 scan_variable=lambda launch_pathway=1 slice_output_format=5 slice_display_mode=6 wait=0
python phasecorfat.py -l%1 -d3.599524388 --naf=na.dat --naff=naf.dat -iport1%1.mls -oinput%1.mls
fieldgen -datapath=.. <input%1.mls >input%1.fld
bsimw32 Si14616201303Dout prefix=output%1 free_space_wavelength=%1 lambda=%1 scan_variable=lambda launch_file=input%1.fld slice_output_format=5 slice_display_mode=6 wait=0
tailmon -v%1 <output%1.mon >>bptmp3Dscan1.dat
