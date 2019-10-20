{ pkgs, python }:

self: super: {

   "python-ldap" = python.overrideDerivation super."python-ldap" (old: {
      NIX_CFLAGS_COMPILE = "-I${pkgs.cyrus_sasl.dev}/include/sasl";
   });
}
