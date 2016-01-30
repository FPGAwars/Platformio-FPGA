"""
    Build script for lattice ice40 FPGAs
    latticeice40-builder.py
"""
import os
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, DefaultEnvironment,
                          Environment, Default, Glob)

env = DefaultEnvironment()
env.Replace(PROGNAME="hardware")

TARGET = join(env['BUILD_DIR'], env['PROGNAME'])
TARGET_SIM = env.subst(TARGET)
print("------> TARGET: {}".format(TARGET_SIM))

# -- Get all the source files
src_dir = env.subst('$PROJECTSRC_DIR')
total = join(src_dir, '*.v')
src_files = Glob(total)

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

blif = env.Synth(TARGET, src_files)
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

out = simenv.IVerilog(TARGET_SIM, src_files)
vcd_file = simenv.VCD(out)

waves = simenv.Alias('sim', TARGET_SIM+'.vcd')
AlwaysBuild(waves)

Default([binf])
