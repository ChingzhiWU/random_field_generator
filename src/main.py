"""
Generate random fields. See 'random_field_funcs.py' for a description.
"""

import matplotlib.pyplot as plt #Library for plotting
import numpy as np #library for multi-dimensional arrays and associated functions
from plot_soil import plotcube
from random_field_funcs import StepwiseCMD_3D_prep, StepwiseCMD_3D_gen, partial_3D_prep, partial_3D_gen

# --- input---

# number of elements in the x,y,z directions
fsize = [20,20,20]
# scale of fluctuation in the x,y,z directions
sof = [10,10,1]
# element sizes in the x,y,z directions
de = [0.5,0.5,0.5]

# use the fully-seperable case (faster, less RAM), otherwise use the partially-seprable case
full_sep = True


# size of the field in metres
fsize_m = [int(fsize[i]/de[i]) for i in range(3)]

if full_sep:
  # pre-process correlation matrix
  L = StepwiseCMD_3D_prep(fsize,sof,de)
  # generate random field
  X = StepwiseCMD_3D_gen(L, fsize_m)
else:
  L = partial_3D_prep(fsize,sof,de)
  # generate random field
  X = partial_3D_gen(L, fsize_m)

# plot 3D field
# note: do exp(X) because plotcube currently assumes it's a lognormally-distributed field and takes the log if it)
plotcube(np.exp(X))

