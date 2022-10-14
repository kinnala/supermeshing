{
  description = "supermeshing: Python wrapper to libsupermesh";

  inputs = {
    libsupermesh.url = "git+https://bitbucket.org/libsupermesh/libsupermesh.git";
    libsupermesh.flake = false;
  };

  outputs = { self, nixpkgs, libsupermesh }: {
    packages.x86_64-linux.libsupermesh =
      with import nixpkgs { system = "x86_64-linux"; };
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
          mkdir -p $out/lib
          mv $TMP/source/build/libsupermesh.a $out/lib
        '';
      };
    packages.x86_64-linux.default = self.packages.x86_64-linux.libsupermesh;
  };               
}
