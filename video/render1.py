# /media/srichters/Storage/XPrograms/blender-2.91.0-linux64/blender --background -P test.py
# ffmpeg -framerate 60 -i res/frame%05d.png -c:v libx264 video.mp4

import bpy
import math
from pathlib import Path

PLATE_WIDTH = 1.43587
CUBE_REFERENCE_WIDTH = 0.2
CUBE_REFERENCE_HEIGHT = 15.8519
PILE_VERTICAL_OFFSET = -0.1


bpy.ops.wm.open_mainfile(filepath="render.blend")
scn = bpy.context.scene

# read current data
data = Path("array.dat").read_text(encoding="utf8")
height_array = []
for line in data.split("\n"):
    if line != "":
        row = [int(x) for x in line.split()]
        height_array.append(row)
nx = len(height_array[0])
ny = len(height_array)

# get column dimensions as
desired_width = PLATE_WIDTH/max(nx, ny) * 0.9 / math.sqrt(2) / 2

# load reference and scale accordingly
reference_cube = bpy.data.objects["Cube_Reference"]
reference_cube.location = (0, 0, -2*CUBE_REFERENCE_HEIGHT)
reference_cube.scale = (desired_width, desired_width, 0.1)

objects = []
for row in height_array:
    thisrow = []
    for value in row:
        column = reference_cube.copy()
        column.data = reference_cube.data.copy()
        scn.collection.objects.link(column)
        thisrow.append(column)
    objects.append(thisrow)

# position columns
for ix, row in enumerate(objects):
    for iy, column in enumerate(row):
        column.location = (
            -desired_width*nx + 2*ix*desired_width,
            -desired_width*ny + 2*iy*desired_width,
            -CUBE_REFERENCE_HEIGHT + PILE_VERTICAL_OFFSET \
                + desired_width*height_array[ix][iy]
        )

bpy.ops.wm.save_as_mainfile(filepath="render_.blend")

nframes = 0

frame0 = 0
frame1 = nframes
for i in range(frame0, frame1 + 1, 1):
    bpy.context.scene.render.filepath = f"res/frame{i}.png"
    bpy.ops.render.render(write_still = True)
    print("frame " + str(1 + i - frame0) + "/" + str(1 + frame1 - frame0) + " done")