import matplotlib.pyplot as plt
import numpy as np

# THE SEVEN EXACT DEFINING CONSTANTS OF THE SI UNIT SYSTEM (2019 UPDATE)
hyperfine = 9192631770  # Hyperfine transition frequency of Cs_133 [Hz]
celeritas = 299792458   # Speed of light in vacuum [m/s]
Planck = 6.62607015E-34  # Planck's constant [Js]
qel = 1.602176634E-19   # Elementary charge [C]
kB = 1.380640E-23       # Boltzmann's constant [J/K]
Avogadro = 6.02214076E23  # Avogadro's constant [1/mole]
kcd = 683               # Luminous efficacy of 540 THz radiation [candela=lumen/Watt]

# PHYSICAL CONSTANTS OF ELECTROMAGNETISM
epsilon0 = 8.8541878128E-12  # Electrical constant [F/m]
mu0 = 1.25663706212E-6       # Magnetic constant [N/A^2]
Klitzing = 25812.80745       # von Klitzing's constant [Ohm]

# UNITS USED IN QUANTUM PHYSICS
hbar = 1.054571817E-34  # Reduced Planck's constant [Js]
Angstroem = 1.0E-10     # Angström [m]
Dalton = 1.66053906660E-27  # Atomic mass unit [kg]
elm = 9.1093837015E-31  # Electron mass [kg]
nem = 1.67492749804E-27  # Neutron mass [kg]
prm = 1.67262192369E-27  # Proton mass [kg]
elecint = qel**2 / (4 * np.pi * epsilon0)  # Scale of electron-electron interaction [N*m^2]
Bohr = hbar**2 / (elm * elecint) / Angstroem  # Bohr radius [Angström]
Rydberg = (elm / (2 * hbar**2)) * (elecint)**2 / qel  # Rydberg [eV]
Hartree = 2 * Rydberg  # Hartree [eV]

# WARNING
# The rest of this file can only be executed when sourced in a *.m file
# that includes plotting commands.

# DEFAULT PLOT CONFIGURATION
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelweight'] = 'normal'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.xmargin'] = 0.02
plt.rcParams['axes.ymargin'] = 0.02
# plt.rcParams['axes.xmargin'] = 'bottom'
# plt.rcParams['axes.prop_cycle'] = plt.cycler(color=brg_colors)

# USER INTERFACE (UI) DEFAULTS
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13

# TRACING HORIZONTAL AND VERTICAL LINES ACROSS THE PLOT WINDOW
def yline(yval, **kwargs):
    plt.axhline(y=yval, **kwargs)

def xline(xval, **kwargs):
    plt.axvline(x=xval, **kwargs)

# Example usage:
# yline(2.0, color='r', linestyle='--')
# xline(0.5, color='b', linestyle=':')
