# This script is to generate the .mls file given the electric field data in .fld file
#
# ver1: 2022/04/09, idea from DWHuang, RSoft
# ver2: 2022/06/19, phase error included
#
# Copyright Ryan(Sheldon) (Kuo-Fang) Chung, from NTU-GIPO NTUEEII-354
#..................................................................................................#
import numpy as np
import os, sys, getopt
from math import *

# pwd = os.path.dirname(os.path.realpath(__file__))
pwd, sysfname = os.path.split(os.path.abspath(sys.argv[0]))
os.chdir(pwd)
# print(pwd)


def str2(var):
    return var if isinstance(var, str) else str(var)

def write_phasecorrected_mls(fname, lines):
    with open(fname, 'w') as foh:
        foh.write('\n'.join(lines))
        foh.write('\n')

def read_txt(fname, startLine = 1, endLine = 0, sep = '\t', f = 'f'):
    with open(fname, 'r') as lines:
        for i, line in enumerate(lines):
            if f == 'f':
                if i == startLine:
                    data = np.array([float(num) for num in line.rstrip('\n').replace(' ', '\t').split(sep)])
                if i > startLine:
                    data = np.insert(np.array([[float(num) for num in line.rstrip('\n').replace(' ', '\t').split(sep)]]), 0, values = data, axis = 0) if line != '\n' else data     # attention!!! the '\n' at the EOF should be eliminated (if line != '\n' else data)
                if i == endLine and endLine >= startLine:
                    return data
            else:
                if i == startLine:
                    data = np.array([num for num in line.rstrip('\n').replace(' ', '\t').split(sep)])
                if i > startLine:
                    data = np.insert(np.array([[num for num in line.rstrip('\n').replace(' ', '\t').split(sep)]]), 0, values = data, axis = 0) if line != '\n' else data     # attention!!! the '\n' at the EOF should be eliminated (if line != '\n' else data)
                if i == endLine and endLine >= startLine:
                    return data
    return data

def nslab_fun(wl, tg, nfFName = None, nsFName = None, ncFName = None, nf = None, ns = None, nc = None, Nb = 6001, pol = 0, m = 0):
    DEte = lambda b, k0, tg, m, nf, ns, nc: k0* tg * np.sqrt(nf**2-ns**2) *np.sqrt(1-b) - np.arctan(np.sqrt((b+(ns**2-nc**2)/(nf**2-ns**2))/(1-b))) - np.arctan(np.sqrt((b)/(1-b))) - m*pi
    DEtm = lambda b, k0, tg, m, nf, ns, nc: k0* tg * np.sqrt(nf**2-ns**2) * np.sqrt(1-b) - np.arctan(nf**2 / nc**2 * ((b+(ns**2-nc**2)/(nf**2-ns**2))/np.sqrt(1-b))) - np.arctan(nf**2 / ns**2 * np.sqrt((b)/(1-b))) - m*pi
    neff_fun = lambda brt, nf, ns: sqrt(brt*(nf**2-ns**2)+ns**2)

    k0 = 2*pi / wl;
    
    if nfFName != None:
        nf_data = read_txt(nfFName, startLine = 0)
        nf_fun = np.vectorize(    lambda wl: np.interp(wl, nf_data[:, 0], nf_data[:, 1])    )
        nf = nf_fun(wl)
        
    if nsFName != None:
        ns_data = read_txt(nsFName, startLine = 0)
        ns_fun = np.vectorize(    lambda wl: np.interp(wl, ns_data[:, 0], ns_data[:, 1])    )
        ns = ns_fun(wl)
    
    if ncFName != None:
        nc_data = read_txt(ncFName, startLine = 0)
        nc_fun = np.vectorize(    lambda wl: np.interp(wl, nc_data[:, 0], nc_data[:, 1])    )
        nc = nc_fun(wl)
    
    b = np.linspace(0, 0.999999, Nb)
    de = DEte(b, k0, tg, m, nf, ns, nc) if pol == 0 else DEtm(b, k0, tg, m, nf, ns, nc)
    brt = np.interp(0, de[::-1], b[::-1])
    nslab = neff_fun(brt, nf, ns)
    return nslab

def printAct():
    print('\nThe exe/py file is to convert the port1.mls file into input.mls file')
    print('Editor: Ryan (Sheldon) Chung from NTU-GIPO NTU-IPL(EEII-354), Jan, 2021.')
    print('Concept from Adivisor DWHuang (Advisor: dwhuang@ntu.edu.tw)\n')
    print('Compared to phasecor.exe used in RSoft, here offers:')
    print('\t1. bug fixed of EIM (slab TM eq. instead of TE one in width direction should be used for 2D TE mode)')
    print('\t2. fat waveguide(eimff, naff) used in incremental region for dispersive property of AWG')
    print('usage: phasecorfat.exe/.py [options]')
    print('options:')
    print('\t-h | --help\t\tprints this help message')
    print('\t-i# | --if=#\t\tinput mls file named with *.mls, namely port1.mls. Default: port1.mls')
    print('\t-o# | --of=#\t\toutput fld file named with *.mls, namely input.mls. Default: test.mls')
    print('\t-l# | --wll=#\t\tcurrent wavelength[um], for dispersive property of AWG, necessary if \n\t\t\t\tinputStar solved only onc time @ central wavelength. Default: from inputfile')
    print('\t-c# | --wlc=#\t\tcentral wavelength[um], neccessary if inputStar and eimfname @ central \n\t\t\t\twavelength solved only one time. Default: from inputfile')
    print('\t-e# | --eimf=#\t\teim file for thin AWs. Height effective indices from inputfile will be used \n\t\t\t\tif it is not assigned here.')
    print('\t-n# | --naf=#\t\tfile for thin arrays neff vs wavelength[um]. It will replece eim method.')
    print('\t-f# | --eimff=#\t\teim file for fat AWs.')
    print('\t-g# | --naff=#\t\tfile for fat arrays neff vs wavelength[um]. It will replece eim method and \n\t\t\t\tnaf in fat(incremental) region.')
    print('\t-d# | --DL=#\t\tlength difference[um], neccessary, \n\t\t\t\tif it is derived from fat waveguide then naff is required.')
    print('\t-D# | --dim=#\t\tdimension, 3 for 3D which requires naf and naff.')
    print('\t-r# | --rf=#\t\treferenced phase-corrected .mls file to compare in the plot.')
    print('\t-p# | --pe=#\t\tphase error in degree.')
    # print('example: phasecorfat.exe -iport1.mls -oinput.mls -d3.566')
    print('example: python phasecorfat.py -iport1.mls -oinput.mls -d3.566')
    # print('example: phasecorfat.exe --if=port1.mls --of=input.mls --DL=3.566')
    print('example: phasecorfat.exe --if=port1.mls --of=input.mls -d3.566 --naf=na.dat --naff=nafat.dat')

# ifname = 'port1.mls'
# ofname = 'test.mls'
# DL = 259.4766169
# nafname = 'na.dat'
# rfname = 'input1.55.mls'
# phase_error = 0     # for pe is not introduced

try:
    opts, args = getopt.getopt(sys.argv[1:],'hi:o:l:c:e:n:f:g:d:D:r:p:', ['help', 'if=', 'of=', 'wll=', 'wlc=', 'eimf=', 'naf=', 'eimff=', 'naff=', 'DL=', 'dim=', 'rf=', 'pef='])
except getopt.GetoptError:
    printAct()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        printAct()
        sys.exit()
    elif opt in ('-i', '--if'):
        ifname = os.path.join(pwd, arg)
    elif opt in ('-o', '--of'):
        ofname = os.path.join(pwd, arg)
    elif opt in ('-l', '--wll'):
        wll = float(arg)
    elif opt in ('-c', '--wlc'):
        wlc = float(arg)
    elif opt in ('-e', '--eimf'):
        eimfname = os.path.join(pwd, arg)
    elif opt in ('-n', '--naf'):
        nafname = os.path.join(pwd, arg)
    elif opt in ('-f', '--eimff'):
        eimffname = os.path.join(pwd, arg)
    elif opt in ('-g', '--naff'):
        naffname = os.path.join(pwd, arg)
    elif opt in ('-d', '--DL'):
        DL = float(arg)
    elif opt in ('-D', '--dim'):
        dim = int(arg)
    elif opt in ('-r', '--rf'):
        rfname = os.path.join(pwd, arg)    
    elif opt in ('-p', '--pef'):
        pefname = os.path.join(pwd, arg)    


[headerline] = read_txt(ifname, startLine = 0, endLine = 0, f = 's')
dim = 2 if headerline == 'MODELIST_2D' else 3

[Nx, xmin, xmax, z] = read_txt(ifname, startLine = 1, endLine = 1)     # second line of port1.mls
[Nz, zmin, zmax] = read_txt(ifname, startLine = 2, endLine = 2) if dim == 3 else [0, 0, 0]

[wl] = read_txt(ifname, startLine = 2+dim-2, endLine = 2+dim-2)                           # central wavelength, third line of port1.mls
wlc = wl if 'wlc' not in globals() else wlc
wll = wl if 'wll' not in globals() else wll
dataStr = read_txt(ifname, startLine = 3+dim-2, f = 's')                                 # data starting from line 4, but in string type to avoid precision error when reading
if dim == 2:
    # data = read_txt(ifname, startLine = 3)                                             # data starting from line 4, for phase-corrected evaluation    
    data = dataStr.astype(float)
else:
    data = dataStr[:, :-1].astype(float)
M = np.size(data, 0)                                                                            # array number, here assigned with 10 for testing
ite = np.array(range(M))                                                                        # iteration index, for incremental phase calculation    
if dim == 2:
    [pol, m, w, nch, nsh, nfh] = data[0, 4:]              # polarization, mode number, width of slab waveguide, cladding index, substrate index, effective slab film index(height)
    wf, nchf, nshf, nfhf = w, nch, nsh, nfh
else:
    [pol, m, na] = data[0, 4:]
    naf = na

if 'eimfname' in globals():
    eimfLine = read_txt(eimfname, startLine = 0, f = 's')
    for ele in eimfLine:
        exec(ele)
    nc, ns, nf, w, h, hside = NC, NS, NF, W, H, Hside
    ncf, nsf, nff, wf, hf, hsidef = NC, NS, NF, W, H, Hside
    nch = nsh = nslab_fun(wl, hside, nf = nf, ns = ns, nc = nc, Nb = 10001, pol = pol, m = m)
    nfh = nslab_fun(wl, h, nf = nf, ns = ns, nc = nc, Nb = 10001, pol = pol, m = m)
    nchf = nshf = nslab_fun(wl, hside, nf = nff, ns = nsf, nc = ncf, Nb = 10001, pol = pol, m = m)
    nfhf = nslab_fun(wl, h, nf = nff, ns = nsf, nc = ncf, Nb = 10001, pol = pol, m = m)
elif 'nafname' in globals():
    na_data = read_txt(nafname, startLine = 0, endLine = -1)
    naeff = np.vectorize(    lambda wl: np.interp(wl, na_data[:, 0], na_data[:, 1])) 
    if 'naffname' not in globals():
        naffname = nafname
    
if 'eimffname' in globals():
    fateimfLine = read_txt(eimffname, startLine = 0, f = 's')
    for ele in fateimfLine:
        exec(ele)
    ncf, nsf, nff, wf, hf, hsidef = NC, NS, NF, W, H, Hside
    nchf = nshf = nslab_fun(wl, hside, nf = nff, ns = nsf, nc = ncf, Nb = 10001, pol = pol, m = m)
    nfhf = nslab_fun(wl, h, nf = nff, ns = nsf, nc = ncf, Nb = 10001, pol = pol, m = m)
elif 'naffname' in globals():
    naf_data = read_txt(naffname, startLine = 0, endLine = -1)
    nafeff = np.vectorize(    lambda wl: np.interp(wl, naf_data[:, 0], naf_data[:, 1])) 

if dim == 2:
    na = nslab_fun(wlc, w, nf = nfh, ns = nsh, nc = nch, Nb = 10001, pol = 1-pol, m = m) if 'nafname' not in globals() else naeff(wlc)
    naf = nslab_fun(wll, wf, nf = nfhf, ns = nshf, nc = nchf, Nb = 10001, pol = 1-pol, m = m) if 'naffname' not in globals() else nafeff(wll)
else:
    na = na if 'nafname' not in globals() else naeff(wlc)
    naf = naf if 'naffname' not in globals() else nafeff(wll)
    
if 'pefname' in globals():
    phase_error = np.random.rand(len(data[:, 1]))*360-180
    lines_pe = []
    for i in range(len(phase_error)):
        lines.append(str2(phase_error[i]))
    with open(pefname, 'w') as pefoh:
        pefoh.write('\n'.join(lines_pe))
        pefoh.write('\n')
else:
    phase_error = 0

# corrected phase
phipron = data[:, 1] - 2*z*(1/(np.cos(data[:, 3]*pi/180))-1)*360/wlc*na + DL*ite*360/wll*naf + phase_error

lines = [
    read_txt(ifname, startLine = 0, endLine = 0, f = 's')[0], 
    ' '.join(read_txt(ifname, startLine = 1, endLine = 1, f = 's')), 
    ]
if dim == 3:
    lines.append(' '.join(read_txt(ifname, startLine = 2, endLine = 2, f = 's')))
lines.append(read_txt(ifname, startLine = 2+dim-2, endLine = 2+dim-2, f = 's')[0])

dataStr[:, 3] = dataStr[::-1, 3]        # reverse the angle zAai

for i in range(len(phipron)):
    dataStr[i, 1] = str(phipron[i])
    lines.append(' '.join(dataStr[i, :]))
with open(ofname, 'w') as foh:
    foh.write('\n'.join(lines))
    foh.write('\n')

if 'rfname' in globals():
    import matplotlib.pyplot as plt
    dataref = read_txt(rfname, startLine = 3+dim-2, f = 's')[:, :-1].astype(float)
    line1, = plt.plot(data[:, 2], phipron, 'r--', linewidth = 2, label = ofname.replace(pwd+'\\', ''))
    line2, = plt.plot(dataref[:, 2], dataref[:, 1], 'b-', linewidth = 1, label = rfname.replace(pwd+'\\', ''))
    plt.legend(handles = [line1, line2], loc='upper right')
    plt.show()