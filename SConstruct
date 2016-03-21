import os
from os.path import join
from os.path import expanduser
from SCons.Script import Environment

# ---------------------- FILES --------------------------
# -- Boards file
BOARDF = join('platformio', 'boards', 'lattice.json')

# -- Platform file
PLATF = join('platformio', 'platforms', 'lattice_ice40.py')

# -- Build file
BUILDF = join('platformio', 'builder', 'scripts', 'lattice_ice40.py')

# -- Get the user home directory
HOME = expanduser("~")

# -- Platformio home user dir
DEST_DIR = join(HOME, '.platformio')

# -- Create the building environment
env = Environment()

# -- Installing files
file1 = env.File(BOARDF)
inst1 = env.Install(join(DEST_DIR, 'boards'), file1)

file2 = env.File(PLATF)
inst2 = env.Install(join(DEST_DIR, 'platforms'), file2)

file3 = env.File(BUILDF)
inst3 = env.InstallAs(join(DEST_DIR, 'platforms', 'lattice_ice40-builder.py'),
                      file3)


# -- Install target
env.Alias('install', [inst1, inst2, inst3])
