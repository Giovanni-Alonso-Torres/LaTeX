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
π = np.pi

δp = np.linspace(-120, 120, 10000)
Γe = 2*π*6.06 # En MHz
Γr = 2*π*0.1  # En MHz
γg = 0.15     # En MHz

def χ(Ωc):
    return (δp+1j*(Γr/2+2*γg))/((Γr/2+2*γg-1j*δp)*(Γe/2+γg/2-1j*δp)+Ωc**2/4)

fig = plt.figure(figsize=(12,4))
ax = plt.Axes(fig, [0.06,0.2,0.93,0.76])
fig.add_axes(ax)

plt.plot(δp, χ(2*π*6.6).real, color='dodgerblue', label=r'$\Omega_{c}\neq0$')
plt.plot(δp, χ(0).real, color='orangered', label=r'$\Omega_{c}=0$')
plt.xticks([0],[0], fontsize=20)
plt.yticks([0],[0], fontsize=20)
plt.xlabel(r'$\delta_{p}$ \textrm{[u.a.]}', fontsize=25)
plt.ylabel(r'$\textrm{Re}{(\chi)}$', fontsize=25)
plt.legend(fontsize=23)
plt.savefig('..\\Imagenes\\dispersion.pdf', transparent=True, dpi=300)
plt.show()