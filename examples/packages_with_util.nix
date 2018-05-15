let
  pythonPackages = import ./packages_with.nix {};
in
{
  "flake8" = pythonPackages.interpreterWithPackages (p: [p.flake8]);
  "tornado" = pythonPackages.interpreterWithPackages (p: [p.tornado]);
}
