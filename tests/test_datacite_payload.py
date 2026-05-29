import unittest

from doi_manager.datacite_payload import generate_datacite_payload
from doi_manager.models import (
    Affiliation,
    AlternateIdentifier,
    Contributor,
    Creator,
    Date,
    Description,
    FundingReference,
    GeoLocation,
    GeoLocationBox,
    GeoLocationPoint,
    Identifier,
    Metadata,
    PolygonPoint,
    Publisher,
    Record,
    RelatedIdentifier,
    Rights,
    Subject,
    Title,
    Types,
)


class DataCitePayloadTest(unittest.TestCase):
    def metadata(self, identifier_value: str | None = None):
        affiliation = Affiliation(
            identifier="https://ror.org/03yrm5c26",
            name="Example University",
        )
        metadata_kwargs = {}
        if identifier_value is not None:
            metadata_kwargs["identifier"] = Identifier(
                identifier_value=identifier_value,
                identifier_type_attr="doi",
            )

        return Metadata(
            creators=[
                Creator(
                    creator_name="Ada Lovelace",
                    name_type="Personal",
                    name_identifiers=["https://orcid.org/0000-0001-2345-6789"],
                    affiliations=[affiliation],
                )
            ],
            titles=[Title(title="Example resource", type="Subtitle")],
            publisher=Publisher(
                name="Example Publisher",
                identifier="https://ror.org/03yrm5c26",
            ),
            publication_year="2026",
            types=Types(
                resource_type="Primary Dataset",
                resource_type_general="Dataset",
            ),
            subjects=[
                Subject(
                    subject="Metadata",
                    subject_scheme="Keyword",
                    classification_code="META",
                )
            ],
            contributors=[
                Contributor(
                    contributor_name="Grace Hopper",
                    name_type="Personal",
                    contributor_type="Researcher",
                    name_identifiers=["https://orcid.org/0000-0002-0000-0000"],
                    affiliations=[affiliation],
                )
            ],
            dates=[Date(date="2026-05-01", date_type="Updated")],
            alternate_identifiers=[
                AlternateIdentifier(
                    alternate_identifier_type="Local accession number",
                    alternate_identifier="ABC123",
                )
            ],
            related_identifiers=[
                RelatedIdentifier(
                    related_identifier="10.123/example-related",
                    related_identifier_type="DOI",
                    relation_type="References",
                    resource_type_general="Dataset",
                )
            ],
            sizes=["1 GB"],
            formats=["text/csv"],
            version="1.0",
            descriptions=[
                Description(
                    description="An example abstract.",
                    description_type="Abstract",
                )
            ],
            geolocations=[
                GeoLocation(
                    geolocation_place="Sydney, Australia",
                    geolocation_point=GeoLocationPoint(
                        point_longitude=151.2093,
                        point_latitude=-33.8688,
                    ),
                    geolocation_box=GeoLocationBox(
                        west_bound_longitude=149.0,
                        east_bound_longitude=150.0,
                        south_bound_latitude=-36.0,
                        north_bound_latitude=-35.0,
                    ),
                    geolocation_polygon=[
                        PolygonPoint(point_longitude=149.0, point_latitude=-36.0),
                        PolygonPoint(point_longitude=150.0, point_latitude=-37.0),
                        PolygonPoint(point_longitude=151.0, point_latitude=-38.0),
                        PolygonPoint(point_longitude=152.0, point_latitude=-39.0),
                    ],
                )
            ],
            funding_references=[
                FundingReference(
                    funder_name="Example Research Council",
                    funder_identifier="https://ror.org/03yrm5c26",
                    funder_identifier_type="ROR",
                    award_title="Example Award",
                    award_number="AWD-123",
                    award_uri="https://example.com/awards/AWD-123",
                )
            ],
            rights_list=[
                Rights(
                    rights="Creative Commons Attribution 4.0 International",
                    rights_uri="https://creativecommons.org/licenses/by/4.0/",
                    scheme_uri="https://spdx.org/licenses/",
                    rights_identifier="CC BY 4.0",
                    rights_identifier_scheme="SPDX",
                    lang="en"
                )
            ],
            **metadata_kwargs,
        )

    def test_generate_datacite_payload_maps_record_metadata(self):
        record = Record(metadata=self.metadata(identifier_value="10.123/example"))

        payload = generate_datacite_payload(record, "10.80402")
        attrs = payload["data"]["attributes"]

        self.assertEqual(payload["data"]["type"], "dois")
        self.assertEqual(attrs["prefix"], "10.80402")
        self.assertEqual(attrs["doi"], "10.123/example")
        self.assertEqual(attrs["creators"][0]["name"], "Ada Lovelace")
        self.assertEqual(attrs["titles"][0]["title"], "Example resource")
        self.assertEqual(attrs["publisher"]["name"], "Example Publisher")
        self.assertEqual(attrs["publicationYear"], 2026)
        self.assertEqual(attrs["types"]["resourceTypeGeneral"], "Dataset")
        self.assertEqual(attrs["subjects"][0]["subject"], "Metadata")
        self.assertEqual(attrs["contributors"][0]["contributorType"], "Researcher")
        self.assertEqual(attrs["dates"][0]["dateType"], "Updated")
        self.assertEqual(
            attrs["alternateIdentifiers"][0]["alternateIdentifier"],
            "ABC123",
        )
        self.assertEqual(
            attrs["relatedIdentifiers"][0]["relatedIdentifier"],
            "10.123/example-related",
        )
        self.assertEqual(attrs["sizes"], ["1 GB"])
        self.assertEqual(attrs["formats"], ["text/csv"])
        self.assertEqual(attrs["version"], "1.0")
        self.assertEqual(attrs["descriptions"][0]["descriptionType"], "Abstract")
        self.assertEqual(
            attrs["geoLocations"][0]["geoLocationPoint"]["pointLongitude"],
            151.2093,
        )
        self.assertEqual(
            attrs["fundingReferences"][0]["funderName"],
            "Example Research Council",
        )
        self.assertEqual(attrs["rightsList"][0]["rightsIdentifier"], "CC BY 4.0")

    def test_generate_datacite_payload_omits_missing_doi(self):
        record = Record(metadata=self.metadata())

        payload = generate_datacite_payload(record, "10.80402")

        self.assertNotIn("doi", payload["data"]["attributes"])

    def test_generate_datacite_payload_requires_record(self):
        with self.assertRaises(TypeError):
            generate_datacite_payload("not a record", "10.80402")

    def test_generate_datacite_payload_requires_metadata(self):
        with self.assertRaises(ValueError):
            generate_datacite_payload(Record(), "10.80402")

    def test_generate_datacite_payload_requires_prefix(self):
        with self.assertRaises(ValueError):
            generate_datacite_payload(Record(metadata=self.metadata()), "")


if __name__ == "__main__":
    unittest.main()
