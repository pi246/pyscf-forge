#!/usr/bin/env python

'''
multi-state

A "quasidegenerate" extension of MC-PDFT for states close in energy. Currently
only "compressed multi-state" (CMS) is supported [JCTC 16, 7444 (2020)]
'''

from pyscf import gto, scf, mcpdft

mol = gto.M(
    atom = [
        ['Li', ( 0., 0.    , 0.   )],
        ['H', ( 0., 0., 3)]
    ], basis = 'sto-3g',
    symmetry = 0 # symmetry enforcement is not recommended for MS-PDFT
    )

mf = scf.RHF(mol)
mf.kernel()

mc = mcpdft.CASSCF(mf, 'tpbe', 2, 2)
mc.fix_spin_(ss=0) # often necessary!
mc_sa = mc.state_average ([.5, .5]).run ()
mc_ms = mc.multi_state ([.5, .5]).run (verbose=4)

print ('{:>21s} {:>12s} {:>12s}'.format ('state 0','state 1', 'gap'))
fmt_str = '{:>9s} {:12.9f} {:12.9f} {:12.9f}'
print (fmt_str.format ('CASSCF', mc_sa.e_mcscf[0], mc_sa.e_mcscf[1],
    mc_sa.e_mcscf[1]-mc_sa.e_mcscf[0]))
print (fmt_str.format ('MC-PDFT', mc_sa.e_states[0], mc_sa.e_states[1],
    mc_sa.e_states[1]-mc_sa.e_states[0]))
print (fmt_str.format ('CMS-PDFT', mc_ms.e_states[0], mc_ms.e_states[1],
    mc_ms.e_states[1]-mc_ms.e_states[0]))
