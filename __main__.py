"""
Module containing the demo-usage of the src/pile.py-module.
"""

# FIXME:
# * have different toppling rules w and wo inhomogeneity
# * put video in separate branch

import math
from pathlib import Path
import numpy as np
import scipy
from src.plot import Plotter
from src.pile import Pile, TopplingRuleSets

# configuration
USE_PLOTTER = True # use matplotlib to plot intermediate results
PLOT_HEIGHT = True # plot height or momentum
USE_MOMENTUM = True # use momentum for simualtion
RESOLUTION = (100, 100) # sandpile lattice resolution
SOURCE_RATE = 2 # factor for source term rate
SIMULATION_DURATION = 360 # number of inner-itereation
SIMULATION_DURATION_INNER = 10 # how many iterations per output
WRITE_DATA_FILES = False # write results into matrix-format files
DATA_DIRECTORY = Path("data") # data file output directory
OUTPUT_MOMENTUM = (not PLOT_HEIGHT) or True # calculate/output momentum

# make output directory if needed
if WRITE_DATA_FILES and not DATA_DIRECTORY.is_dir():
    DATA_DIRECTORY.mkdir(parents=True)

# apply configuration
if USE_PLOTTER:
    plotter = Plotter()

if USE_MOMENTUM:
    # w momentum
    # instantiate pile-object with toppling rule that allows for inhomogeneity
    DIFF_TOPPLE = 30
    pile = Pile(
        nx=RESOLUTION[0], ny=RESOLUTION[1],
        toppling_rule=TopplingRuleSets.BASIC_TOPPLING_RULE(diff_topple=DIFF_TOPPLE)
    )
else:
    # wo momentum
    # instantiate pile-object with basic toppling rule
    DIFF_TOPPLE = 15
    pile = Pile(
        nx=RESOLUTION[0], ny=RESOLUTION[1],
        toppling_rule=TopplingRuleSets.BASIC_TOPPLING_RULE(diff_topple=DIFF_TOPPLE)
    )

# randomize start-configuration
pile.randomize()

if USE_MOMENTUM or OUTPUT_MOMENTUM:
    # initialize arrays to keep track of momentum
    momentum_dummy = np.ones((pile.nx, pile.ny))
    momentum = np.ones((pile.nx, pile.ny))
for i in range(SIMULATION_DURATION):
    print(i)

    # write data to disk
    if WRITE_DATA_FILES:
        np.savetxt(DATA_DIRECTORY / f"height_{i}.dat", pile.height, fmt="%d")
        if OUTPUT_MOMENTUM:
            np.savetxt(DATA_DIRECTORY / f"momentum_{i}.dat", momentum, fmt="%f")

    for _ in range(SIMULATION_DURATION_INNER):
        # pour material into system
        pile.pour(
            probability=0.3,
            stencil=lambda x, y: \
                SOURCE_RATE*(1 if math.sqrt((x-0.5)**2 + (y-0.5)**2) < 0.1 else 0)
        )

        if USE_MOMENTUM or OUTPUT_MOMENTUM:
            # save reference
            pre = np.copy(pile.height)

        pile.iterate(1, inhomogeneity=momentum_dummy)

        if USE_MOMENTUM or OUTPUT_MOMENTUM:
            # calculate momentum
            momentum = scipy.ndimage.uniform_filter(
                    np.exp(
                        np.abs(np.subtract(pre, pile.height))
                            /float(DIFF_TOPPLE)*4.0*(-1)
                    ).astype(np.float32),
                size=3, mode="constant"
            )

        if USE_PLOTTER:
            # use matplotlib to show results
            if PLOT_HEIGHT:
                plotter.plot2d(pile.height, block=False, interval=0.05)
            else:
                plotter.plot2d(momentum, block=False, interval=0.05)
