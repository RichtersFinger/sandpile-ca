"""Pile of granular material as a collection of grains in a grid-space."""
import random
import math
import numpy as np

class TopplingRuleSets():
    @classmethod
    def BASIC_TOPPLING_RULE(self, diff_topple=1):
        """Returns function to be used as toppling rule."""
        def rule(data, ix, iy, ix2, iy2, inhomogeneity=1):
            """Compares neighbors and returns toppling event or None."""
            if data[ix, iy] + diff_topple*inhomogeneity < data[ix2, iy2]:
                return TopplingEvent(ix, iy, ix2, iy2,
                    (data[ix, iy] - data[ix2, iy2])//2)
            if data[ix, iy] - diff_topple*inhomogeneity > data[ix2, iy2]:
                return TopplingEvent(ix2, iy2, ix, iy,
                    (data[ix2, iy2] - data[ix, iy])//2)
            return None
        return rule

class TopplingEvent():
    def __init__(self, fromx, fromy, tox, toy, amount):
        self.fromx = fromx
        self.fromy = fromy
        self.tox = tox
        self.toy = toy
        self.amount = amount

    def __str__(self):
        return f"{self.amount} "\
            f"from ({self.fromx}, {self.fromy}) "\
            f"to ({self.tox}, {self.toy})"

    def execute(self, data, multiplier=1):
        """Applies the stored event information to data."""
        data[self.fromx, self.fromy] -= int(self.amount/multiplier)
        data[self.tox, self.toy] += int(self.amount/multiplier)
        return None

class Pile():
    """
    Pile of granular material as a collection of grains in a grid-space.

    Keyword arguments:
    nx -- lateral pile resolution in x-direction
          (default 100)
    ny -- lateral pile resolution in y-direction
          (default 100)
    toppling_rule -- function taking arguments data, ix, iy, ix2, iy2
                     to return a TopplingEvent or None if no toppling
    bc -- function to map the boundary condition-appropriate value to
          given index
          (default _periodic_boundary)
    """
    def __init__(self,
        nx=100, ny=100,
        toppling_rule=TopplingRuleSets.BASIC_TOPPLING_RULE(diff_topple=10),
        #boundary_condition=_periodic_boundary
    ):
        self.nx = nx
        self.ny = ny
        self.height = np.zeros((self.nx, self.ny))
        self._toppling_rule = toppling_rule
        self._bc = self._periodic_boundary

        # setup iteration 2d indices in random sequence
        # third value corresponds to distance between lateral locations and
        # is mostly relevant for symmetry
        self._indexpairs = []
        for ix in range(self.nx):
            for iy in range(self.ny):
                self._indexpairs.append([(ix, iy), self._bc(ix + 1, iy), 1])
                self._indexpairs.append([(ix, iy), self._bc(ix, iy + 1), 1])
                self._indexpairs.append(
                    [(ix, iy), self._bc(ix + 1, iy + 1), 1/math.sqrt(2)]
                )
                self._indexpairs.append(
                    [(ix, iy), self._bc(ix - 1, iy + 1), 1/math.sqrt(2)]
                )

    def _periodic_boundary(self, ix, iy):
        """Apply periodic boundary to indices."""
        resx = ix % self.nx
        resy = iy % self.ny
        return resx, resy

    def randomize(self):
        self.height = np.random.randint(0, 15, (self.nx, self.ny))

    def pour(self, nsteps=1, probability = 0.5, stencil=lambda x, y: 1):
        """
        Add/Remove material to/from the pile. The stencil function can be
        used to precisely control the conditions

        Keyword arguments:
        nsteps -- number of iterations
                  (default 1)
        probability -- probability of adding one piece to the pile per iteration
                       (default 0.5)
        stencil -- function expecting 2d-indices [0,1]x[0,1] which returns the
                   average material for deposition/erosion.
                   (default lambda x, y: 1)
        """

        for ix in range(self.nx):
            for iy in range(self.ny):
                x, y = ix/self.nx, iy/self.ny
                for ii in range(nsteps):
                    if random.random() < probability:
                        self.height[ix, iy] += \
                            stencil(x, y)

    def iterate(self, nsteps=1, inhomogeneity=None):
        """
        Apply toppling rules.

        Keyword arguments:
        nsteps -- number of iterations
                  (default 1)
        """

        if inhomogeneity is None:
            inhomogeneity = np.ones((self.nx, self.ny))

        for _ in range(nsteps):
            # permute execution order
            random.shuffle(self._indexpairs)

            # look for toppling events
            for indexpair in self._indexpairs:
                event = self._toppling_rule(
                    self.height, *indexpair[0], *indexpair[1],
                    inhomogeneity=min(
                        inhomogeneity[indexpair[0]],
                        inhomogeneity[indexpair[1]]
                    )
                )
                if event is not None:
                    event.execute(self.height, indexpair[2])
