import json
import unittest
from unittest.mock import patch

from doi_manager.datacite_client import create_draft_and_assign_doi, datacite_login
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

        identifier = create_draft_and_assign_doi(
            record,
            "10.80402",
            datacite_url="https://api.test.datacite.org/dois",
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
        self.assertEqual(identifier.identifier_value, "10.80402/example-doi")
        self.assertEqual(identifier.identifier_type_attr, "doi")
        self.assertEqual(record.metadata.identifier, identifier)
        self.assertEqual(record.identifier, record_identifier)

    def test_create_draft_datacite_requires_record(self):
        with self.assertRaises(TypeError):
            create_draft_and_assign_doi(
                "not a record",
                "10.80402",
                datacite_url="https://api.test.datacite.org/dois",
                auth_token="Basic test-token",
            )

    def test_create_draft_datacite_requires_metadata(self):
        with self.assertRaises(ValueError):
            create_draft_and_assign_doi(
                Record(),
                "10.80402",
                datacite_url="https://api.test.datacite.org/dois",
                auth_token="Basic test-token",
            )

    def test_create_draft_datacite_rejects_existing_metadata_identifier(self):
        record = Record(metadata=self.metadata(identifier_value="10.123/existing"))

        with self.assertRaises(ValueError):
            create_draft_and_assign_doi(
                record,
                "10.80402",
                datacite_url="https://api.test.datacite.org/dois",
                auth_token="Basic test-token",
            )

    def test_create_draft_datacite_requires_datacite_url(self):
        with self.assertRaises(AttributeError):
            create_draft_and_assign_doi(
                Record(metadata=self.metadata()),
                "10.80402",
                auth_token="Basic test-token",
            )


if __name__ == "__main__":
    unittest.main()
