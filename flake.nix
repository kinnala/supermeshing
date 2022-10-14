{
  description = "supermeshing: Python wrapper to libsupermesh";

  inputs = {
    libsupermesh.url = "git+https://bitbucket.org/libsupermesh/libsupermesh.git";
    libsupermesh.flake = false;
  };

  outputs = { self, nixpkgs, libsupermesh }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      python-numpy = pkgs.python3.withPackages(ps: with ps; [ numpy ]);
    in {
      packages.x86_64-linux.libsupermesh =
        with pkgs;
        stdenv.mkDerivation {
          name = "libsupermesh";
          src = libsupermesh;
          nativeBuildInputs = [
            cmake
            gfortran
            mpich
          ];
          buildPhase = "make -j $NIX_BUILD_CORES";
          installPhase = ''
            mkdir -p $out
            mv $TMP/source/build/* $out
          '';
        };
      packages.x86_64-linux.supermeshing-bin =
        with pkgs;
        stdenv.mkDerivation {
          name = "supermeshing-bin";
          src = self;
          nativeBuildInputs = [
            gfortran
            mpich
            python-numpy
          ];
          buildInputs = [
            self.packages.x86_64-linux.libsupermesh
          ];
          buildPhase = "f2py3 -c --fcompiler=gfortran --f90exec=mpif90 -L${self.packages.x86_64-linux.libsupermesh.out} -I${self.packages.x86_64-linux.libsupermesh.out}/include -lsupermesh -lstdc++ -m supermeshing_fortran supermeshing/supermeshing.f90";
          installPhase = ''
            mkdir -p $out/supermeshing
            mv $TMP/source/*.so $out/supermeshing
            mv $TMP/source/supermeshing/*.py $out/supermeshing
            mv $TMP/source/setup.py $out
          '';
        };
      packages.x86_64-linux.default =
        with pkgs;
        python310Packages.buildPythonPackage {
          name = "supermeshing";
          version = "0.0.1";
          src = self.packages.x86_64-linux.supermeshing-bin;
          propagatedBuildInputs = [ python3Packages.numpy ];
        };
      devShells.x86_64-linux.default =
        with pkgs;
        (python310.withPackages (ps: with ps; [
          self.packages.x86_64-linux.default
          numpy
          scipy
          matplotlib
          meshio
          ipython
        ])).env;
    };
}
