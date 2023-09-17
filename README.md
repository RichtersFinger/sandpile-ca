`sandpile-ca` is a simple python program which can be used to simulate
deposition and erosion processes, like piling up sand, on a two-dimensional
lattice-space.

# Dependencies
* (Linux) packages

  `python3-tk`
* python packages

  `numpy`, `matplotlib`, `bpy`

# Run
Run the simulation with
```
python3 .
```

# Configuration
The file `__main__.py` contains a block of configuration definitions:
```
...
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
...
```
which can easily be modified to your liking.
