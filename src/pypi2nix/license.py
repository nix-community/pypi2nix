import re
from typing import Dict
from typing import List
from typing import Optional

from pypi2nix.utils import safe

all_classifiers = {
    "License :: Aladdin Free Public License (AFPL)": None,
    "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication": None,
    "License :: DFSG approved": None,
    "License :: Eiffel Forum License (EFL)": None,
    "License :: Free For Educational Use": None,
    "License :: Free For Home Use": None,
    "License :: Free for non-commercial use": None,
    "License :: Freely Distributable": None,
    "License :: Free To Use But Restricted": None,
    "License :: Freeware": None,
    "License :: Netscape Public License (NPL)": None,
    "License :: Nokia Open Source License (NOKOS)": None,
    "License :: OSI Approved": None,
    "License :: OSI Approved :: Academic Free License (AFL)": "licenses.afl21",
    "License :: OSI Approved :: Apache Software License": "licenses.asl20",
    "License :: OSI Approved :: Apple Public Source License": None,
    "License :: OSI Approved :: Artistic License": "licenses.artistic2",
    "License :: OSI Approved :: Attribution Assurance License": None,
    "License :: OSI Approved :: BSD License": "licenses.bsdOriginal",
    "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)": None,
    "License :: OSI Approved :: Common Public License": "licenses.cpl10",
    "License :: OSI Approved :: Eiffel Forum License": "licenses.efl20",
    "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)": None,
    "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)": None,
    "License :: OSI Approved :: GNU Affero General Public License v3": "licenses.agpl3",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)": "licenses.agpl3Plus",
    "License :: OSI Approved :: GNU Free Documentation License (FDL)": "licenses.fdl13",
    "License :: OSI Approved :: GNU General Public License (GPL)": "licenses.gpl1",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)": "licenses.gpl2",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)": "licenses.gpl2Plus",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)": "licenses.gpl3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)": "licenses.gpl3Plus",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)": "licenses.lgpl2",
    "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)": "licenses.lgpl2Plus",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)": "licenses.lgpl3",
    "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)": "licenses.lgpl3Plus",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)": "licenses.lgpl2",
    "License :: OSI Approved :: IBM Public License": "licenses.ipl10",
    "License :: OSI Approved :: Intel Open Source License": None,
    "License :: OSI Approved :: ISC License (ISCL)": "licenses.isc",
    "License :: OSI Approved :: Jabber Open Source License": None,
    "License :: OSI Approved :: MIT License": "licenses.mit",
    "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)": None,
    "License :: OSI Approved :: Motosoto License": None,
    "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)": "licenses.mpl10",
    "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)": "licenses.mpl11",
    "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)": "licenses.mpl20",
    "License :: OSI Approved :: Nethack General Public License": None,
    "License :: OSI Approved :: Nokia Open Source License": None,
    "License :: OSI Approved :: Open Group Test Suite License": None,
    "License :: OSI Approved :: Python License (CNRI Python License)": None,
    "License :: OSI Approved :: Python Software Foundation License": "licenses.psfl",
    "License :: OSI Approved :: Qt Public License (QPL)": None,
    "License :: OSI Approved :: Ricoh Source Code Public License": None,
    "License :: OSI Approved :: Sleepycat License": "licenses.sleepycat",
    "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)": None,
    "License :: OSI Approved :: Sun Public License": None,
    "License :: OSI Approved :: University of Illinois/NCSA Open Source License": "licenses.ncsa",
    "License :: OSI Approved :: Vovida Software License 1.0": "licenses.vsl10",
    "License :: OSI Approved :: W3C License": "licenses.w3c",
    "License :: OSI Approved :: X.Net License": None,
    "License :: OSI Approved :: zlib/libpng License": "licenses.zlib",
    "License :: OSI Approved :: Zope Public License": "licenses.zpl21",
    "License :: Other/Proprietary License": None,
    "License :: Public Domain": "licenses.publicDomain",
    "License :: Repoze Public License": None,
}


def escape_regex(text: str) -> str:
    return re.escape(text)


LICENSE_PATTERNS: Dict[str, List[str]] = {
    "licenses.zpl21": list(
        map(escape_regex, ["LGPL with exceptions or ZPL", "ZPL 2.1"])
    ),
    "licenses.bsd3": list(map(escape_regex, ["3-Clause BSD License", "BSD-3-Clause"])),
    "licenses.mit": list(
        map(
            escape_regex,
            [
                "MIT",
                "MIT License",
                "MIT or Apache License, Version 2.0",
                "The MIT License",
                "Expat license",
                "MIT license",
            ],
        )
    ),
    "licenses.bsdOriginal": list(
        map(
            escape_regex,
            ["BSD", "BSD License", "BSD-like", "BSD or Apache License, Version 2.0"],
        )
    )
    + ["BSD -.*"],
    "licenses.asl20": list(
        map(
            escape_regex,
            [
                "Apache 2.0",
                "Apache License 2.0",
                "Apache 2",
                "Apache License, Version 2.0",
                "Apache License Version 2.0",
                "http://www.apache.org/licenses/LICENSE-2.0",
            ],
        )
    ),
    "licenses.lgpl3": list(
        map(
            escape_regex,
            ["GNU Lesser General Public License (LGPL), Version 3", "LGPL"],
        )
    ),
    "licenses.lgpl3Plus": list(map(escape_regex, ["LGPLv3+"])),
    "licenses.mpl20": list(
        map(
            escape_regex,
            ["MPL2", "MPL 2.0", "MPL 2.0 (Mozilla Public License)", "MPL-2.0"],
        )
    ),
    "licenses.psfl": list(map(escape_regex, ["Python Software Foundation License"])),
    "licenses.gpl2": list(map(escape_regex, ["GPL version 2"])),
}


def recognized_nix_license_from_classifiers(classifiers: List[str],) -> Optional[str]:
    license_classifiers = [i for i in classifiers if i in all_classifiers]
    for license_classifier in license_classifiers:
        license_nix = all_classifiers[license_classifier]
        if license_nix is not None:
            return license_nix
    return None


def first_license_classifier_from_list(classifiers: List[str]) -> Optional[str]:
    for classifier in classifiers:
        if classifier in all_classifiers:
            escaped_classifier: str = safe(classifier)
            return '"' + escaped_classifier + '"'
    return None


def license_from_string(license_string: str) -> Optional[str]:
    for nix_license, license_patterns in LICENSE_PATTERNS.items():
        for pattern in license_patterns:
            if re.match("^" + pattern + "$", license_string):
                return nix_license
    return None


def find_license(classifiers: List[str], license_string: str) -> Optional[str]:
    return (
        recognized_nix_license_from_classifiers(classifiers)
        or license_from_string(license_string)
        or first_license_classifier_from_list(classifiers)
    )
