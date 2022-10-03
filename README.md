(in conda environment)
git clone https://bitbucket.org/libsupermesh/libsupermesh.git
nix-shell -p gfortran cmake mpichh glibc
cd libsupermesh/build
cmake ..
make
cp -r * ../..
cd ../..
f2py3 -c --fcompiler=gfortran --f90exec=mpif90 -L. -I./include -lsupermesh -lstdc++ -m testlib test.f90
