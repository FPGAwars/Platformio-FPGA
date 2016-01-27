import os
from SCons.Script import Environment

# ---------------------- FILES --------------------------
# -- Boards file
BOARDF = 'platformio/boards/fpga_boards.json'

# -- Platform file
PLATF = 'platformio/platforms/lattice_ice40.py'

# -- Build file
BUILDF = 'platformio/platforms/lattice_ice40-builder.py'

# -- Get the user home directory
HOME = os.environ['HOME']

# -- Platformio home user dir
DEST_DIR = HOME + '/.platformio/'

# -- Create the building environment
env = Environment()

# -- Installing files
file1 = env.File(BOARDF)
inst1 = env.Install(DEST_DIR+'/boards/', file1)

file2 = env.File(PLATF)
inst2 = env.Install(DEST_DIR+'/platforms/', file2)

file3 = env.File(BUILDF)
inst3 = env.Install(DEST_DIR+'/platforms/', file3)


# -- Install target
env.Alias('install', [inst1, inst2, inst3])
