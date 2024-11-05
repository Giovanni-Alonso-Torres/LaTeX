preambleList = [
# r'\usepackage{amsfonts}',
# r'\usepackage{amsmath}',
# r'\usepackage{amssymb}',
# r'\usepackage{amsthm}',
# r'\usepackage{array}',
# r'\usepackage[spanish,activeacute]{babel}',
# r'\usepackage{BOONDOX-cal}',
# r'\usepackage{color}',
# r'\usepackage{delarray}',
# r'\usepackage{dsfont}',
# r'\usepackage{eurosym}',
# r'\usepackage[T1]{fontenc}',
# r'\usepackage[utf8]{inputenc}',
# r'\usepackage{latexsym}',
# r'\usepackage{lmodern}',
# r'\usepackage{mathrsfs}',
# r'\usepackage{mathtools}',
# r'\usepackage{times}',
# r'\usepackage{upgreek}',
# r'\usepackage{xfrac}',
 r'\usepackage{siunitx}',
 r'\newcommand{\sm}[1]{{\scriptscriptstyle#1}}',
 r'\DeclareSIUnit\gauss{G}'
# r'\DeclareSymbolFont{mathcall}{OMS}{txsy}{m}{n}',
# r'\DeclareMathSymbol{\iH}{\mathord}{mathcall}{72}'
]
import numpy as np
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble='\n'.join(preambleList))
GMHz = 6

ProbeDetuning1, Transsmitance1, σT1 = np.loadtxt('42934-2_Tmean.txt', delimiter=',', unpack=True)
ProbeDetuning2, Transsmitance2, σT2 =  np.loadtxt('43675-2_Tmean.txt', delimiter=',', unpack=True)
fitx2 = np.loadtxt('43675-2_T14levelfit_freq.txt', delimiter=",", unpack=True)
fity2 = np.loadtxt('43675-2_T14levelfit_EIT.txt', delimiter=",", unpack=True)

fig, ax = plt.subplots(figsize=(8,5))
plt.errorbar(ProbeDetuning1, Transsmitance1, yerr=σT1, label=r'$\Omega_c = 0$', fmt='.-', color='orangered')
plt.errorbar(ProbeDetuning2, Transsmitance2, yerr=σT2, label=r'$\Omega_c \neq 0$', fmt='.-', color='dodgerblue')
#pl.plot(fitx2*GMHz,fity2,color='tab:orange',linewidth=0.9)
plt.legend(fontsize=14, loc='lower left')

plt.xlabel(r'\textrm{Desentonamiento haz de prueba [MHZ]}', fontsize=15)#'\\rm{Detuning $\delta_1$ (MHz)}',fontsize=15)
plt.ylabel(r'\textrm{Transmitancia}', fontsize=15)#"\\rm{Transmitance}",fontsize=15)

#plt.savefig(savepath+'EITfirst.pdf',bbox_inches='tight', dpi=150)
#plt.savefig('..\\Imagenes\\eitExp.pdf',bbox_inches='tight', dpi=300)
plt.show()