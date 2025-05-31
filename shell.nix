{
  pkgs ? import <nixpkgs> {},
}:
pkgs.mkShell {
  name = "fcitx5-table-extra";  
  packages = with pkgs; [
    python3
    pyright
  ];
}
