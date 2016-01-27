##############################
# Icestorm toolchain builder #
##############################

# Generate toolchain-icestorm.tar.gz from installed packages
# This tarball can be unpacked in ~/.platformio/packages

#$MAIN_DIR=/usr
MAIN_DIR=/usr/local
TC_DIR=toolchain-icestorm

## Create filesystem
mkdir ${TC_DIR}
mkdir ${TC_DIR}/bin ${TC_DIR}/share

## Copy bin
cp ${MAIN_DIR}/bin/yosys ${TC_DIR}/bin
cp ${MAIN_DIR}/bin/arachne-pnr ${TC_DIR}/bin
cp ${MAIN_DIR}/bin/icepack ${TC_DIR}/bin
cp ${MAIN_DIR}/bin/iceprog ${TC_DIR}/bin

## Copy share
cp -r ${MAIN_DIR}/share/yosys ${TC_DIR}/share
cp -r ${MAIN_DIR}/share/arachne-pnr ${TC_DIR}/share

# Package
tar -czvf ${TC_DIR}.tar.gz ${TC_DIR}
rm -rf ${TC_DIR}
