"""
    Build script for lattice ice40 FPGAs
    latticeice40-builder.py
"""
import os
from os.path import join, split
from SCons.Script import (AlwaysBuild, Builder, DefaultEnvironment,
                          Environment, Default, Glob)

env = DefaultEnvironment()
env.Replace(PROGNAME="hardware")

# -- Target name for synthesis
TARGET = join(env['BUILD_DIR'], env['PROGNAME'])

# -- Target name for simulation
TARGET_SIM = join(env['PROJECTSRC_DIR'], env['PROGNAME'])

# -- Get a list of all the verilog files in the src folfer, in ASCII, with
# -- the full path. All these files are used for the simulation
v_nodes = Glob(join(env['PROJECTSRC_DIR'], '*.v'))
src_sim = ["{}".format(f) for f in v_nodes]

# --------- Get the Testbench file (there should be only 1)
# -- Create a list with all the files finished in _tb.v. It should contain
# -- the test bench
list_tb = [f for f in src_sim if f[-5:].upper() == "_TB.V"]

# -- TODO: error checking
testbench = list_tb[0]

# -------- Get the synthesis files.  They are ALL the files except the
# -------- testbench
src_synth = [f for f in src_sim if f != testbench]

# -- For debugging
print("Testbench: {}".format(testbench))
print("Synth files: {}".format(src_synth))
print("Sim files: {}".format(src_sim))
print("")

# -- Get the PCF file
src_dir = env.subst('$PROJECTSRC_DIR')
PCFs = join(src_dir, '*.pcf')
PCF = Glob(PCFs)

bin_dir = join('$PIOPACKAGES_DIR', 'toolchain-icestorm', 'bin')

# -- Builder 1 (.v --> .blif)
synth = Builder(action=join(bin_dir, 'yosys') +
                ' -p \"synth_ice40 -blif {}.blif\" $SOURCES'.format(TARGET),
                suffix='.blif',
                src_suffix='.v')

# -- Builder 2 (.blif --> .asc)
pnr = Builder(action=join(bin_dir, 'arachne-pnr') +
              ' -d 1k -o $TARGET -p {} $SOURCE'.format(PCF[0]),
              suffix='.asc',
              src_suffix='.blif')

# -- Builder 3 (.asc --> .bin)
bitstream = Builder(action=join(bin_dir, 'icepack') + ' $SOURCE $TARGET',
                    suffix='.bin',
                    src_suffix='.asc')

# -- Builder 4 (.asc --> .rpt)
time_rpt = Builder(action='icetime -mtr $TARGET $SOURCE',
                   suffix='.rpt',
                   src_suffix='.asc')

env.Append(BUILDERS={'Synth': synth, 'PnR': pnr, 'Bin': bitstream,
                     'Time': time_rpt})

blif = env.Synth(TARGET, src_synth)
asc = env.PnR([blif, PCF[0]])
binf = env.Bin(asc)

upload = env.Alias('upload', binf, join(bin_dir, 'iceprog') + ' $SOURCE')
AlwaysBuild(upload)

# -- Target for calculating the time (.rpt)
# rpt = env.Time(asc)
t = env.Alias('time', env.Time('time.rpt', asc))

# -------------------- Simulation ------------------
# -- Constructor para generar simulacion: icarus Verilog
iverilog = Builder(action='iverilog $SOURCES -o $TARGET',
                   suffix='.out',
                   src_suffix='.v')

vcd = Builder(action='./$SOURCE', suffix='.vcd', src_suffix='.out')

simenv = Environment(BUILDERS={'IVerilog': iverilog, 'VCD': vcd},
                     ENV=os.environ)

out = simenv.IVerilog(TARGET_SIM, src_sim)
vcd_file = simenv.VCD(out)

waves = simenv.Alias('sim', TARGET_SIM+'.vcd')
AlwaysBuild(waves)

Default([binf])
