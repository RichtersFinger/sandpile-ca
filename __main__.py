import numpy as np
import scipy
import math
import sys
from src.plot import Plotter
from src.pile import Pile, TopplingRuleSets

plotter = Plotter()

DIFF_TOPPLE = 30

pile = Pile(
    nx=100, ny=100,
    toppling_rule=TopplingRuleSets.BASIC_TOPPLING_RULE(diff_topple=DIFF_TOPPLE)
)

pile.randomize()

momentum = np.ones((pile.nx, pile.ny))
for i in range(3600):
    print(i)

    with open(f"data/height_{i}.dat", "w") as file:
        np.savetxt(file, pile.height, fmt="%d")

    with open(f"data/momentum_{i}.dat", "w") as file:
        np.savetxt(file, momentum, fmt="%f")

    for _ in range(1):
        pile.pour(
            probability=0.3,
            stencil=lambda x, y: 2*(1 if math.sqrt((x-0.5)**2 + (y-0.5)**2) < 0.1 else 0)
            #stencil=lambda x, y: 5*(1 if math.sqrt((x-0.5)**2 + (y-0.5)**2) < 0.1 else 0)
        )

        pre = np.copy(pile.height)
        pile.iterate(1, inhomogeneity=momentum)
        #pile.iterate(3, inhomogeneity=momentum)
        momentum = scipy.ndimage.uniform_filter(
                np.exp(
                    np.abs(np.subtract(pre, pile.height))
                        /float(DIFF_TOPPLE)*4.0*(-1)
                ).astype(np.float32),
            size=3, mode="constant"
        )

        #plotter.plot2d(pile.height, block=False, interval=0.25)
        plotter.plot2d(momentum, block=False, interval=0.05)
