import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from doi_manager.datacite_client import (
    create_draft_and_assign_doi,
    datacite_login,
    load_datacite_config,
)
from doi_manager.models import Creator, Identifier, Metadata, Publisher, Record, Title, Types


class FakeResponse:
    def __init__(self, body: dict):
        self.body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class DataCiteClientTest(unittest.TestCase):
    def metadata(self, identifier_value: str | None = None):
        metadata_kwargs = {}
        if identifier_value is not None:
            metadata_kwargs["identifier"] = Identifier(
                identifier_value=identifier_value,
                identifier_type_attr="doi",
            )

        return Metadata(
            creators=[Creator(creator_name="Ada Lovelace", name_type="Personal")],
            titles=[Title(title="Example resource")],
            publisher=Publisher(name="Example Publisher"),
            publication_year="2026",
            types=Types(
                resource_type="Dataset",
                resource_type_general="Dataset",
            ),
            **metadata_kwargs,
        )

    def test_datacite_login_returns_basic_auth_token(self):
        with patch("doi_manager.datacite_client.load_dotenv") as mock_load_dotenv, patch.dict(
            "os.environ",
            {
                "DATACITE_USERNAME": "repo.test",
                "DATACITE_PASSWORD": "secret",
            },
        ):
            token = datacite_login()

        mock_load_dotenv.assert_called_once_with()
        self.assertEqual(token, "Basic UkVQTy5URVNUOnNlY3JldA==")

    def test_datacite_login_does_not_accept_credentials_as_arguments(self):
        with self.assertRaises(TypeError):
            datacite_login("repo.test", "secret")

    def test_create_draft_datacite_posts_payload_and_updates_metadata_identifier(self):
        captured = {}
        record = Record(metadata=self.metadata())
        record_identifier = record.identifier

        def fake_urlopen(request):
            captured["request"] = request
            return FakeResponse({"data": {"id": "10.80402/example-doi"}})

        with patch.dict(
            "sys.modules",
            {
                "config": SimpleNamespace(
                    DOI_PREFIX="10.80402",
                    DATACITE_URL="https://api.test.datacite.org/dois",
                )
            },
        ):
            response_data = create_draft_and_assign_doi(
                record,
                auth_token="Basic test-token",
                urlopen_func=fake_urlopen,
            )

        posted_payload = json.loads(captured["request"].data.decode("utf-8"))

        self.assertEqual(captured["request"].full_url, "https://api.test.datacite.org/dois")
        self.assertEqual(posted_payload["data"]["type"], "dois")
        self.assertEqual(
            posted_payload["data"]["attributes"]["prefix"],
            "10.80402",
        )
        self.assertEqual(response_data["data"]["id"], "10.80402/example-doi")
        self.assertEqual(
            record.metadata.identifier.identifier_value,
            "10.80402/example-doi",
        )
        self.assertEqual(record.metadata.identifier.identifier_type_attr, "doi")
        self.assertEqual(record.identifier, record_identifier)

    def test_create_draft_datacite_requires_record(self):
        with self.assertRaises(TypeError):
            create_draft_and_assign_doi(
                "not a record",
                auth_token="Basic test-token",
            )

    def test_create_draft_datacite_requires_metadata(self):
        with self.assertRaises(ValueError):
            create_draft_and_assign_doi(
                Record(),
                auth_token="Basic test-token",
            )

    def test_create_draft_datacite_rejects_existing_metadata_identifier(self):
        record = Record(metadata=self.metadata(identifier_value="10.123/existing"))

        with self.assertRaises(ValueError):
            create_draft_and_assign_doi(
                record,
                auth_token="Basic test-token",
            )

    def test_load_datacite_config_reads_user_config_module(self):
        with patch.dict(
            "sys.modules",
            {
                "config": SimpleNamespace(
                    DOI_PREFIX="10.80402",
                    DATACITE_URL="https://api.test.datacite.org/dois",
                )
            },
        ):
            doi_prefix, datacite_url = load_datacite_config()

        self.assertEqual(doi_prefix, "10.80402")
        self.assertEqual(datacite_url, "https://api.test.datacite.org/dois")

    def test_create_draft_datacite_requires_user_config_file(self):
        with patch.dict("sys.modules"):
            with patch("doi_manager.datacite_client.import_module") as mock_import_module:
                mock_import_module.side_effect = ModuleNotFoundError(
                    "No module named 'config'",
                    name="config",
                )

                with self.assertRaises(AttributeError):
                    create_draft_and_assign_doi(
                        Record(metadata=self.metadata()),
                        auth_token="Basic test-token",
                    )

    def test_create_draft_datacite_requires_doi_prefix_config(self):
        with patch.dict(
            "sys.modules",
            {"config": SimpleNamespace(DOI_PREFIX="", DATACITE_URL="https://api.test.datacite.org/dois")},
        ):
            with self.assertRaises(AttributeError):
                create_draft_and_assign_doi(
                    Record(metadata=self.metadata()),
                    auth_token="Basic test-token",
                )

    def test_create_draft_datacite_requires_datacite_url_config(self):
        with patch.dict(
            "sys.modules",
            {"config": SimpleNamespace(DOI_PREFIX="10.80402", DATACITE_URL="")},
        ):
            with self.assertRaises(AttributeError):
                create_draft_and_assign_doi(
                    Record(metadata=self.metadata()),
                    auth_token="Basic test-token",
                )

    def test_create_draft_datacite_does_not_accept_doi_prefix_argument(self):
        with self.assertRaises(TypeError):
            create_draft_and_assign_doi(
                Record(metadata=self.metadata()),
                "10.80402",
                auth_token="Basic test-token",
            )


if __name__ == "__main__":
    unittest.main()
