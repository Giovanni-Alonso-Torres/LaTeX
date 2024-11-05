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
import h5py
import json
from scipy.optimize import curve_fit
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble='\n'.join(preambleList))

override_parameter =  'ProbeDetuning' 

start = 241484
cycles = 2

# Remove cycles from analysis. 
exclude_cycles = []

# fit options: None, "OD", "EIT"
fit = "EIT"

##########################################
########## Physical Constants ############

Γ1 = 6.06 # MHz Rb 5S_1/2 <--> 5P_3/2

with h5py.File(f'tag/{start}-tags.hdf5', 'r') as file:
    iterators = json.loads(file.attrs['iterators'])
    parameter_name = next(iter(iterators.keys()))
    num_pulses =  int(json.loads(file.attrs['variables'])['num_pulses'])
    num_bins = int(json.loads(file.attrs['variables'])['num_bins'])
    bin_width = int(json.loads(file.attrs['variables'])['bin_width'])
    num_values = iterators[next(iter(iterators.keys()))]['num_values']
    end = start+num_values*cycles-1
    print(file.keys())
    print(file.attrs.keys())
nums = range(start, end+1)
paths = [f'tag/{file_no}-tags.hdf5' for file_no in nums]
if override_parameter:
    parameter_name = override_parameter


vardata  = []
itedata  = []
signals  = []
references = []
for path in paths:
    with h5py.File(path, 'r') as file:
        vardata.append(json.loads(file.attrs['variables']))
        itedata.append(json.loads(file.attrs['iterators']))
        signals.append(np.array(file['spcm1signal']))
        references.append(np.array(file['spcm1ref']))
        
signals     = np.array(signals)
references  = np.array(references)

signals     = signals.reshape((cycles, num_values, num_pulses, num_bins))
references  = references.reshape((cycles, num_values, num_pulses, num_bins))

variables = {key: [i[key] for i in vardata] for key in vardata[0]}
iterators = {key: [i[key] for i in itedata] for key in itedata[0]}
x_values = np.array(variables[parameter_name][:num_values])

print(signals.shape)

signal     = signals.sum(axis=(-1,-2))
reference  = references.sum(axis=(-1,-2))

excluded = np.array([ c in exclude_cycles for c in range(cycles)])
included = np.invert(excluded)

T  = signal/reference
Tm = T[included].mean(axis=0)
Ts = T[included].std(axis=0)


def transmittanceEITFunction(δp, δp0, δc, OD0, γg, Ωc, offs, amp):

    A = 2j*γg+δc+(δp-δp0)
    C = Γ1+γg-2j*(δp-δp0)
    D = 4*γg-2j*(δc+(δp-δp0)) 
    E = Ωc**2
    α = 2*OD0*(Γ1+γg)*np.imag(A/(C*D+E))
    return amp*np.exp(-α)+offs

def transmittanceFunction(δ, δ0, OD0) :
    return np.exp(-OD0/(1+(2*(δ-δ0)/Γ1)**2))


plt.figure(dpi=200)

try:
    if fit == "EIT":
        p0 = [-2.9,0.1,10.9,0.06,7,0,1]
        popt, pcov = curve_fit(transmittanceEITFunction, x_values, Tm, p0=p0)
        x_smooth = np.linspace(x_values[0], x_values[-1],len(x_values)*100)
        Tfit = transmittanceEITFunction(x_smooth, *popt)
        plt.plot(x_smooth, Tfit, color="orangered", label=r'$\Omega_c = 0$')

        # props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
        # paramstr = f'δp$_0$={popt[0]:.1f} MHz\nδc= {popt[1]:.1f} MHz\nOD= {popt[2]:.1f}\nγ$_g$={popt[3]:0.2f} MHz\nΩ$_c$={popt[4]:0.1f} MHz'
        # plt.text(0.05, 0.23, paramstr, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top', bbox=props)

    if fit == "OD":
        p0 = [0,10]
        popt, pcov = curve_fit(transmittanceFunction, x_values, Tm, p0=p0)
        x_smooth = np.linspace(x_values[0], x_values[-1],len(x_values)*100)
        Tfit = transmittanceFunction(x_smooth, *popt)
        plt.plot(x_smooth, Tfit, color="C1", label="fit")

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
        paramstr = f'δ={popt[0]:.1f} MHz\nOD= {popt[1]:.1f}'
        plt.text(0.05, 0.23, paramstr, transform=plt.gca().transAxes, fontsize=8, verticalalignment='top', bbox=props)

except RuntimeError:
    pass


plt.errorbar(x=x_values, y=Tm, yerr=Ts, color="dodgerblue", ecolor='black', label=r'$\Omega_c \neq 0$')
plt.legend(fontsize=14, loc='lower left')

plt.xlabel(r'\textrm{Desentonamiento haz de prueba [MHZ]}', fontsize=15)
plt.ylabel(r'\textrm{Transmitancia}', fontsize=15)


excl_str = ""
if len(exclude_cycles) > 0:
    excl_str = f"\\{exclude_cycles}"

# plt.title(f"{start}-{cycles}{excl_str}")

plt.savefig('..\\Imagenes\\eitExp.pdf',bbox_inches='tight', dpi=300)

plt.show()