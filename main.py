import matplotlib.pyplot as plt
import numpy as np

import finesse
from finesse.analysis.actions import Xaxis
finesse.init_plotting()

base = finesse.Model()

base.parse(""" 
           
l LASER P=2
s NULLSPACE LASER.p1 M1.p1 L=.5
m M1 T=0.03 L=37.5u
s CAVITY M1.p2 M2.p1 L=1
m M2 T=0.03 L=37.5u

s DISTANCE M2.p2 M3.p1 L=.2
m M3 T=0.3 L=37.5u
free_mass M3_sus M3.mech mass=40
""")   

# specifying our frequency range for future use
fstart = .1
fstop = 1
Npoints = 1000

# Here we add our new code to compute a transfer function
def get_TF(base, input_node, amplitude):
    ifo = base.deepcopy()
    ifo.parse(f"""
    fsig(1)
    sgen sig1 {input_node} {amplitude} 0
    #pd1 circ M1.p2.i f=fsig.f   # circulating power
    #pd1 refl M1.p1.o f=fsig.f   # reflected power
    pd1 B8 M3.p2.o f=fsig.f     # measured scattered
    """)
    return ifo.run(Xaxis('fsig.f', 'log', fstart, fstop, Npoints))

out = get_TF(base, 'M3.mech.z', 0.001)
out.plot(log=True)
plt.show()