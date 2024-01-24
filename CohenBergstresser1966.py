import numpy as np

# INPUT PARAMETERS FOR COMPUTING
# THE ELECTRON BAND STRUCTURE OF FCC SEMICONDUCTORS
# USING EMPIRICAL PSEUDOPOTENTIALS

semiconductor = 'Si'
tol = 1e-12

# PARAMETERS IN RECIPROCAL SPACE
BZstep = 0.02  # Step along path in BZ
cutoff = 21    # Deal only with |G|^2 < cutoff [2*pi/spacing]^2
               # in Hamiltonian
Gs_max = 11    # |G|^2 of highest non-zero Fourier coefficients in
               # expanding potential [2*pi/spacing]^2

# FOR COMPUTING THE DISPERSION RELATION
# PATH IN BRILLOUIN ZONE OF FCC LATTICE

dispersion_relation = True

if dispersion_relation:
    nband = 16    # Number of bands to be stored in output file

    qs = np.array([[0.5, 0.5, 0.5], [0, 0, 0], [1, 1, 0], [0.75, 0.75, 0]])
    qs_str = ['L', '\Gamma', 'X', 'K']

    qe = np.array([[0, 0, 0], [1, 0, 0], [0.75, 0.75, 0], [0, 0, 0]])
    qe_str = ['\Gamma', 'X', 'K', '\Gamma']

# FOR COMPUTING DOS
# MONKHORST-PACK SAMPLING PARAMETERS OF BZ VOLUME

compute_dos = True

if compute_dos:
    movie = True    # Show movie of DOS construction
    mp = 21         # mp^3 q vectors will sample the BZ volume if no
                    # symmetry is exploited
    foldsym = 1     # th-fold symmetry to be exploited =>
                    # mp^3/foldsym q vectors will sample the BZ volume
    Energy_min = -14  # [eV]
    Energy_max = 6    # [eV]
    E_step = 0.005    # [eV]

    FWHM = E_step * 5  # Full Width at Half-Maximum of the
                       # representation of the Dirac delta function
    Dirac = 'Gaussian'  # Representation of Dirac delta function
                        # Possible choices: 'Gaussian' or 'Lorentzian'

    Energy = np.arange(Energy_min, Energy_max + E_step, E_step)
    DOS = np.zeros(len(Energy))  # Initialize DOS

# DATA OF EMPIRICAL PSEUDOPOTENTIALS
# FOR COMPUTING ELECTRON ENERGY BANDS
# OF 14 FCC SEMICONDUCTORS
#
# from M.L. Cohen & T.K. Bergstresser,
# Phys. Rev. vol.141, p.789 (1966)

material_list = ['Si', 'Ge', 'Sn', 'GaP', 'GaAs', 'AlSb', 'InP', 'GaSb', 'InAs', 'InSb', 'ZnS', 'ZnSe', 'ZnTe', 'CdTe', 'Empty lattice']

# MATERIAL IDENTIFIER

m = material_list.index(semiconductor)

if m == -1:
    raise ValueError('Semiconductor material not recognized.')

# DIRECT LATTICE UNIT VECTORS AND ATOMIC POSITIONS
# OF FCC SEMICONDUCTORS

a = np.array([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.5, 0.0, 0.5]])
cell_volume = np.dot(a[:, 0], np.cross(a[:, 1], a[:, 2]))

tau = np.array([[0.125, 0.125, 0.125], [-0.125, -0.125, -0.125]])

# LATTICE SPACINGS [Angström]

ls = np.array([5.43, 5.66, 6.49, 5.44, 5.64, 6.13, 5.86, 6.12, 6.04, 6.48, 5.41,
               5.65, 6.07, 6.41])

# PSEUDOPOTENTIAL FORM FACTORS [Rydberg]

# Remark: ff(i, 0) = V0 = V_{G=0} for material i
#                 = constant adjusting zero of potential

#            V0  VS3  VS8  VS11 VA3  VA4  VA11
ff = np.array([
    [0.00, -0.21, 0.04, 0.08, 0.00, 0.00, 0.00],  # Si
    [0.00, -0.23, 0.01, 0.06, 0.00, 0.00, 0.00],  # Ge
    [0.00, -0.20, 0.00, 0.04, 0.00, 0.00, 0.00],  # Sn
    [0.00, -0.22, 0.03, 0.07, 0.12, 0.07, 0.02],  # GaP
    [0.00, -0.23, 0.01, 0.06, 0.07, 0.05, 0.01],  # GaAs
    [0.00, -0.21, 0.02, 0.06, 0.06, 0.04, 0.02],  # AlSb
    [0.00, -0.23, 0.01, 0.06, 0.07, 0.05, 0.01],  # InP
    [0.00, -0.22, 0.00, 0.05, 0.06, 0.05, 0.01],  # GaSb
    [0.00, -0.22, 0.00, 0.05, 0.08, 0.05, 0.03],  # InAs
    [0.00, -0.20, 0.00, 0.04, 0.06, 0.05, 0.01],  # InSb
    [0.00, -0.22, 0.03, 0.07, 0.24, 0.14, 0.04],  # ZnS
    [0.00, -0.23, 0.01, 0.06, 0.18, 0.12, 0.03],
    [0.00, -0.22, 0.00, 0.05, 0.13, 0.10, 0.01], #ZnTe
    [0.00, -0.20, 0.00, 0.04, 0.15, 0.09, 0.04]])
