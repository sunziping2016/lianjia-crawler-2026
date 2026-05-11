{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShellNoCC {
  nativeBuildInputs = with pkgs; [
    # dev dependencies
    python3
    uv

    # dev helpers
    process-compose
  ];

  shellHook = ''
    if [[ ! -d .venv ]]; then
      uv venv
    fi
    uv sync
    source .venv/bin/activate
  '';
}
