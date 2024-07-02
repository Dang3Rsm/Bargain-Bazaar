{pkgs}: {
  deps = [
    pkgs.sqlite
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
  ];
}
