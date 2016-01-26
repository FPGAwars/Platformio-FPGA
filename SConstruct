import os
from SCons.Script import Environment

# -- Get the user home directory
HOME = os.environ['HOME']

# -- Platformio home user dir
DEST_DIR = HOME + '/.platformio/'

# -- Create the building environment
env = Environment()

# -- Testing: copying one file
file1 = env.File('test.v')
test = env.Install(DEST_DIR, file1)

# -- Install target
env.Alias('install', test)
