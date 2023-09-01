import numpy as np
import math
import sys
from src.plot import Plotter
from src.pile import Pile

plotter = Plotter()

pile = Pile(nx=100, ny=100)

pile.randomize()

momentum = np.ones((pile.nx, pile.ny))
for i in range(2000):
    with open(f"data/array_{i}.dat", "w") as file:
        np.savetxt(file, momentum, fmt="%d")
        #np.savetxt(file, pile.height, fmt="%d")
    for _ in range(10):
        pile.pour(
            probability=0.3,
            stencil=lambda x, y: 10*(1 if math.sqrt((x-0.5)**2 + (y-0.5)**2) < 0.1 else 0)
        )

        pre = np.copy(pile.height)
        pile.iterate(3, inhomogeneity=momentum)
        momentum = np.reciprocal(
            np.minimum(
                np.abs(np.subtract(pre, pile.height)),
                np.ones((pile.nx, pile.ny))
            ).astype(np.float32)
        )

        #plotter.plot2d(pile.height, block=False, interval=0.25)
        plotter.plot2d(momentum, block=False, interval=0.25)