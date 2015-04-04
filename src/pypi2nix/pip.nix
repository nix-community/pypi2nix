{ path }:
let
  pkgs = import <nixpkgs> {};

in pkgs.stdenv.mkDerivation rec {
  name = "pypi2nix-pip-bootstrapping";
  __noChroot = true;
  buildInputs = [ pkgs.strace pkgs.which pkgs.wget pkgs.makeWrapper pkgs.python ];
  buildCommand = ''
    unset http_proxy
    unset https_proxy
    unset ftp_proxy

    mkdir tmp-bin
    ln -s `which python` tmp-bin/python
    wrapProgram tmp-bin/python \
        --set  PYTHONUSERBASE "`pwd`/tmp"

    export PYTHONUSERBASE=./tmp
    export PATH=./tmp-bin:$PATH

    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py --user

    python ./tmp/bin/pip install ${path} --user
    PYTHONPATH=$PYTHONUSERBASE/lib/python2.7/site-packages python ./tmp/bin/pip freeze > requirements.txt

    mkdir $out
    cp requirements.txt $out/
  '';
}
