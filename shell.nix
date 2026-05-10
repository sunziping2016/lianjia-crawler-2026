{
  pkgs ? import <nixpkgs> {
    config.cudaSupport = true;
    config.allowUnfree = true;
  },
}:
let
  mypython = pkgs.python3.withPackages (
    ps: with ps; [
      torch
      ultralytics
      aiohttp
    ]
  );
in
pkgs.mkShellNoCC {
  nativeBuildInputs = [
    mypython
  ]
  ++ (with pkgs; [
    nodejs
    pnpm
  ]);
}
