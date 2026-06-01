import uuid
import unittest
from datetime import datetime
from unittest.mock import patch

from doi_manager.models import (
    Affiliation,
    AlternateIdentifier,
    Contributor,
    Creator,
    Date,
    Description,
    FundingReference,
    Identifier,
    GeoLocation,
    GeoLocationBox,
    GeoLocationPoint,
    NameIdentifier,
    PolygonPoint,
    Rights,
    Publisher,
    Record,
    RelatedIdentifier,
    Metadata,
    Subject,
    Title,
    Types,
)


class MetadataTest(unittest.TestCase):
    def example_types(self):
        return Types(
            resource_type="Dataset",
            resource_type_general="Dataset",
        )

    def example_metadata(self):
        return Metadata(
            identifier=Identifier(
                identifier_value="10.123/example",
                identifier_type_attr="doi",
            ),
            creators=[
                Creator(
                    creator_name="Ada Lovelace",
                    name_type="Personal",
                )
            ],
            titles=[Title(title="Example resource")],
            publisher=Publisher(name="Example Publisher"),
            publication_year="2026",
            types=self.example_types(),
        )

    # Record tests
    def test_record_generates_uuid_identifier(self):
        """Checks that a record automatically receives a UUID identifier."""
        item_record = Record()

        parsed_identifier = uuid.UUID(item_record.identifier)

        self.assertEqual(str(parsed_identifier), item_record.identifier)

    def test_record_generates_unique_identifier_for_each_instance(self):
        """Checks that each record receives its own identifier."""
        first_record = Record()
        second_record = Record()

        self.assertNotEqual(first_record.identifier, second_record.identifier)

    def test_record_stores_no_metadata_by_default(self):
        """Checks that a record can exist without metadata."""
        item_record = Record()

        self.assertIsNone(item_record.metadata)

    def test_record_stores_metadata(self):
        """Checks that a record can store one metadata object."""
        item_metadata = self.example_metadata()
        item_record = Record(metadata=item_metadata)

        self.assertEqual(item_record.metadata, item_metadata)

    def test_record_metadata_must_be_metadata(self):
        """Checks that record metadata must be a Metadata object."""
        with self.assertRaises(TypeError):
            Record(metadata="not metadata")

    def test_record_allows_metadata_update(self):
        """Checks that record metadata can be updated to Metadata or None."""
        item_record = Record()
        item_metadata = self.example_metadata()

        item_record.metadata = item_metadata
        self.assertEqual(item_record.metadata, item_metadata)

        item_record.metadata = None
        self.assertIsNone(item_record.metadata)

    def test_record_metadata_update_must_be_metadata(self):
        """Checks that record metadata updates must use Metadata objects."""
        item_record = Record()

        with self.assertRaises(TypeError):
            item_record.metadata = "not metadata"

    def test_record_rejects_identifier_input(self):
        """Checks that users cannot supply a record identifier."""
        with self.assertRaises(TypeError):
            Record(identifier=str(uuid.uuid4()))

    def test_record_identifier_is_read_only(self):
        """Checks that users cannot update a record identifier."""
        item_record = Record()

        with self.assertRaises(AttributeError):
            item_record.identifier = str(uuid.uuid4())

    # Affiliation tests
    def test_affiliation_stores_identifier_and_name(self):
        """Checks that an affiliation stores its identifier and name."""
        item_affiliation = Affiliation(
            name="Example University",
            affiliation_identifier="https://ror.org/03yrm5c26",
            affiliation_identifier_scheme="ROR",
            scheme_uri="https://ror.org/",
        )

        self.assertEqual(
            item_affiliation.affiliation_identifier,
            "https://ror.org/03yrm5c26",
        )
        self.assertEqual(item_affiliation.name, "Example University")
        self.assertEqual(item_affiliation.affiliation_identifier_scheme, "ROR")
        self.assertEqual(item_affiliation.scheme_uri, "https://ror.org/")

    def test_affiliation_identifier_fields_are_optional(self):
        """Checks that an affiliation can be created with just a name."""
        item_affiliation = Affiliation(name="Example University")

        self.assertEqual(item_affiliation.name, "Example University")
        self.assertIsNone(item_affiliation.affiliation_identifier)
        self.assertIsNone(item_affiliation.affiliation_identifier_scheme)
        self.assertIsNone(item_affiliation.scheme_uri)

    def test_affiliation_fields_must_be_keywords(self):
        """Checks that affiliation fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Affiliation("https://ror.org/03yrm5c26", "Example University")

    def test_affiliation_rejects_invalid_identifier_prefix(self):
        """Checks that affiliation identifiers must use an allowed prefix."""
        with self.assertRaises(ValueError):
            Affiliation(
                name="Example University",
                affiliation_identifier="https://example.com/03yrm5c26",
                affiliation_identifier_scheme="ROR",
            )

    def test_affiliation_identifier_must_be_string(self):
        """Checks that affiliation identifiers must be strings."""
        with self.assertRaises(TypeError):
            Affiliation(
                name="Example University",
                affiliation_identifier=123,
                affiliation_identifier_scheme="ROR",
            )

    def test_affiliation_requires_scheme_when_identifier_is_supplied(self):
        """Checks that affiliation identifiers require an identifier scheme."""
        with self.assertRaises(ValueError):
            Affiliation(
                name="Example University",
                affiliation_identifier="https://ror.org/03yrm5c26",
            )

    def test_affiliation_identifier_scheme_must_be_string(self):
        """Checks that affiliation identifier schemes must be strings."""
        with self.assertRaises(TypeError):
            Affiliation(
                name="Example University",
                affiliation_identifier="https://ror.org/03yrm5c26",
                affiliation_identifier_scheme=123,
            )

    def test_affiliation_rejects_invalid_identifier_scheme(self):
        """Checks that affiliation identifier schemes use the controlled list."""
        with self.assertRaises(ValueError):
            Affiliation(
                name="Example University",
                affiliation_identifier="https://ror.org/03yrm5c26",
                affiliation_identifier_scheme="GRID",
            )

    def test_affiliation_scheme_uri_must_be_string(self):
        """Checks that affiliation scheme URIs must be strings."""
        with self.assertRaises(TypeError):
            Affiliation(
                name="Example University",
                affiliation_identifier="https://ror.org/03yrm5c26",
                affiliation_identifier_scheme="ROR",
                scheme_uri=123,
            )

    def test_affiliation_rejects_invalid_scheme_uri(self):
        """Checks that affiliation scheme URIs use the controlled list."""
        with self.assertRaises(ValueError):
            Affiliation(
                name="Example University",
                affiliation_identifier="https://ror.org/03yrm5c26",
                affiliation_identifier_scheme="ROR",
                scheme_uri="https://example.com/",
            )

    def test_affiliation_name_must_be_string(self):
        """Checks that affiliation names must be strings."""
        with self.assertRaises(TypeError):
            Affiliation(name=123)

    # Creator tests
    def test_name_identifier_stores_fields(self):
        """Checks that a name identifier stores its DataCite fields."""
        item_name_identifier = NameIdentifier(
            name_identifier="https://orcid.org/0000-0001-2345-6789",
            name_identifier_scheme="ORCID",
            scheme_uri="https://orcid.org",
        )

        self.assertEqual(
            item_name_identifier.name_identifier,
            "https://orcid.org/0000-0001-2345-6789",
        )
        self.assertEqual(item_name_identifier.name_identifier_scheme, "ORCID")
        self.assertEqual(item_name_identifier.scheme_uri, "https://orcid.org")

    def test_name_identifier_value_must_be_string(self):
        """Checks that name identifier values must be strings."""
        with self.assertRaises(TypeError):
            NameIdentifier(
                name_identifier=123,
                name_identifier_scheme="ORCID",
            )

    def test_name_identifier_scheme_must_be_string(self):
        """Checks that name identifier schemes must be strings."""
        with self.assertRaises(TypeError):
            NameIdentifier(
                name_identifier="https://orcid.org/0000-0001-2345-6789",
                name_identifier_scheme=123,
            )

    def test_name_identifier_rejects_invalid_identifier_prefix(self):
        """Checks that name identifiers must use an allowed prefix."""
        with self.assertRaises(ValueError):
            NameIdentifier(
                name_identifier="https://example.com/0000-0001-2345-6789",
                name_identifier_scheme="ORCID",
            )

    def test_name_identifier_rejects_invalid_identifier_scheme(self):
        """Checks that name identifier schemes use the controlled list."""
        with self.assertRaises(ValueError):
            NameIdentifier(
                name_identifier="https://orcid.org/0000-0001-2345-6789",
                name_identifier_scheme="GRID",
            )

    def test_name_identifier_scheme_uri_must_be_string(self):
        """Checks that name identifier scheme URIs must be strings."""
        with self.assertRaises(TypeError):
            NameIdentifier(
                name_identifier="https://orcid.org/0000-0001-2345-6789",
                name_identifier_scheme="ORCID",
                scheme_uri=123,
            )

    def test_name_identifier_rejects_invalid_scheme_uri(self):
        """Checks that name identifier scheme URIs use the controlled list."""
        with self.assertRaises(ValueError):
            NameIdentifier(
                name_identifier="https://orcid.org/0000-0001-2345-6789",
                name_identifier_scheme="ORCID",
                scheme_uri="https://example.com",
            )

    def test_creator_stores_name_and_name_type(self):
        """Checks that a creator stores name, type, and empty optional lists."""
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )

        self.assertEqual(item_creator.creator_name, "Ada Lovelace")
        self.assertEqual(item_creator.name_type, "Personal")
        self.assertEqual(item_creator.name_identifiers, [])
        self.assertEqual(item_creator.affiliations, [])

    def test_creator_stores_name_identifiers(self):
        """Checks that a creator stores multiple name identifiers."""
        first_name_identifier = NameIdentifier(
            name_identifier="https://orcid.org/0000-0001-2345-6789",
            name_identifier_scheme="ORCID",
        )
        second_name_identifier = NameIdentifier(
            name_identifier="https://ror.org/12345",
            name_identifier_scheme="ROR",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
            name_identifiers=[first_name_identifier, second_name_identifier],
        )

        self.assertEqual(
            item_creator.name_identifiers,
            [first_name_identifier, second_name_identifier],
        )

    def test_creator_requires_name_and_name_type(self):
        """Checks that creator name and name type are mandatory."""
        with self.assertRaises(TypeError):
            Creator()

    def test_creator_fields_must_be_keywords(self):
        """Checks that creator fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Creator("Ada Lovelace", "Personal")

    def test_creator_name_must_be_string(self):
        """Checks that creator name must be a string."""
        with self.assertRaises(TypeError):
            Creator(creator_name=123, name_type="Personal")

    def test_creator_rejects_invalid_name_type(self):
        """Checks that creator name type must be controlled."""
        with self.assertRaises(ValueError):
            Creator(creator_name="Ada Lovelace", name_type="Individual")

    def test_creator_uses_creator_name_type_vocab(self):
        """Checks that creators use the creator-specific name type vocabulary."""
        with patch("doi_manager.models.CREATOR_NAME_TYPE_VALUES", ["CreatorOnly"]):
            item_creator = Creator(
                creator_name="Ada Lovelace",
                name_type="CreatorOnly",
            )

        self.assertEqual(item_creator.name_type, "CreatorOnly")

    def test_creator_rejects_non_name_identifier(self):
        """Checks that creator name identifiers must be NameIdentifier objects."""
        with self.assertRaises(TypeError):
            Creator(
                creator_name="Ada Lovelace",
                name_type="Personal",
                name_identifiers=[123],
            )

    def test_creator_name_identifiers_must_be_list(self):
        """Checks that creator name identifiers must be supplied as a list."""
        with self.assertRaises(TypeError):
            Creator(
                creator_name="Ada Lovelace",
                name_type="Personal",
                name_identifiers="https://orcid.org/123",
            )

    def test_creator_stores_affiliations(self):
        """Checks that a creator stores affiliation objects."""
        item_affiliation = Affiliation(
            name="Example University",
            affiliation_identifier="https://ror.org/03yrm5c26",
            affiliation_identifier_scheme="ROR",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
            affiliations=[item_affiliation],
        )

        self.assertEqual(item_creator.affiliations, [item_affiliation])

    def test_creator_affiliations_must_be_list(self):
        """Checks that creator affiliations must be supplied as a list."""
        item_affiliation = Affiliation(
            name="Example University",
            affiliation_identifier="https://ror.org/03yrm5c26",
            affiliation_identifier_scheme="ROR",
        )

        with self.assertRaises(TypeError):
            Creator(
                creator_name="Ada Lovelace",
                name_type="Personal",
                affiliations=item_affiliation,
            )

    def test_creator_affiliations_must_contain_affiliations(self):
        """Checks that creator affiliations must contain affiliation objects."""
        with self.assertRaises(TypeError):
            Creator(
                creator_name="Ada Lovelace",
                name_type="Personal",
                affiliations=["Example University"],
            )

    # Contributor tests
    def test_contributor_stores_name_type_and_contributor_type(self):
        """Checks that a contributor stores required fields and empty optional lists."""
        item_contributor = Contributor(
            contributor_name="Grace Hopper",
            name_type="Personal",
            contributor_type="Researcher",
        )

        self.assertEqual(item_contributor.contributor_name, "Grace Hopper")
        self.assertEqual(item_contributor.name_type, "Personal")
        self.assertEqual(item_contributor.contributor_type, "Researcher")
        self.assertEqual(item_contributor.name_identifiers, [])
        self.assertEqual(item_contributor.affiliations, [])

    def test_contributor_stores_name_identifiers(self):
        """Checks that a contributor stores multiple name identifiers."""
        first_name_identifier = NameIdentifier(
            name_identifier="https://orcid.org/0000-0001-2345-6789",
            name_identifier_scheme="ORCID",
        )
        second_name_identifier = NameIdentifier(
            name_identifier="https://ror.org/12345",
            name_identifier_scheme="ROR",
        )
        item_contributor = Contributor(
            contributor_name="Grace Hopper",
            name_type="Personal",
            contributor_type="Researcher",
            name_identifiers=[first_name_identifier, second_name_identifier],
        )

        self.assertEqual(
            item_contributor.name_identifiers,
            [first_name_identifier, second_name_identifier],
        )

    def test_contributor_requires_name_type_and_contributor_type(self):
        """Checks that contributor required fields are mandatory."""
        with self.assertRaises(TypeError):
            Contributor()

    def test_contributor_fields_must_be_keywords(self):
        """Checks that contributor fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Contributor("Grace Hopper", "Personal", "Researcher")

    def test_contributor_name_must_be_string(self):
        """Checks that contributor name must be a string."""
        with self.assertRaises(TypeError):
            Contributor(
                contributor_name=123,
                name_type="Personal",
                contributor_type="Researcher",
            )

    def test_contributor_rejects_invalid_name_type(self):
        """Checks that contributor name type must be controlled."""
        with self.assertRaises(ValueError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Individual",
                contributor_type="Researcher",
            )

    def test_contributor_uses_contributor_name_type_vocab(self):
        """Checks that contributors use their own name type vocabulary."""
        with patch("doi_manager.models.CONTRIBUTOR_NAME_TYPE_VALUES", ["ContributorOnly"]):
            item_contributor = Contributor(
                contributor_name="Grace Hopper",
                name_type="ContributorOnly",
                contributor_type="Researcher",
            )

        self.assertEqual(item_contributor.name_type, "ContributorOnly")

    def test_contributor_type_must_be_string(self):
        """Checks that contributor type must be a string."""
        with self.assertRaises(TypeError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Personal",
                contributor_type=123,
            )

    def test_contributor_rejects_invalid_contributor_type(self):
        """Checks that contributor type must be controlled."""
        with self.assertRaises(ValueError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Personal",
                contributor_type="Reviewer",
            )

    def test_contributor_rejects_non_name_identifier(self):
        """Checks that contributor name identifiers must be NameIdentifier objects."""
        with self.assertRaises(TypeError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Personal",
                contributor_type="Researcher",
                name_identifiers=[123],
            )

    def test_contributor_name_identifiers_must_be_list(self):
        """Checks that contributor name identifiers must be supplied as a list."""
        with self.assertRaises(TypeError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Personal",
                contributor_type="Researcher",
                name_identifiers="https://orcid.org/123",
            )

    def test_contributor_stores_affiliations(self):
        """Checks that a contributor stores affiliation objects."""
        item_affiliation = Affiliation(
            name="Example University",
            affiliation_identifier="https://ror.org/03yrm5c26",
            affiliation_identifier_scheme="ROR",
        )
        item_contributor = Contributor(
            contributor_name="Grace Hopper",
            name_type="Personal",
            contributor_type="Researcher",
            affiliations=[item_affiliation],
        )

        self.assertEqual(item_contributor.affiliations, [item_affiliation])

    def test_contributor_affiliations_must_be_list(self):
        """Checks that contributor affiliations must be supplied as a list."""
        item_affiliation = Affiliation(
            name="Example University",
            affiliation_identifier="https://ror.org/03yrm5c26",
            affiliation_identifier_scheme="ROR",
        )

        with self.assertRaises(TypeError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Personal",
                contributor_type="Researcher",
                affiliations=item_affiliation,
            )

    def test_contributor_affiliations_must_contain_affiliations(self):
        """Checks that contributor affiliations must contain affiliation objects."""
        with self.assertRaises(TypeError):
            Contributor(
                contributor_name="Grace Hopper",
                name_type="Personal",
                contributor_type="Researcher",
                affiliations=["Example University"],
            )

    # Identifier tests
    def test_identifier_stores_value_and_type_attr(self):
        """Checks that an identifier stores its value and type attribute."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )

        self.assertEqual(item_identifier.identifier_value, "10.123/example")
        self.assertEqual(item_identifier.identifier_type_attr, "doi")

    def test_identifier_requires_value_and_type_attr(self):
        """Checks that identifier value and type attribute are mandatory."""
        with self.assertRaises(TypeError):
            Identifier(identifier_value="10.123/example")

    def test_identifier_fields_must_be_keywords(self):
        """Checks that identifier fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Identifier("10.123/example", "doi")

    def test_identifier_rejects_invalid_type_attr(self):
        """Checks that identifier type attribute must be controlled."""
        with self.assertRaises(ValueError):
            Identifier(
                identifier_value="10.123/example",
                identifier_type_attr="isbn",
            )

    # Rights tests
    def test_rights_stores_identifier_and_derived_fields(self):
        """Checks that a Rights object stores identifier"""
        item_rights = Rights(rights="Creative Commons Attribution 4.0 International", rights_identifier="CC0")

        self.assertEqual(item_rights.rights, "Creative Commons Attribution 4.0 International")
        self.assertEqual(item_rights.rights_identifier, "CC0")


    def test_rights_rejects_invalid_identifier(self):
        """Checks that Rights rejects identifiers not in the controlled list."""
        with self.assertRaises(ValueError):
            Rights(rights="Creative Commons Attribution 4.0 International", rights_identifier="INVALID")


    # Alternate identifier tests
    def test_alternate_identifier_stores_type_and_value(self):
        """Checks that an alternate identifier stores its type and value."""
        item_alternate_identifier = AlternateIdentifier(
            alternate_identifier_type="Local accession number",
            alternate_identifier="ABC123",
        )

        self.assertEqual(
            item_alternate_identifier.alternate_identifier_type,
            "Local accession number",
        )
        self.assertEqual(item_alternate_identifier.alternate_identifier, "ABC123")

    def test_alternate_identifier_requires_type_and_value(self):
        """Checks that alternate identifier type and value are mandatory."""
        with self.assertRaises(TypeError):
            AlternateIdentifier()

    def test_alternate_identifier_fields_must_be_keywords(self):
        """Checks that alternate identifier fields cannot be positional."""
        with self.assertRaises(TypeError):
            AlternateIdentifier("Local accession number", "ABC123")

    def test_alternate_identifier_type_must_be_string(self):
        """Checks that alternate identifier type must be a string."""
        with self.assertRaises(TypeError):
            AlternateIdentifier(
                alternate_identifier_type=123,
                alternate_identifier="ABC123",
            )

    def test_alternate_identifier_must_be_string(self):
        """Checks that alternate identifier value must be a string."""
        with self.assertRaises(TypeError):
            AlternateIdentifier(
                alternate_identifier_type="Local accession number",
                alternate_identifier=123,
            )

    # Related identifier tests
    def test_related_identifier_stores_required_fields(self):
        """Checks that a related identifier stores required fields."""
        item_related_identifier = RelatedIdentifier(
            related_identifier="10.123/example-related",
            related_identifier_type="DOI",
            relation_type="References",
        )

        self.assertEqual(
            item_related_identifier.related_identifier,
            "10.123/example-related",
        )
        self.assertEqual(item_related_identifier.related_identifier_type, "DOI")
        self.assertEqual(item_related_identifier.relation_type, "References")
        self.assertIsNone(item_related_identifier.resource_type_general)
        self.assertIsNone(item_related_identifier.relation_type_information)

    def test_related_identifier_stores_optional_fields(self):
        """Checks that a related identifier stores optional fields."""
        item_related_identifier = RelatedIdentifier(
            related_identifier="https://example.com/related",
            related_identifier_type="URL",
            relation_type="IsSupplementTo",
            resource_type_general="Dataset",
            relation_type_information="Supplementary dataset",
        )

        self.assertEqual(item_related_identifier.resource_type_general, "Dataset")
        self.assertEqual(
            item_related_identifier.relation_type_information,
            "Supplementary dataset",
        )

    def test_related_identifier_requires_required_fields(self):
        """Checks that related identifier required fields are mandatory."""
        with self.assertRaises(TypeError):
            RelatedIdentifier()

    def test_related_identifier_fields_must_be_keywords(self):
        """Checks that related identifier fields cannot be positional."""
        with self.assertRaises(TypeError):
            RelatedIdentifier("10.123/example-related", "DOI", "References")

    def test_related_identifier_must_be_string(self):
        """Checks that related identifier must be a string."""
        with self.assertRaises(TypeError):
            RelatedIdentifier(
                related_identifier=123,
                related_identifier_type="DOI",
                relation_type="References",
            )

    def test_related_identifier_type_must_be_string(self):
        """Checks that related identifier type must be a string."""
        with self.assertRaises(TypeError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type=123,
                relation_type="References",
            )

    def test_related_identifier_rejects_invalid_identifier_type(self):
        """Checks that related identifier type must be controlled."""
        with self.assertRaises(ValueError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type="URI",
                relation_type="References",
            )

    def test_related_identifier_relation_type_must_be_string(self):
        """Checks that related identifier relation type must be a string."""
        with self.assertRaises(TypeError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type="DOI",
                relation_type=123,
            )

    def test_related_identifier_rejects_invalid_relation_type(self):
        """Checks that related identifier relation type must be controlled."""
        with self.assertRaises(ValueError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type="DOI",
                relation_type="LinksTo",
            )

    def test_related_identifier_resource_type_general_must_be_string(self):
        """Checks that related identifier resource type general must be a string."""
        with self.assertRaises(TypeError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type="DOI",
                relation_type="References",
                resource_type_general=123,
            )

    def test_related_identifier_rejects_invalid_resource_type_general(self):
        """Checks that related identifier resource type general must be controlled."""
        with self.assertRaises(ValueError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type="DOI",
                relation_type="References",
                resource_type_general="Database",
            )

    def test_related_identifier_relation_type_information_must_be_string(self):
        """Checks that related identifier relation information must be a string."""
        with self.assertRaises(TypeError):
            RelatedIdentifier(
                related_identifier="10.123/example-related",
                related_identifier_type="DOI",
                relation_type="References",
                relation_type_information=123,
            )

    # Title tests
    def test_title_stores_title_and_defaults_lang(self):
        """Checks that a title stores its text and defaults language to English."""
        item_title = Title(title="Example resource")

        self.assertEqual(item_title.title, "Example resource")
        self.assertEqual(item_title.lang, "en")
        self.assertIsNone(item_title.type)

    def test_title_stores_lang_and_type(self):
        """Checks that a title stores supplied language and type."""
        item_title = Title(title="Example subtitle", lang="en", type="Subtitle")

        self.assertEqual(item_title.title, "Example subtitle")
        self.assertEqual(item_title.lang, "en")
        self.assertEqual(item_title.type, "Subtitle")

    def test_title_requires_title(self):
        """Checks that title text is mandatory."""
        with self.assertRaises(TypeError):
            Title()

    def test_title_must_be_string(self):
        """Checks that title text must be a string."""
        with self.assertRaises(TypeError):
            Title(title=123)

    def test_title_lang_must_be_string(self):
        """Checks that title language must be a string."""
        with self.assertRaises(TypeError):
            Title(title="Example resource", lang=123)

    def test_title_fields_must_be_keywords(self):
        """Checks that title fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Title("Example resource")

    def test_title_rejects_invalid_type(self):
        """Checks that title type must be controlled when supplied."""
        with self.assertRaises(ValueError):
            Title(title="Example resource", type="MainTitle")

    # Types tests
    def test_types_stores_resource_type_fields(self):
        """Checks that types stores resource type fields."""
        item_types = Types(
            resource_type="Dataset",
            resource_type_general="Dataset",
        )

        self.assertEqual(item_types.resource_type, "Dataset")
        self.assertEqual(item_types.resource_type_general, "Dataset")

    def test_types_requires_resource_type_fields(self):
        """Checks that resource type fields are mandatory."""
        with self.assertRaises(TypeError):
            Types()

    def test_types_fields_must_be_keywords(self):
        """Checks that types fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Types("Dataset", "Dataset")

    def test_types_resource_type_must_be_string(self):
        """Checks that resource type must be a string."""
        with self.assertRaises(TypeError):
            Types(resource_type=123, resource_type_general="Dataset")

    def test_types_resource_type_general_must_be_string(self):
        """Checks that resource type general must be a string."""
        with self.assertRaises(TypeError):
            Types(resource_type="Dataset", resource_type_general=123)

    def test_types_rejects_invalid_resource_type_general(self):
        """Checks that resource type general must be controlled."""
        with self.assertRaises(ValueError):
            Types(resource_type="Dataset", resource_type_general="Database")

    # Subject tests
    def test_subject_stores_subject_and_defaults_lang(self):
        """Checks that a subject stores its text and defaults language to English."""
        item_subject = Subject(subject="Computer science")

        self.assertEqual(item_subject.subject, "Computer science")
        self.assertEqual(item_subject.lang, "en")
        self.assertIsNone(item_subject.scheme_uri)
        self.assertIsNone(item_subject.value_uri)
        self.assertIsNone(item_subject.subject_scheme)
        self.assertIsNone(item_subject.classification_code)

    def test_subject_stores_optional_metadata(self):
        """Checks that a subject stores optional scheme metadata."""
        item_subject = Subject(
            subject="Computer science",
            lang="fr",
            scheme_uri="https://example.com/scheme",
            value_uri="https://example.com/value",
            subject_scheme="Example Scheme",
            classification_code="ABC123",
        )

        self.assertEqual(item_subject.lang, "fr")
        self.assertEqual(item_subject.scheme_uri, "https://example.com/scheme")
        self.assertEqual(item_subject.value_uri, "https://example.com/value")
        self.assertEqual(item_subject.subject_scheme, "Example Scheme")
        self.assertEqual(item_subject.classification_code, "ABC123")

    def test_subject_requires_subject(self):
        """Checks that subject text is mandatory."""
        with self.assertRaises(TypeError):
            Subject()

    def test_subject_fields_must_be_keywords(self):
        """Checks that subject fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Subject("Computer science")

    def test_subject_must_be_string(self):
        """Checks that subject text must be a string."""
        with self.assertRaises(TypeError):
            Subject(subject=123)

    def test_subject_lang_must_be_string(self):
        """Checks that subject language must be a string."""
        with self.assertRaises(TypeError):
            Subject(subject="Computer science", lang=123)

    def test_subject_optional_metadata_must_be_strings(self):
        """Checks that optional subject metadata fields must be strings."""
        for field_name in [
            "scheme_uri",
            "value_uri",
            "subject_scheme",
            "classification_code",
        ]:
            with self.subTest(field_name=field_name):
                with self.assertRaises(TypeError):
                    Subject(subject="Computer science", **{field_name: 123})

    # Date tests
    def test_date_stores_year_and_type(self):
        """Checks that a date stores a year and controlled date type."""
        item_date = Date(date="2026", date_type="Issued")

        self.assertEqual(item_date.date, "2026")
        self.assertEqual(item_date.date_type, "Issued")
        self.assertIsNone(item_date.date_information)

    def test_date_stores_full_date_and_information(self):
        """Checks that a date stores a full date and date information."""
        item_date = Date(
            date="2026-05-01",
            date_type="Updated",
            date_information="Metadata updated",
        )

        self.assertEqual(item_date.date, "2026-05-01")
        self.assertEqual(item_date.date_type, "Updated")
        self.assertEqual(item_date.date_information, "Metadata updated")

    def test_date_requires_date(self):
        """Checks that date value is mandatory."""
        with self.assertRaises(TypeError):
            Date()

    def test_date_fields_must_be_keywords(self):
        """Checks that date fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Date("2026", "Issued")

    def test_date_must_be_string(self):
        """Checks that date value must be a string."""
        with self.assertRaises(TypeError):
            Date(date=2026, date_type="Issued")

    def test_date_rejects_invalid_format(self):
        """Checks that date value must use YYYY or YYYY-MM-DD format."""
        for date_value in ["26", "2026-5-1", "2026/05/01"]:
            with self.subTest(date_value=date_value):
                with self.assertRaises(ValueError):
                    Date(date=date_value, date_type="Issued")

    def test_date_type_must_be_string(self):
        """Checks that date type must be a string."""
        with self.assertRaises(TypeError):
            Date(date="2026", date_type=123)

    def test_date_rejects_invalid_date_type(self):
        """Checks that date type must be controlled."""
        with self.assertRaises(ValueError):
            Date(date="2026", date_type="Published")

    def test_date_information_must_be_string(self):
        """Checks that date information must be a string."""
        with self.assertRaises(TypeError):
            Date(
                date="2026",
                date_type="Issued",
                date_information=123,
            )

    # Description tests
    def test_description_stores_description_type_and_defaults_lang(self):
        """Checks that a description stores text and defaults language to English."""
        item_description = Description(
            description="Example abstract",
            description_type="Abstract",
        )

        self.assertEqual(item_description.description, "Example abstract")
        self.assertEqual(item_description.description_type, "Abstract")
        self.assertEqual(item_description.lang, "en")

    def test_description_stores_custom_lang(self):
        """Checks that a description stores a supplied language."""
        item_description = Description(
            description="Example methods",
            description_type="Methods",
            lang="fr",
        )

        self.assertEqual(item_description.lang, "fr")

    def test_description_requires_description_and_type(self):
        """Checks that description text and type are mandatory."""
        with self.assertRaises(TypeError):
            Description()

    def test_description_fields_must_be_keywords(self):
        """Checks that description fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Description("Example abstract", "Abstract")

    def test_description_must_be_string(self):
        """Checks that description text must be a string."""
        with self.assertRaises(TypeError):
            Description(description=123, description_type="Abstract")

    def test_description_type_must_be_string(self):
        """Checks that description type must be a string."""
        with self.assertRaises(TypeError):
            Description(description="Example abstract", description_type=123)

    def test_description_rejects_invalid_description_type(self):
        """Checks that description type must be controlled."""
        with self.assertRaises(ValueError):
            Description(
                description="Example abstract",
                description_type="Summary",
            )

    def test_description_lang_must_be_string(self):
        """Checks that description language must be a string."""
        with self.assertRaises(TypeError):
            Description(
                description="Example abstract",
                description_type="Abstract",
                lang=123,
            )

    # GeoLocationPoint tests
    def test_geolocation_point_stores_longitude_and_latitude(self):
        """Checks that a geolocation point stores longitude and latitude."""
        item_point = GeoLocationPoint(
            point_longitude=151.2093,
            point_latitude=-33.8688,
        )

        self.assertEqual(item_point.point_longitude, 151.2093)
        self.assertEqual(item_point.point_latitude, -33.8688)

    def test_geolocation_point_accepts_boundary_values(self):
        """Checks that geolocation point coordinates accept inclusive bounds."""
        item_point = GeoLocationPoint(
            point_longitude=-180.0,
            point_latitude=90.0,
        )

        self.assertEqual(item_point.point_longitude, -180.0)
        self.assertEqual(item_point.point_latitude, 90.0)

    def test_geolocation_point_requires_longitude_and_latitude(self):
        """Checks that geolocation point coordinates are mandatory."""
        with self.assertRaises(TypeError):
            GeoLocationPoint()

    def test_geolocation_point_fields_must_be_keywords(self):
        """Checks that geolocation point fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            GeoLocationPoint(151.2093, -33.8688)

    def test_geolocation_point_longitude_must_be_float(self):
        """Checks that geolocation point longitude must be a float."""
        with self.assertRaises(TypeError):
            GeoLocationPoint(point_longitude=151, point_latitude=-33.8688)

    def test_geolocation_point_latitude_must_be_float(self):
        """Checks that geolocation point latitude must be a float."""
        with self.assertRaises(TypeError):
            GeoLocationPoint(point_longitude=151.2093, point_latitude=-33)

    def test_geolocation_point_rejects_longitude_outside_range(self):
        """Checks that geolocation point longitude must be within valid bounds."""
        for point_longitude in [-180.1, 180.1]:
            with self.subTest(point_longitude=point_longitude):
                with self.assertRaises(ValueError):
                    GeoLocationPoint(
                        point_longitude=point_longitude,
                        point_latitude=-33.8688,
                    )

    def test_geolocation_point_rejects_latitude_outside_range(self):
        """Checks that geolocation point latitude must be within valid bounds."""
        for point_latitude in [-90.1, 90.1]:
            with self.subTest(point_latitude=point_latitude):
                with self.assertRaises(ValueError):
                    GeoLocationPoint(
                        point_longitude=151.2093,
                        point_latitude=point_latitude,
                    )

    # GeoLocationBox tests
    def test_geolocation_box_stores_bounds(self):
        """Checks that a geolocation box stores longitude and latitude bounds."""
        item_box = GeoLocationBox(
            west_bound_longitude=150.0,
            east_bound_longitude=152.0,
            south_bound_latitude=-34.0,
            north_bound_latitude=-33.0,
        )

        self.assertEqual(item_box.west_bound_longitude, 150.0)
        self.assertEqual(item_box.east_bound_longitude, 152.0)
        self.assertEqual(item_box.south_bound_latitude, -34.0)
        self.assertEqual(item_box.north_bound_latitude, -33.0)

    def test_geolocation_box_accepts_boundary_values(self):
        """Checks that geolocation box coordinates accept inclusive bounds."""
        item_box = GeoLocationBox(
            west_bound_longitude=-180.0,
            east_bound_longitude=180.0,
            south_bound_latitude=-90.0,
            north_bound_latitude=90.0,
        )

        self.assertEqual(item_box.west_bound_longitude, -180.0)
        self.assertEqual(item_box.east_bound_longitude, 180.0)
        self.assertEqual(item_box.south_bound_latitude, -90.0)
        self.assertEqual(item_box.north_bound_latitude, 90.0)

    def test_geolocation_box_requires_all_bounds(self):
        """Checks that geolocation box bounds are mandatory."""
        with self.assertRaises(TypeError):
            GeoLocationBox()

    def test_geolocation_box_fields_must_be_keywords(self):
        """Checks that geolocation box fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            GeoLocationBox(150.0, 152.0, -34.0, -33.0)

    def test_geolocation_box_west_bound_longitude_must_be_float(self):
        """Checks that geolocation box west bound longitude must be a float."""
        with self.assertRaises(TypeError):
            GeoLocationBox(
                west_bound_longitude=150,
                east_bound_longitude=152.0,
                south_bound_latitude=-34.0,
                north_bound_latitude=-33.0,
            )

    def test_geolocation_box_east_bound_longitude_must_be_float(self):
        """Checks that geolocation box east bound longitude must be a float."""
        with self.assertRaises(TypeError):
            GeoLocationBox(
                west_bound_longitude=150.0,
                east_bound_longitude=152,
                south_bound_latitude=-34.0,
                north_bound_latitude=-33.0,
            )

    def test_geolocation_box_south_bound_latitude_must_be_float(self):
        """Checks that geolocation box south bound latitude must be a float."""
        with self.assertRaises(TypeError):
            GeoLocationBox(
                west_bound_longitude=150.0,
                east_bound_longitude=152.0,
                south_bound_latitude=-34,
                north_bound_latitude=-33.0,
            )

    def test_geolocation_box_north_bound_latitude_must_be_float(self):
        """Checks that geolocation box north bound latitude must be a float."""
        with self.assertRaises(TypeError):
            GeoLocationBox(
                west_bound_longitude=150.0,
                east_bound_longitude=152.0,
                south_bound_latitude=-34.0,
                north_bound_latitude=-33,
            )

    def test_geolocation_box_rejects_longitudes_outside_range(self):
        """Checks that geolocation box longitudes must be within valid bounds."""
        longitude_cases = [
            ("west_bound_longitude", -180.1),
            ("west_bound_longitude", 180.1),
            ("east_bound_longitude", -180.1),
            ("east_bound_longitude", 180.1),
        ]

        for field_name, field_value in longitude_cases:
            with self.subTest(field_name=field_name, field_value=field_value):
                kwargs = {
                    "west_bound_longitude": 150.0,
                    "east_bound_longitude": 152.0,
                    "south_bound_latitude": -34.0,
                    "north_bound_latitude": -33.0,
                }
                kwargs[field_name] = field_value

                with self.assertRaises(ValueError):
                    GeoLocationBox(**kwargs)

    def test_geolocation_box_rejects_latitudes_outside_range(self):
        """Checks that geolocation box latitudes must be within valid bounds."""
        latitude_cases = [
            ("south_bound_latitude", -90.1),
            ("south_bound_latitude", 90.1),
            ("north_bound_latitude", -90.1),
            ("north_bound_latitude", 90.1),
        ]

        for field_name, field_value in latitude_cases:
            with self.subTest(field_name=field_name, field_value=field_value):
                kwargs = {
                    "west_bound_longitude": 150.0,
                    "east_bound_longitude": 152.0,
                    "south_bound_latitude": -34.0,
                    "north_bound_latitude": -33.0,
                }
                kwargs[field_name] = field_value

                with self.assertRaises(ValueError):
                    GeoLocationBox(**kwargs)

    # PolygonPoint tests
    def test_polygon_point_stores_longitude_and_latitude(self):
        """Checks that a polygon point stores longitude and latitude."""
        item_point = PolygonPoint(
            point_longitude=151.2093,
            point_latitude=-33.8688,
        )

        self.assertEqual(item_point.point_longitude, 151.2093)
        self.assertEqual(item_point.point_latitude, -33.8688)

    def test_polygon_point_accepts_boundary_values(self):
        """Checks that polygon point coordinates accept inclusive bounds."""
        item_point = PolygonPoint(
            point_longitude=180.0,
            point_latitude=-90.0,
        )

        self.assertEqual(item_point.point_longitude, 180.0)
        self.assertEqual(item_point.point_latitude, -90.0)

    def test_polygon_point_requires_longitude_and_latitude(self):
        """Checks that polygon point coordinates are mandatory."""
        with self.assertRaises(TypeError):
            PolygonPoint()

    def test_polygon_point_fields_must_be_keywords(self):
        """Checks that polygon point fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            PolygonPoint(151.2093, -33.8688)

    def test_polygon_point_longitude_must_be_float(self):
        """Checks that polygon point longitude must be a float."""
        with self.assertRaises(TypeError):
            PolygonPoint(point_longitude=151, point_latitude=-33.8688)

    def test_polygon_point_latitude_must_be_float(self):
        """Checks that polygon point latitude must be a float."""
        with self.assertRaises(TypeError):
            PolygonPoint(point_longitude=151.2093, point_latitude=-33)

    def test_polygon_point_rejects_longitude_outside_range(self):
        """Checks that polygon point longitude must be within valid bounds."""
        for point_longitude in [-180.1, 180.1]:
            with self.subTest(point_longitude=point_longitude):
                with self.assertRaises(ValueError):
                    PolygonPoint(
                        point_longitude=point_longitude,
                        point_latitude=-33.8688,
                    )

    def test_polygon_point_rejects_latitude_outside_range(self):
        """Checks that polygon point latitude must be within valid bounds."""
        for point_latitude in [-90.1, 90.1]:
            with self.subTest(point_latitude=point_latitude):
                with self.assertRaises(ValueError):
                    PolygonPoint(
                        point_longitude=151.2093,
                        point_latitude=point_latitude,
                    )

    # GeoLocationPolygon tests
    def example_geolocation_polygon(self):
        PolygonPoint_1 = PolygonPoint(point_longitude=150.0, point_latitude=-34.0)
        PolygonPoint_2 = PolygonPoint(point_longitude=151.0, point_latitude=-35.0)
        PolygonPoint_3 = PolygonPoint(point_longitude=152.0, point_latitude=-36.0)
        PolygonPoint_4 = PolygonPoint(point_longitude=153.0, point_latitude=-37.0)

        return [
            PolygonPoint_1,
            PolygonPoint_2,
            PolygonPoint_3,
            PolygonPoint_4
        ]

    # GeoLocation tests
    def test_geolocation_defaults_place_to_none(self):
        """Checks that a geolocation place can be omitted."""
        item_geolocation = GeoLocation()

        self.assertIsNone(item_geolocation.geolocation_place)
        self.assertIsNone(item_geolocation.geolocation_point)
        self.assertIsNone(item_geolocation.geolocation_box)
        self.assertEqual(item_geolocation.geolocation_polygon, None)

    def test_geolocation_stores_place(self):
        """Checks that a geolocation stores its place."""
        item_geolocation = GeoLocation(geolocation_place="Sydney, Australia")

        self.assertEqual(item_geolocation.geolocation_place, "Sydney, Australia")

    def test_geolocation_stores_point(self):
        """Checks that a geolocation stores a point."""
        item_point = GeoLocationPoint(
            point_longitude=151.2093,
            point_latitude=-33.8688,
        )
        item_geolocation = GeoLocation(
            geolocation_place="Sydney, Australia",
            geolocation_point=item_point,
        )

        self.assertEqual(item_geolocation.geolocation_point, item_point)

    def test_geolocation_stores_box(self):
        """Checks that a geolocation stores a box."""
        item_box = GeoLocationBox(
            west_bound_longitude=150.0,
            east_bound_longitude=152.0,
            south_bound_latitude=-34.0,
            north_bound_latitude=-33.0,
        )
        item_geolocation = GeoLocation(
            geolocation_place="Sydney region",
            geolocation_box=item_box,
        )

        self.assertEqual(item_geolocation.geolocation_box, item_box)

    def test_geolocation_stores_polygon(self):
        """Checks that a geolocation stores multiple polygon points."""

        polygon = self.example_geolocation_polygon()

        item_geolocation = GeoLocation(
            geolocation_polygon=polygon
        )

        self.assertEqual(item_geolocation.geolocation_polygon, polygon)

    def test_geolocation_fields_must_be_keywords(self):
        """Checks that geolocation fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            GeoLocation("Sydney, Australia")

    def test_geolocation_place_must_be_string(self):
        """Checks that geolocation place must be a string."""
        with self.assertRaises(TypeError):
            GeoLocation(geolocation_place=123)

    def test_geolocation_point_must_be_geolocation_point(self):
        """Checks that geolocation points must be a GeoLocationPoint object."""
        with self.assertRaises(TypeError):
            GeoLocation(geolocation_point=["151.2093", "-33.8688"])

    def test_geolocation_box_must_be_geolocation_box(self):
        """Checks that geolocation box must be a GeoLocationBox object."""
        with self.assertRaises(TypeError):
            GeoLocation(geolocation_box=[150.0, 152.0, -34.0, -33.0])

    # FundingReference tests
    def test_funding_reference_stores_required_funder_name(self):
        """Checks that a funding reference stores required and default fields."""
        item_funding_reference = FundingReference(funder_name="Example Funder")

        self.assertEqual(item_funding_reference.funder_name, "Example Funder")
        self.assertIsNone(item_funding_reference.funder_identifier)
        self.assertIsNone(item_funding_reference.funder_identifier_type)
        self.assertIsNone(item_funding_reference.award_title)
        self.assertIsNone(item_funding_reference.award_number)
        self.assertIsNone(item_funding_reference.award_uri)

    def test_funding_reference_stores_identifier_type_and_award_fields(self):
        """Checks that a funding reference stores optional funding metadata."""
        item_funding_reference = FundingReference(
            funder_name="Example Funder",
            funder_identifier="https://ror.org/03yrm5c26",
            funder_identifier_type="ROR",
            award_title="Example Award",
            award_number="AWD-123",
            award_uri="https://example.com/awards/AWD-123",
        )

        self.assertEqual(
            item_funding_reference.funder_identifier,
            "https://ror.org/03yrm5c26",
        )
        self.assertEqual(item_funding_reference.funder_identifier_type, "ROR")
        self.assertEqual(item_funding_reference.award_title, "Example Award")
        self.assertEqual(item_funding_reference.award_number, "AWD-123")
        self.assertEqual(
            item_funding_reference.award_uri,
            "https://example.com/awards/AWD-123",
        )

    def test_funding_reference_requires_funder_name(self):
        """Checks that funding reference funder name is mandatory."""
        with self.assertRaises(TypeError):
            FundingReference()

    def test_funding_reference_fields_must_be_keywords(self):
        """Checks that funding reference fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            FundingReference("Example Funder")

    def test_funding_reference_funder_name_must_be_string(self):
        """Checks that funding reference funder name must be a string."""
        with self.assertRaises(TypeError):
            FundingReference(funder_name=123)

    def test_funding_reference_funder_identifier_must_be_string(self):
        """Checks that funding reference funder identifier must be a string."""
        with self.assertRaises(TypeError):
            FundingReference(
                funder_name="Example Funder",
                funder_identifier=123,
                funder_identifier_type="ROR",
            )

    def test_funding_reference_requires_identifier_type_with_identifier(self):
        """Checks that a funder identifier requires its identifier type."""
        with self.assertRaises(ValueError):
            FundingReference(
                funder_name="Example Funder",
                funder_identifier="https://ror.org/03yrm5c26",
            )

    def test_funding_reference_identifier_type_must_be_string(self):
        """Checks that funding reference identifier type must be a string."""
        with self.assertRaises(TypeError):
            FundingReference(
                funder_name="Example Funder",
                funder_identifier_type=123,
            )

    def test_funding_reference_rejects_invalid_identifier_type(self):
        """Checks that funding reference identifier type must be controlled."""
        with self.assertRaises(ValueError):
            FundingReference(
                funder_name="Example Funder",
                funder_identifier_type="DOI",
            )

    def test_funding_reference_optional_award_fields_must_be_strings(self):
        """Checks that funding reference award metadata fields must be strings."""
        for field_name in ["award_title", "award_number", "award_uri"]:
            with self.subTest(field_name=field_name):
                with self.assertRaises(TypeError):
                    FundingReference(
                        funder_name="Example Funder",
                        **{field_name: 123},
                    )

    # Publisher tests
    def test_publisher_stores_name_and_defaults(self):
        """Checks that a publisher stores its name and default optional fields."""
        item_publisher = Publisher(name="Example Publisher")

        self.assertEqual(item_publisher.name, "Example Publisher")
        self.assertIsNone(item_publisher.publisher_identifier)
        self.assertIsNone(item_publisher.lang)
        self.assertIsNone(item_publisher.publisher_identifier_scheme)
        self.assertIsNone(item_publisher.scheme_uri)

    def test_publisher_stores_identifier_lang_and_scheme_fields(self):
        """Checks that publisher identifier fields are stored."""
        item_publisher = Publisher(
            name="Example Publisher",
            publisher_identifier="https://ror.org/03yrm5c26",
            publisher_identifier_scheme="ROR",
            scheme_uri="https://ror.org/",
            lang="fr",
        )

        self.assertEqual(item_publisher.publisher_identifier, "https://ror.org/03yrm5c26")
        self.assertEqual(item_publisher.lang, "fr")
        self.assertEqual(item_publisher.publisher_identifier_scheme, "ROR")
        self.assertEqual(item_publisher.scheme_uri, "https://ror.org/")

    def test_publisher_requires_name(self):
        """Checks that publisher name is mandatory."""
        with self.assertRaises(TypeError):
            Publisher()

    def test_publisher_fields_must_be_keywords(self):
        """Checks that publisher fields cannot be supplied positionally."""
        with self.assertRaises(TypeError):
            Publisher("Example Publisher")

    def test_publisher_name_must_be_string(self):
        """Checks that publisher name must be a string."""
        with self.assertRaises(TypeError):
            Publisher(name=123)

    def test_publisher_identifier_must_be_string(self):
        """Checks that publisher identifier must be a string."""
        with self.assertRaises(TypeError):
            Publisher(name="Example Publisher", publisher_identifier=123)

    def test_publisher_rejects_invalid_identifier_prefix(self):
        """Checks that publisher identifiers must use an allowed prefix."""
        with self.assertRaises(ValueError):
            Publisher(
                name="Example Publisher",
                publisher_identifier="https://example.com/03yrm5c26",
                publisher_identifier_scheme="ROR",
            )

    def test_publisher_requires_identifier_scheme_when_identifier_is_supplied(self):
        """Checks that publisher identifiers require an explicit scheme."""
        with self.assertRaises(ValueError):
            Publisher(
                name="Example Publisher",
                publisher_identifier="https://ror.org/03yrm5c26",
            )

    def test_publisher_lang_must_be_string(self):
        """Checks that publisher language must be a string."""
        with self.assertRaises(TypeError):
            Publisher(name="Example Publisher", lang=123)

    # Metadata tests
    def test_metadata_stores_identifier(self):
        """Checks that a resource stores its core metadata."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_types = self.example_types()
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=item_types,
        )

        self.assertEqual(item.identifier, item_identifier)
        self.assertEqual(item.creators, [item_creator])
        self.assertEqual(item.titles, [item_title])
        self.assertEqual(item.publisher, item_publisher)
        self.assertEqual(item.publication_year, "2026")
        self.assertEqual(item.types, item_types)
        self.assertEqual(item.language, "en")
        self.assertEqual(item.subjects, [])
        self.assertEqual(item.contributors, [])
        self.assertEqual(item.dates, [])
        self.assertEqual(item.alternate_identifiers, [])
        self.assertEqual(item.related_identifiers, [])
        self.assertEqual(item.descriptions, [])
        self.assertEqual(item.funding_references, [])
        self.assertEqual(item.geolocations, [])

    def test_metadata_stores_custom_language(self):
        """Checks that a resource can store a custom language."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            language="fr",
        )

        self.assertEqual(item.language, "fr")

    def test_metadata_stores_subjects(self):
        """Checks that a resource can store multiple subjects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_subject_1 = Subject(subject="Computer science")
        item_subject_2 = Subject(subject="Metadata", subject_scheme="Keyword")
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            subjects=[item_subject_1, item_subject_2],
        )

        self.assertEqual(item.subjects, [item_subject_1, item_subject_2])

    def test_metadata_stores_contributors(self):
        """Checks that a resource can store multiple contributors."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_contributor_1 = Contributor(
            contributor_name="Grace Hopper",
            name_type="Personal",
            contributor_type="Researcher",
        )
        item_contributor_2 = Contributor(
            contributor_name="Example Organization",
            name_type="Organizational",
            contributor_type="HostingInstitution",
        )
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            contributors=[item_contributor_1, item_contributor_2],
        )

        self.assertEqual(
            item.contributors,
            [item_contributor_1, item_contributor_2],
        )

    def test_metadata_stores_dates(self):
        """Checks that a resource can store multiple dates."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_date_1 = Date(date="2026", date_type="Issued")
        item_date_2 = Date(date="2026-05-01", date_type="Updated")
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            dates=[item_date_1, item_date_2],
        )

        self.assertEqual(item.dates, [item_date_1, item_date_2])

    def test_metadata_stores_descriptions(self):
        """Checks that a resource can store multiple descriptions."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_description_1 = Description(
            description="Example abstract",
            description_type="Abstract",
        )
        item_description_2 = Description(
            description="Example methods",
            description_type="Methods",
        )
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            descriptions=[item_description_1, item_description_2],
        )

        self.assertEqual(
            item.descriptions,
            [item_description_1, item_description_2],
        )

    def test_metadata_stores_geolocations(self):
        """Checks that a resource can store multiple geolocations."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_geolocation_1 = GeoLocation(geolocation_place="Sydney, Australia")
        item_geolocation_2 = GeoLocation(geolocation_place="Canberra, Australia")
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            geolocations=[item_geolocation_1, item_geolocation_2],
        )

        self.assertEqual(
            item.geolocations,
            [item_geolocation_1, item_geolocation_2],
        )

    def test_metadata_stores_funding_references(self):
        """Checks that a resource can store multiple funding references."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_funding_reference_1 = FundingReference(
            funder_name="Example Funder",
        )
        item_funding_reference_2 = FundingReference(
            funder_name="Example Research Council",
            funder_identifier="https://ror.org/03yrm5c26",
            funder_identifier_type="ROR",
            award_number="AWD-123",
        )
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            funding_references=[
                item_funding_reference_1,
                item_funding_reference_2,
            ],
        )

        self.assertEqual(
            item.funding_references,
            [item_funding_reference_1, item_funding_reference_2],
        )

    def test_metadata_stores_alternate_identifiers(self):
        """Checks that a resource can store multiple alternate identifiers."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_alternate_identifier_1 = AlternateIdentifier(
            alternate_identifier_type="Local accession number",
            alternate_identifier="ABC123",
        )
        item_alternate_identifier_2 = AlternateIdentifier(
            alternate_identifier_type="Legacy ID",
            alternate_identifier="LEGACY-456",
        )
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            alternate_identifiers=[
                item_alternate_identifier_1,
                item_alternate_identifier_2,
            ],
        )

        self.assertEqual(
            item.alternate_identifiers,
            [item_alternate_identifier_1, item_alternate_identifier_2],
        )

    def test_metadata_stores_related_identifiers(self):
        """Checks that a resource can store multiple related identifiers."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_related_identifier_1 = RelatedIdentifier(
            related_identifier="10.123/example-related",
            related_identifier_type="DOI",
            relation_type="References",
        )
        item_related_identifier_2 = RelatedIdentifier(
            related_identifier="https://example.com/related",
            related_identifier_type="URL",
            relation_type="IsSupplementTo",
            resource_type_general="Dataset",
        )
        item = Metadata(
            identifier=item_identifier,
            creators=[item_creator],
            titles=[item_title],
            publisher=item_publisher,
            publication_year="2026",
            types=self.example_types(),
            related_identifiers=[
                item_related_identifier_1,
                item_related_identifier_2,
            ],
        )

        self.assertEqual(
            item.related_identifiers,
            [item_related_identifier_1, item_related_identifier_2],
        )

    def test_metadata_stores_no_identifier_by_default(self):
        """Checks that metadata can be created before a DOI is allocated."""
        item_metadata = Metadata(
            creators=[Creator(creator_name="Ada Lovelace", name_type="Personal")],
            titles=[Title(title="Example resource")],
            publisher=Publisher(name="Example Publisher"),
            publication_year="2026",
            types=self.example_types(),
        )

        self.assertIsNone(item_metadata.identifier)

    def test_metadata_identifier_must_be_identifier(self):
        """Checks that metadata identifier must be an Identifier object."""
        with self.assertRaises(TypeError):
            Metadata(
                identifier="10.123/example",
                creators=[Creator(creator_name="Ada Lovelace", name_type="Personal")],
                titles=[Title(title="Example resource")],
                publisher=Publisher(name="Example Publisher"),
                publication_year="2026",
                types=self.example_types(),
            )

    def test_metadata_requires_at_least_one_creator(self):
        """Checks that a resource must have at least one creator."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(ValueError):
            Metadata(
                identifier=item_identifier,
                creators=[],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
            )

    def test_metadata_requires_at_least_one_title(self):
        """Checks that a resource must have at least one title."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(ValueError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
            )

    def test_metadata_requires_publisher(self):
        """Checks that a resource publisher is mandatory."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publication_year="2026",
                types=self.example_types(),
            )

    def test_metadata_fields_must_be_keywords(self):
        """Checks that resource fields cannot be supplied positionally."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(item_identifier, [item_creator], [item_title], item_publisher)

    def test_metadata_defaults_publication_year_to_current_year(self):
        """Checks that a resource publication year defaults to the current year."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with patch("doi_manager.models.datetime") as mock_datetime:
            mock_datetime.now.return_value.year = datetime.now().year

            item_metadata = Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                types=self.example_types(),
            )

        self.assertEqual(item_metadata.publication_year, str(datetime.now().year))

    def test_metadata_requires_types(self):
        """Checks that a resource types object is mandatory."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
            )

    def test_metadata_types_must_be_types(self):
        """Checks that resource types must be a Types object."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types="Dataset",
            )

    def test_metadata_publication_year_must_be_string(self):
        """Checks that resource publication year must be a string."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year=2026,
                types=self.example_types(),
            )

    def test_metadata_language_must_be_string(self):
        """Checks that resource language must be a string."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                language=123,
            )

    def test_metadata_rejects_invalid_publication_year_format(self):
        """Checks that resource publication year must be exactly four digits."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        for publication_year in ["26", "202A"]:
            with self.subTest(publication_year=publication_year):
                with self.assertRaises(ValueError):
                    Metadata(
                        identifier=item_identifier,
                        creators=[item_creator],
                        titles=[item_title],
                        publisher=item_publisher,
                        publication_year=publication_year,
                        types=self.example_types(),
                    )

    def test_metadata_publisher_must_be_publisher(self):
        """Checks that a resource publisher must be a Publisher object."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher="Example Publisher",
                publication_year="2026",
                types=self.example_types(),
            )

    def test_metadata_subjects_must_be_list(self):
        """Checks that resource subjects must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_subject = Subject(subject="Computer science")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                subjects=item_subject,
            )

    def test_metadata_subjects_must_contain_subjects(self):
        """Checks that resource subjects must contain Subject objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                subjects=["Computer science"],
            )

    def test_metadata_contributors_must_be_list(self):
        """Checks that resource contributors must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_contributor = Contributor(
            contributor_name="Grace Hopper",
            name_type="Personal",
            contributor_type="Researcher",
        )

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                contributors=item_contributor,
            )

    def test_metadata_contributors_must_contain_contributors(self):
        """Checks that resource contributors must contain Contributor objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                contributors=["Grace Hopper"],
            )

    def test_metadata_dates_must_be_list(self):
        """Checks that resource dates must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_date = Date(date="2026", date_type="Issued")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                dates=item_date,
            )

    def test_metadata_dates_must_contain_dates(self):
        """Checks that resource dates must contain Date objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                dates=["2026"],
            )

    def test_metadata_alternate_identifiers_must_be_list(self):
        """Checks that resource alternate identifiers must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_alternate_identifier = AlternateIdentifier(
            alternate_identifier_type="Local accession number",
            alternate_identifier="ABC123",
        )

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                alternate_identifiers=item_alternate_identifier,
            )

    def test_metadata_alternate_identifiers_must_contain_alternate_identifiers(self):
        """Checks that resource alternate identifiers contain correct objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                alternate_identifiers=["ABC123"],
            )

    def test_metadata_related_identifiers_must_be_list(self):
        """Checks that resource related identifiers must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_related_identifier = RelatedIdentifier(
            related_identifier="10.123/example-related",
            related_identifier_type="DOI",
            relation_type="References",
        )

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                related_identifiers=item_related_identifier,
            )

    def test_metadata_related_identifiers_must_contain_related_identifiers(self):
        """Checks that resource related identifiers contain correct objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                related_identifiers=["10.123/example-related"],
            )

    def test_metadata_descriptions_must_be_list(self):
        """Checks that resource descriptions must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_description = Description(
            description="Example abstract",
            description_type="Abstract",
        )

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                descriptions=item_description,
            )

    def test_metadata_descriptions_must_contain_descriptions(self):
        """Checks that resource descriptions contain Description objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                descriptions=["Example abstract"],
            )

    def test_metadata_geolocations_must_be_list(self):
        """Checks that resource geolocations must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_geolocation = GeoLocation(geolocation_place="Sydney, Australia")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                geolocations=item_geolocation,
            )

    def test_metadata_geolocations_must_contain_geolocations(self):
        """Checks that resource geolocations contain GeoLocation objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                geolocations=["Sydney, Australia"],
            )

    def test_metadata_funding_references_must_be_list(self):
        """Checks that resource funding references must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")
        item_funding_reference = FundingReference(funder_name="Example Funder")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                funding_references=item_funding_reference,
            )

    def test_metadata_funding_references_must_contain_funding_references(self):
        """Checks that resource funding references contain correct objects."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                funding_references=["Example Funder"],
            )

    def test_metadata_sizes_must_be_list(self):
        """Checks that resource sizes must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                sizes="10 MB"
            )

    def test_metadata_sizes_must_be_list_of_strings(self):
        """Checks that resource sizes must be supplied as a list of strings."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                sizes=["10 MB", 2034]
            )

    def test_metadata_formats_must_be_list(self):
        """Checks that resource formats must be supplied as a list."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                formats="jpeg"
            )

    def test_metadata_formats_must_be_list_of_strings(self):
        """Checks that resource formats must be supplied as a list of strings."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                formats=["jpeg", 2034]
            )

    def test_metadata_version_must_be_string(self):
        """Checks that resource version must be a string."""
        item_identifier = Identifier(
            identifier_value="10.123/example",
            identifier_type_attr="doi",
        )
        item_creator = Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
        item_title = Title(title="Example resource")
        item_publisher = Publisher(name="Example Publisher")

        with self.assertRaises(TypeError):
            Metadata(
                identifier=item_identifier,
                creators=[item_creator],
                titles=[item_title],
                publisher=item_publisher,
                publication_year="2026",
                types=self.example_types(),
                version = [3.2]
            )


if __name__ == "__main__":
    unittest.main()
