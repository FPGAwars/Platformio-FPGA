##############################
# Icestorm toolchain builder #
##############################

# Generate toolchain-icestorm.tar.gz from source code
# sources: http://www.clifford.at/icestorm/
# This tarball can be unpacked in ~/.platformio/packages

TCDIR=$PWD/toolchain-icestorm

# Go to code directory
if [ -z "$1" ]; then
    echo "Add your code directory. Ex: ., .., ~/code"
    exit 1
fi
cd $1

# Install dependencies
sudo apt-get install build-essential clang bison flex libreadline-dev \
                     gawk tcl-dev libffi-dev git mercurial graphviz   \
                     xdot pkg-config python python3 libftdi-dev

# Instal Icestorm
git -C icestorm pull || git clone https://github.com/cliffordwolf/icestorm.git icestorm
cd icestorm
make -j$nproc
make install DESTDIR=$TCDIR PREFIX=""
cd ..

# Install Arachne-PNR
git -C arachne-pnr pull || git clone https://github.com/cseed/arachne-pnr.git arachne-pnr
cd arachne-pnr
make -j$nproc
make install DESTDIR=$TCDIR PREFIX=""
cd ..

# Install Yosys
git -C yosys pull || git clone https://github.com/cliffordwolf/yosys.git yosys
cd yosys
make -j$nproc
make install DESTDIR=$TCDIR PREFIX=""
cd ..

# Package tarball
tar -czvf $TCDIR.tar.gz $TCDIR

# Install toolchain into local
cp -r $TCDIR $HOME/.platformio/packages/
rm -r $TCDIR
