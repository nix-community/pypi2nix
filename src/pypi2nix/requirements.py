import os
import platform
import sys

import parsley
from setuptools._vendor.packaging.utils import canonicalize_name

from pypi2nix.package_source import GitSource
from pypi2nix.package_source import HgSource
from pypi2nix.package_source import UrlSource


class ParsingFailed(Exception):
    pass


class IncompatibleRequirements(Exception):
    pass


class Requirement:
    def __init__(self, name, extras=[], version=[], environment_markers=None, url=None):
        if bool(version) and bool(url):
            raise ParsingFailed(
                "Cannot construct requirement `{name}` with version and url specifier set at the same time".format(
                    name=name
                )
            )
        self.name = canonicalize_name(name)
        self.extras = extras
        self.version = version
        self.environment_markers = environment_markers
        self.url = url
        self._source = None

    def add(self, other, target_platform):
        if not self.applies_to_target(target_platform):
            return other
        if not other.applies_to_target(target_platform):
            return self
        if self.name != other.name:
            raise IncompatibleRequirements(
                "Cannot add requirements with different names, given `{}` and `{}`".format(
                    self.name, other.name
                )
            )
        if self.url and other.url:
            if self.url == other.url:
                url = self.url
                version = []
            else:
                raise IncompatibleRequirements(
                    "Cannot add requirements with different URLs, given `{}` and `{}`".format(
                        self.url, other.url
                    )
                )
        elif self.url or other.url:
            version = []
            url = self.url or other.url
        else:
            version = self.version + other.version
            url = None
        environment_marker = None
        return Requirement(
            name=self.name,
            extras=self.extras + other.extras,
            version=version,
            environment_markers=environment_marker,
            url=url,
        )

    @classmethod
    def from_line(constructor, line):
        name, extras, versions_or_url, markers = requirement_parser.parse(line)
        if isinstance(versions_or_url, list):
            versions = versions_or_url
            url = None
        else:
            versions = []
            url = versions_or_url
        return constructor(name, extras, versions, markers, url)

    @property
    def source(self):
        if self._source is None:
            if self.url is None:
                pass
            elif self.url.startswith("git+"):
                self.handle_git_source(self.url[4:])
            elif self.url.startswith("git://"):
                self.handle_git_source(self.url)
            elif self.url.startswith("hg+"):
                self.handle_hg_source(self.url[3:])
            else:
                self._source = UrlSource(url=self.url)
        return self._source

    def handle_hg_source(self, url):
        try:
            url, rev = url.split("@")
        except ValueError:
            self._source = HgSource(url=url)
        else:
            self._source = HgSource(url=url, revision=rev)

    def handle_git_source(self, url):
        try:
            url, rev = url.split("@")
        except ValueError:
            self._source = GitSource(url=url)
        else:
            self._source = GitSource(url=url, revision=rev)

    def applies_to_target(self, target_platform):
        mapping = {
            RequirementParser.PYTHON_VERSION: ".".join(
                target_platform.version.split(".")[:2]
            )
        }

        def evaluate_marker(marker):
            if not isinstance(marker, tuple):
                return marker
            operation, left, right = marker
            left = mapping.get(left, left)
            right = mapping.get(right, right)
            if operation == "or":
                return evaluate_marker(left) or evaluate_marker(right)
            elif operation == "and":
                return evaluate_marker(left) and evaluate_marker(right)
            elif operation == "in":
                return evaluate_marker(left) in evaluate_marker(right)
            elif operation == "not in":
                return evaluate_marker(left) not in evaluate_marker(right)
            elif operation == "==":
                return evaluate_marker(left) == evaluate_marker(right)
            elif operation == "!=":
                return evaluate_marker(left) != evaluate_marker(right)
            raise Exception("Unknown operation: {}".format(operation))

        return (
            True
            if self.environment_markers is None
            else evaluate_marker(self.environment_markers)
        )

    def to_line(self):
        if self.url:
            line = self.url + "#egg=" + self.name
        elif self.version:
            line = self.name
            versions_line = ",".join(
                [
                    " {operator} {version}".format(operator=operator, version=version)
                    for operator, version in self.version
                ]
            )
            line += versions_line
        else:
            line = self.name
        return line


class RequirementParser:
    def __init__(self):
        self._compiled_grammar = None

    requirement_grammar = """
        wsp           = ' ' | '\t'
        version_cmp   = wsp* <'<=' | '<' | '!=' | '==' | '>=' | '>' | '~=' | '==='>
        version       = wsp* <( letterOrDigit | '-' | '_' | '.' | '*' | '+' | '!' )+>
        version_one   = version_cmp:op version:v wsp* -> (op, v)
        version_many  = version_one:v1 (wsp* ',' version_one)*:v2 -> [v1] + v2
        versionspec   = ('(' version_many:v ')' ->v) | version_many
        urlspec       = '@' wsp* <URI_reference>
        python_str_c  = (wsp | letter | digit | '(' | ')' | '.' | '{' | '}' |
                         '-' | '_' | '*' | '#' | ':' | ';' | ',' | '/' | '?' |
                         '[' | ']' | '!' | '~' | '`' | '@' | '$' | '%' | '^' |
                         '&' | '=' | '+' | '|' | '<' | '>' )
        dquote        = '"'
        squote        = '\\''
        python_str    = (squote <(python_str_c | dquote)*>:s squote |
                         dquote <(python_str_c | squote)*>:s dquote) -> s
        env_var       = ('python_version' | 'python_full_version' |
                         'os_name' | 'sys_platform' | 'platform_release' |
                         'platform_system' | 'platform_version' |
                         'platform_machine' | 'platform_python_implementation' |
                         'implementation_name' | 'implementation_version' |
                         'python_implementation' | 'extra'
                         # ONLY when defined by a containing layer
                         ):varname -> lookup(varname)
        marker_var    = wsp* (env_var | python_str)
        marker_expr   = marker_var:l marker_op:o marker_var:r -> (o, l, r)
                      | wsp* '(' marker:m wsp* ')' -> m
        marker_op     = version_cmp | (wsp* 'in') | (wsp* 'not' wsp+ 'in' -> 'not in')
        marker_and    = marker_expr:l wsp* 'and' marker_expr:r -> ('and', l, r)
                      | marker_expr:m -> m
        marker_or     = marker_and:l wsp* 'or' marker_and:r -> ('or', l, r)
                          | marker_and:m -> m
        marker        = marker_or
        quoted_marker = ';' wsp* marker
        identifier_end = letterOrDigit | (('-' | '_' | '.' )* letterOrDigit)
        identifier    = < letterOrDigit identifier_end* >
        name          = identifier
        extras_list   = identifier:i (wsp* ',' wsp* identifier)*:ids -> [i] + ids
        extras        = '[' wsp* extras_list?:e wsp* ']' -> e
        name_req      = (name:n wsp* extras?:e wsp* versionspec?:v wsp* quoted_marker?:m
                         -> (n, e or [], v or [], m))
        url_req       = (name:n wsp* extras?:e wsp* urlspec:v (wsp+ | end) quoted_marker?:m
                         -> (n, e or [], v or [], m))
        url_req_pip_style = (('-e' wsp+)? (('hg+' | 'git+')?:p <URI_reference_pip_style>:s -> (p or "") + s):v
                            '#egg=' name:n -> (n, [], v or [], None))
        specification = wsp* ( url_req_pip_style | url_req | name_req ):s wsp* -> s
        # The result is a tuple - name, list-of-extras,
        # list-of-version-constraints-or-a-url, marker-ast or None


        URI_reference = <URI | relative_ref>
        URI_reference_pip_style = <URI_pip_style | relative_ref>
        URI           = scheme ':' hier_part ('?' query )? ( '#' fragment)?
        URI_pip_style = scheme ':' hier_part ('?' query )?
        hier_part     = ('//' authority path_abempty) | path_absolute | path_rootless | path_empty
        absolute_URI  = scheme ':' hier_part ( '?' query )?
        relative_ref  = relative_part ( '?' query )? ( '#' fragment )?
        relative_part = '//' authority path_abempty | path_absolute | path_noscheme | path_empty
        scheme        = letter ( letter | digit | '+' | '-' | '.')*
        authority     = ( userinfo '@' )? host ( ':' port )?
        userinfo      = ( unreserved | pct_encoded | sub_delims | ':')*
        host          = IP_literal | IPv4address | reg_name
        port          = digit*
        IP_literal    = '[' ( IPv6address | IPvFuture) ']'
        IPvFuture     = 'v' hexdig+ '.' ( unreserved | sub_delims | ':')+
        IPv6address   = (
                          ( h16 ':'){6} ls32
                          | '::' ( h16 ':'){5} ls32
                          | ( h16 )?  '::' ( h16 ':'){4} ls32
                          | ( ( h16 ':')? h16 )? '::' ( h16 ':'){3} ls32
                          | ( ( h16 ':'){0,2} h16 )? '::' ( h16 ':'){2} ls32
                          | ( ( h16 ':'){0,3} h16 )? '::' h16 ':' ls32
                          | ( ( h16 ':'){0,4} h16 )? '::' ls32
                          | ( ( h16 ':'){0,5} h16 )? '::' h16
                          | ( ( h16 ':'){0,6} h16 )? '::' )
        h16           = hexdig{1,4}
        ls32          = ( h16 ':' h16) | IPv4address
        IPv4address   = dec_octet '.' dec_octet '.' dec_octet '.' dec_octet
        nz            = ~'0' digit
        dec_octet     = (
                          digit # 0-9
                          | nz digit # 10-99
                          | '1' digit{2} # 100-199
                          | '2' ('0' | '1' | '2' | '3' | '4') digit # 200-249
                          | '25' ('0' | '1' | '2' | '3' | '4' | '5') )# %250-255
        reg_name = ( unreserved | pct_encoded | sub_delims)*
        path = (
                path_abempty # begins with '/' or is empty
                | path_absolute # begins with '/' but not '//'
                | path_noscheme # begins with a non-colon segment
                | path_rootless # begins with a segment
                | path_empty ) # zero characters
        path_abempty  = ( '/' segment)*
        path_absolute = '/' ( segment_nz ( '/' segment)* )?
        path_noscheme = segment_nz_nc ( '/' segment)*
        path_rootless = segment_nz ( '/' segment)*
        path_empty    = pchar{0}
        segment       = pchar*
        segment_nz    = pchar+
        segment_nz_nc = ( unreserved | pct_encoded | sub_delims | '@')+
                        # non-zero-length segment without any colon ':'
        pchar         = unreserved | pct_encoded | sub_delims | ':' | '@'
        query         = ( pchar | '/' | '?')*
        fragment      = ( pchar | '/' | '?')*
        pct_encoded   = '%' hexdig
        unreserved    = letter | digit | '-' | '.' | '_' | '~'
        reserved      = gen_delims | sub_delims
        gen_delims    = ':' | '/' | '?' | '#' | '(' | ')?' | '@'
        sub_delims    = '!' | '$' | '&' | '\\'' | '(' | ')' | '*' | '+' | ',' | ';' | '='
        hexdig        = digit | 'a' | 'A' | 'b' | 'B' | 'c' | 'C' | 'd' | 'D' | 'e' | 'E' | 'f' | 'F'
    """

    def format_full_version(self, info):
        version = "{0.major}.{0.minor}.{0.micro}".format(info)
        kind = info.releaselevel
        if kind != "final":
            version += kind[0] + str(info.serial)
        return version

    def environment_bindings(self):
        if hasattr(sys, "implementation"):
            implementation_version = self.format_full_version(
                sys.implementation.version
            )
            implementation_name = sys.implementation.name
        else:
            implementation_version = "0"
            implementation_name = ""
        bindings = {
            "implementation_name": implementation_name,
            "implementation_version": implementation_version,
            "os_name": os.name,
            "platform_machine": platform.machine(),
            "platform_python_implementation": platform.python_implementation(),
            "python_implementation": platform.python_implementation(),
            "platform_release": platform.release(),
            "platform_system": platform.system(),
            "platform_version": platform.version(),
            "python_full_version": platform.python_version(),
            "python_version": RequirementParser.PYTHON_VERSION,
            "sys_platform": sys.platform,
        }
        return bindings

    def compiled_grammar(self):
        if self._compiled_grammar is None:
            self._compiled_grammar = parsley.makeGrammar(
                self.requirement_grammar, {"lookup": self.environment_bindings().get}
            )
        return self._compiled_grammar

    def parse(self, line):
        line = line.strip()
        if "\n" in line:
            raise ParsingFailed(
                "Failed to parse requirement from string `{}`".format(line)
            )
        try:
            return self.compiled_grammar()(line).specification()
        except parsley.ParseError as e:
            raise ParsingFailed("{message}".format(message=e.formatError()))

    PYTHON_VERSION = object()


requirement_parser = RequirementParser()
