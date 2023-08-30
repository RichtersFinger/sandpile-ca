import numpy as np
import math
import sys
from src.plot import Plotter
from src.pile import Pile

plotter = Plotter()

pile = Pile(nx=100, ny=100)

pile.randomize()

for _ in range(100):
    pile.pour(
        stencil=lambda x, y: 1*(1 if math.sqrt((x-0.5)**2 + (y-0.5)**2) < 0.25 else 0)
    )

    pile.iterate()

    plotter.plot2d(pile.height, block=False, interval=0.25)

with open("array.dat", "w") as file:
	np.savetxt(file, pile.height, fmt="%d")