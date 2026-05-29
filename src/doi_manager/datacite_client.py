import json
import os
from base64 import b64encode
from importlib import import_module
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

from .datacite_payload import generate_datacite_payload
from .models import Identifier, Record


class DataCiteHTTPError(RuntimeError):
    pass


def load_datacite_config() -> tuple[str, str]:
    try:
        user_config = import_module("config")
    except ModuleNotFoundError as err:
        if err.name == "config":
            raise AttributeError(
                "You need to provide a config.py file containing "
                "DOI_PREFIX and DATACITE_URL"
            ) from err
        raise

    doi_prefix = getattr(user_config, "DOI_PREFIX", None)
    datacite_url = getattr(user_config, "DATACITE_URL", None)

    if not doi_prefix:
        raise AttributeError("You need to provide a valid DOI_PREFIX in config.py")

    if not datacite_url:
        raise AttributeError("You need to provide a valid DATACITE_URL in config.py")

    return doi_prefix, datacite_url


def datacite_login() -> str:
    load_dotenv()
    username = os.environ.get("DATACITE_USERNAME")
    password = os.environ.get("DATACITE_PASSWORD")

    if not username or not password:
        raise ValueError("DATACITE_USERNAME and DATACITE_PASSWORD are required")

    token = b64encode(f"{username.upper()}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def post_datacite_payload(
    *,
    datacite_url: str,
    payload: dict,
    auth_token: str,
    urlopen_func=urlopen,
) -> dict:
    request = Request(
        datacite_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/vnd.api+json",
            "content-type": "application/json",
            "authorization": auth_token,
        },
        method="POST",
    )

    try:
        with urlopen_func(request) as response:
            body = response.read().decode("utf-8")
    except HTTPError as err:
        message = err.read().decode("utf-8")
        raise DataCiteHTTPError(message) from err

    return json.loads(body)


def create_draft_and_assign_doi(
    record: Record,
    *,
    auth_token: str | None = None,
    urlopen_func=urlopen,
) -> Identifier:
    if not isinstance(record, Record):
        raise TypeError("record must be a Record object")

    if record.metadata is None:
        raise ValueError("record must have metadata before allocating a DOI")

    if record.metadata.identifier is not None and record.metadata.identifier.identifier_value:
        raise ValueError("This record already has an identifier allocated")

    doi_prefix, datacite_url = load_datacite_config()
    token = auth_token or datacite_login()
    payload = generate_datacite_payload(record, doi_prefix)
    response_data = post_datacite_payload(
        datacite_url=datacite_url,
        payload=payload,
        auth_token=token,
        urlopen_func=urlopen_func,
    )

    doi = response_data["data"]["id"]
    identifier = Identifier(identifier_value=doi, identifier_type_attr="doi")
    record.metadata.identifier = identifier
    return identifier
