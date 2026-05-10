{
  pkgs ? import <nixpkgs> {
    config.cudaSupport = true;
    config.allowUnfree = true;
  },
}:
let
  inherit (pkgs) lib;
  pyproject = lib.importTOML ./pyproject.toml;
  pylianjia-crawler = pkgs.python3Packages.mkPythonEditablePackage {
    pname = pyproject.project.name;
    version = pyproject.project.version;
    build-system = [ pkgs.python3Packages.uv-build ];
    dependencies = with pkgs.python3Packages; [
      torch
      ultralytics
      aiohttp
    ];
    root = "$PRJ_ROOT";
    scripts = pyproject.project.scripts or { };
  };
in
pkgs.mkShellNoCC {
  nativeBuildInputs = with pkgs; [
    # dev dependencies
    nodejs
    pnpm
    (python3.withPackages (ps: [ pylianjia-crawler ]))
    uv

    # dev helpers
    watchexec
    process-compose
  ];
  shellHook = ''
    export PRJ_ROOT=$PWD
  '';
}
