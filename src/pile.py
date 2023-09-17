"""Pile of granular material as a height profile defined on a discrete 2d-lattice."""
import random
import math
import numpy as np

class TopplingRuleSets():
    """Container class for a collection of toppling rule generators."""
    @classmethod
    def BASIC_TOPPLING_RULE(cls, diff_topple=15):
        """Returns function to be used as toppling rule."""
        def rule(data, ix, iy, ix2, iy2):
            """Compares neighbors and returns toppling event or None."""
            if data[ix, iy] + diff_topple < data[ix2, iy2]:
                return TopplingEvent((ix, iy), (ix2, iy2),
                    (data[ix, iy] - data[ix2, iy2])//2)
            if data[ix, iy] - diff_topple > data[ix2, iy2]:
                return TopplingEvent((ix2, iy2), (ix, iy),
                    (data[ix2, iy2] - data[ix, iy])//2)
            return None
        return rule

    @classmethod
    def INHOMOGENEOUS_TOPPLING_RULE(cls, diff_topple=15):
        """Returns function to be used as toppling rule."""
        def rule(data, ix, iy, ix2, iy2, inhomogeneity):
            """
            Compares neighbors and returns toppling event or None;
            Makes use of inhomogeneity array to modify topple threshold.
            """
            if data[ix, iy] + diff_topple*min(
                        inhomogeneity[ix, iy],
                        inhomogeneity[ix2, iy2]
                    ) < data[ix2, iy2]:
                return TopplingEvent((ix, iy), (ix2, iy2),
                    (data[ix, iy] - data[ix2, iy2])//2)
            if data[ix, iy] - diff_topple*min(
                        inhomogeneity[ix, iy],
                        inhomogeneity[ix2, iy2]
                    ) > data[ix2, iy2]:
                return TopplingEvent((ix2, iy2), (ix, iy),
                    (data[ix2, iy2] - data[ix, iy])//2)
            return None
        return rule

class TopplingEvent():
    """
    Class that describes a toppling event via transport coordinates and
    volume.

    Keyword arguments:
    _from -- 2-tuple origin of mass transport
    _to -- 2-tuple target of mass transport
    _amount -- transport volume
    """
    def __init__(self, _from, _to, _amount):
        self.fromx = _from[0]
        self.fromy = _from[1]
        self.tox = _to[0]
        self.toy = _to[1]
        self.amount = _amount

    def __str__(self):
        return f"{self.amount} "\
            f"from ({self.fromx}, {self.fromy}) "\
            f"to ({self.tox}, {self.toy})"

    def execute(self, data, multiplier=1):
        """
        Applies the stored event information to np array.

        Keyword arguments:
        data -- 2d np-array containing pile
        multiplier -- multiplier for transport volume (reciprocal)
        """
        data[self.fromx, self.fromy] -= int(self.amount/multiplier)
        data[self.tox, self.toy] += int(self.amount/multiplier)

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
    """
    def __init__(self,
        nx=100, ny=100,
        toppling_rule=TopplingRuleSets.BASIC_TOPPLING_RULE(diff_topple=10)
    ):
        self.nx = nx
        self.ny = ny
        self.height = np.zeros((self.nx, self.ny))
        self._toppling_rule = toppling_rule
        self._bc = self._periodic_boundary

        # setup iteration of 2d indices in random sequence
        # third value corresponds to distance in lateral position and
        # is mostly relevant for symmetry in the simulation result
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
        """Randomize height profile."""
        self.height = np.random.randint(0, 15, (self.nx, self.ny))

    def pour(self, nsteps=1, probability = 0.5, stencil=lambda x, y: 0):
        """
        Add/Remove material to/from the pile. The stencil function can be
        used to precisely control the conditions

        Keyword arguments:
        nsteps -- number of iterations
                  (default 1)
        probability -- probability of adding one piece to the pile per iteration
                       (default 0.5)
        stencil -- function expecting 2d-indices [0,nx-1]x[0,ny-1] which returns
                   the average material for deposition/erosion.
                   (default lambda x, y: 0)
        """

        for ix in range(self.nx):
            for iy in range(self.ny):
                x, y = ix/self.nx, iy/self.ny
                for _ in range(nsteps):
                    if random.random() < probability:
                        self.height[ix, iy] += \
                            stencil(x, y)

    def iterate(self, nsteps=1, **kwargs):
        """
        Apply toppling rules.

        Keyword arguments:
        nsteps -- number of iterations
                  (default 1)
        """

        for _ in range(nsteps):
            # permute execution order
            random.shuffle(self._indexpairs)

            # look for toppling events
            for indexpair in self._indexpairs:
                event = self._toppling_rule(
                    self.height, *indexpair[0], *indexpair[1],
                    **kwargs
                )
                if event is not None:
                    event.execute(self.height, indexpair[2])
