"""
utils.py

Utility/Helper functions for this project.
"""


cc_licenses = [
    {
        "identifier": "CC0",
        "rights": "Creative Commons Zero v1.0 Universal",
        "rights_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
    {
        "identifier": "CC BY 4.0",
        "rights": "Creative Commons Attribution 4.0 International",
        "rights_uri": "https://creativecommons.org/licenses/by/4.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
    {
        "identifier": "CC BY-SA 4.0",
        "rights": "Creative Commons Attribution-ShareAlike 4.0 International",
        "rights_uri": "https://creativecommons.org/licenses/by-sa/4.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
    {
        "identifier": "CC BY-NC 4.0",
        "rights": "Creative Commons Attribution-NonCommercial 4.0 International",
        "rights_uri": "https://creativecommons.org/licenses/by-nc/4.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
    {
        "identifier": "CC BY-ND 4.0",
        "rights": "Creative Commons Attribution-NoDerivatives 4.0 International",
        "rights_uri": "https://creativecommons.org/licenses/by-nd/4.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
    {
        "identifier": "CC BY-NC-SA 4.0",
        "rights": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
        "rights_uri": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
    {
        "identifier": "CC BY-NC-ND 4.0",
        "rights": "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International",
        "rights_uri": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "scheme_uri": "https://spdx.org/licenses/",
        "rights_identifier_scheme": "SPDX",
        "lang": "en"
    },
]

# from typing import Any

def get_cc_license_rights(identifier: str):
    """
    Return DataCite rights fields for a Creative Commons license identifier.
    """
    normalized_identifier = identifier.strip().lower()

    for license_info in cc_licenses:
        if license_info["identifier"].strip().lower() == normalized_identifier:
            return {
                "rights": license_info["rights"],
                "rights_uri": license_info["rights_uri"],
                "scheme_uri": license_info["scheme_uri"],
                "rights_identifier_scheme": license_info["rights_identifier_scheme"],
                "lang": license_info["lang"],
            }
