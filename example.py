import random
from doi_manager import (
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
    NameIdentifier,
    PolygonPoint,
    Publisher,
    Record,
    RelatedIdentifier,
    Metadata,
    Subject,
    Title,
    Types,
    Rights,
    create_draft_and_assign_doi,
)

TITLES = [
    "Thermo Fisher Scientific Orbitrap Exploris 240",
    "Agilent Technologies 6545 Q-TOF LC/MS",
    "Waters Xevo G2-XS QTof",
    "Bruker timsTOF Pro",
    "Shimadzu Nexera X2 UHPLC",
    "Bio-Rad CFX96 Touch Real-Time PCR System",
    "PerkinElmer Lambda 365 UV/Vis Spectrophotometer",
    "Leica Microsystems DM6 B Upright Microscope",
    "ZEISS LSM 980 Confocal Microscope",
]


# Create some affiliations that can be attached to people or organizations.
affiliation_1 = Affiliation(
    name="UNSW Sydney",
    affiliation_identifier="https://ror.org/03r8z3t63",
    affiliation_identifier_scheme="ROR",
    scheme_uri="https://ror.org/",
)
affiliation_2 = Affiliation(
    name="The University of Melbourne",
    affiliation_identifier="https://ror.org/01ej9dk98",
    affiliation_identifier_scheme="ROR",
    scheme_uri="https://ror.org/",
)

# Create an optional alternate identifier for the resource.
item_alternate_identifier_1 = AlternateIdentifier(
    alternate_identifier_type="Local accession number",
    alternate_identifier="ABC123",
)
item_alternate_identifier_2 = AlternateIdentifier(
    alternate_identifier_type="Internal ID",
    alternate_identifier="XYZ12345",
)

# Create optional related identifiers for linked resources.
item_related_identifier_1 = RelatedIdentifier(
    related_identifier="https://doi.org/10.123/5435493",
    related_identifier_type="DOI",
    relation_type="References",
    resource_type_general="Dataset",
    relation_type_information="Referenced dataset",
)
item_related_identifier_2 = RelatedIdentifier(
    related_identifier="https://doi.org/10.123/2836829",
    related_identifier_type="DOI",
    relation_type="IsSupplementTo",
    resource_type_general="Text",
    relation_type_information="Supplementary instrument documentation",
)
item_related_identifier_3 = RelatedIdentifier(
    related_identifier="https://example.com/instruments/example-manual",
    related_identifier_type="URL",
    relation_type="Documents",
    resource_type_general="Instrument",
    relation_type_information="Instrument manual",
)

# Create creators with an ORCID name identifier.
creator_name_identifier_1 = NameIdentifier(
    name_identifier="https://orcid.org/0000-0002-1825-0097",
    name_identifier_scheme="ORCID",
    scheme_uri="https://orcid.org",
)
creator_name_identifier_2 = NameIdentifier(
    name_identifier="https://orcid.org/0000-0002-1825-0098",
    name_identifier_scheme="ORCID",
    scheme_uri="https://orcid.org",
)
creator_1 = Creator(
    creator_name="Ada Lovelace",
    name_type="Personal",
    name_identifiers=[creator_name_identifier_1],
    affiliations=[affiliation_1, affiliation_2],
)

creator_2 = Creator(
    creator_name="Alan Turing",
    name_type="Personal",
    name_identifiers=[creator_name_identifier_2],
    affiliations=[affiliation_1],
)

# Create an optional contributor with an ORCID name identifier and affiliation.
contributor_identifier = NameIdentifier(
    name_identifier="https://orcid.org/0000-0001-5109-3700",
    name_identifier_scheme="ORCID",
    scheme_uri="https://orcid.org",
)
item_contributor = Contributor(
    contributor_name="Grace Hopper",
    name_type="Personal",
    contributor_type="Researcher",
    name_identifiers=[contributor_identifier],
    affiliations=[affiliation_1],
)

# Create multiple titles. The first overrides the default language.
item_title_1 = Title(title=random.choice(TITLES), lang="fr")
item_title_2 = Title(title="Metadata documentation", type="Subtitle")

# Create the required resource type metadata.
item_types = Types(
    resource_type="Primary Dataset",
    resource_type_general="Dataset",
)

# Create optional subjects for the resource.
item_subject_1 = Subject(subject="Global warming")
item_subject_2 = Subject(
    subject="Climate change processes",
    subject_scheme="ANZSRC Fields of Research",
    classification_code="370201",
)

# Create optional dates for the resource.
item_date_1 = Date(date="2026", date_type="Issued")
item_date_2 = Date(
    date="2026-05-01",
    date_type="Updated",
    date_information="Metadata updated",
)

# Create optional descriptions for the resource.
item_description_1 = Description(
    description="An example abstract for the resource.",
    description_type="Abstract",
)
item_description_2 = Description(
    description="An example methods description for the resource.",
    description_type="Methods",
    lang="fr",
)

# Create optional geolocations for the resource.
item_geolocation_1 = GeoLocation(
    geolocation_place="Canberra, Australia",
)

item_geolocation_point_2 = GeoLocationPoint(
    point_longitude=151.2093,
    point_latitude=-33.8688,
)
item_geolocation_2 = GeoLocation(
    geolocation_point=item_geolocation_point_2,
)

item_geolocation_box_3 = GeoLocationBox(
    west_bound_longitude=149.0,
    east_bound_longitude=150.0,
    south_bound_latitude=-36.0,
    north_bound_latitude=-35.0,
)
item_geolocation_3 = GeoLocation(
    geolocation_box=item_geolocation_box_3,
)

polygon_point_1=PolygonPoint(point_longitude=149.0, point_latitude=-36.0)
polygon_point_2=PolygonPoint(point_longitude=150.0, point_latitude=-37.0)
polygon_point_3=PolygonPoint(point_longitude=151.0, point_latitude=-38.0)
polygon_point_4=PolygonPoint(point_longitude=152.0, point_latitude=-39.0)

item_geolocation_polygon = [
    vars(polygon_point_1),
    vars(polygon_point_2),
    vars(polygon_point_3),
    vars(polygon_point_4)
]

item_geolocation_4 = GeoLocation(
    geolocation_polygon=item_geolocation_polygon
)

# Create the single publisher required by the resource.
item_publisher = Publisher(
    name="UNSW Sydney",
    publisher_identifier="https://ror.org/03r8z3t63",
    publisher_identifier_scheme="ROR",
    scheme_uri="https://ror.org/",
    lang="en",
)

# Create optional rights for the resource.
item_rights_1 = Rights(
    rights="Creative Commons Attribution 4.0 International",
    rights_uri="https://creativecommons.org/licenses/by/4.0/",
    scheme_uri="https://spdx.org/licenses/",
    rights_identifier="CC BY 4.0",
    rights_identifier_scheme="SPDX",
    lang="en"
)

# Create optional funding references for the resource.
item_funding_reference_1 = FundingReference(
    funder_name="Australian Research Council",
    funder_identifier="https://ror.org/05mmh0f86",
    funder_identifier_type="ROR",
    award_title="ARC LIEF Award 123ABC",
    award_number="AWD-123",
    award_uri="https://example.com/awards/AWD-123",
)

# Create a record and assign the metadata to it.
record = Record()

# Create an alternate identifier for the record UUID itself.
item_alternate_identifier_record = AlternateIdentifier(
    alternate_identifier_type="local UNSW identifier",
    alternate_identifier=record.identifier,
)

# Assemble the metadata from its required child objects.
metadata = Metadata(
    creators=[creator_1, creator_2],
    titles=[item_title_1, item_title_2],
    publisher=item_publisher,
    publication_year="2026",
    types=item_types,
    language="en",
    subjects=[item_subject_1, item_subject_2],
    contributors=[item_contributor],
    dates=[item_date_1, item_date_2],
    alternate_identifiers=[
        item_alternate_identifier_1,
        item_alternate_identifier_2,
        item_alternate_identifier_record,
    ],
    related_identifiers=[
        item_related_identifier_1,
        item_related_identifier_2,
        item_related_identifier_3,
    ],
    sizes=["1 GB", "2 GB"],
    formats=["text/csv", "application/json"],
    version="1.0",
    descriptions=[item_description_1, item_description_2],
    geolocations=[item_geolocation_1, item_geolocation_2, item_geolocation_3, item_geolocation_4],
    funding_references=[item_funding_reference_1],
    rights_list=[item_rights_1]
)


# Attach the record metadata to the record
record.metadata = metadata

# Allocate a DOI through DataCite and store the returned DOI on the record metadata.
allocated_doi = create_draft_and_assign_doi(record)


# Inspect the record identifier and assigned metadata.
print(f"Record identifier: {record.identifier}")
print(f"Record metadata identifier before DOI allocation: {record.metadata.identifier}")

print(f"Allocated DOI: {allocated_doi.identifier_value}")
print(f"Record metadata identifier after DOI allocation: {record.metadata.identifier.identifier_value}")

# Inspect the resource identifier.
print(f"Identifier value: {metadata.identifier.identifier_value}")
print(f"Identifier type: {metadata.identifier.identifier_type_attr}")

# Inspect the first alternate identifier.
print(
    "Alternate identifier 1 type: "
    f"{metadata.alternate_identifiers[0].alternate_identifier_type}"
)
print(f"Alternate identifier 1: {metadata.alternate_identifiers[0].alternate_identifier}")
print(
    "Alternate identifier 2 type: "
    f"{metadata.alternate_identifiers[1].alternate_identifier_type}"
)
print(f"Alternate identifier 2: {metadata.alternate_identifiers[1].alternate_identifier}")

# Inspect the related identifiers.
for index, related_identifier in enumerate(metadata.related_identifiers, start=1):
    print(f"Related identifier {index}: {related_identifier.related_identifier}")
    print(
        f"Related identifier {index} type: "
        f"{related_identifier.related_identifier_type}"
    )
    print(
        f"Related identifier {index} relation: "
        f"{related_identifier.relation_type}"
    )
    print(
        f"Related identifier {index} resource type general: "
        f"{related_identifier.resource_type_general}"
    )
    print(
        f"Related identifier {index} relation information: "
        f"{related_identifier.relation_type_information}"
    )

# Inspect the first creator.
print(f"Creator name: {metadata.creators[0].creator_name}")
print(f"Creator name type: {metadata.creators[0].name_type}")
print(f"Creator name identifier: {metadata.creators[0].name_identifiers[0].name_identifier}")

# Inspect the first contributor.
print(f"Contributor name: {metadata.contributors[0].contributor_name}")
print(f"Contributor name type: {metadata.contributors[0].name_type}")
print(f"Contributor type: {metadata.contributors[0].contributor_type}")
print(
    "Contributor name identifier: "
    f"{metadata.contributors[0].name_identifiers[0].name_identifier}"
)
print(f"Contributor affiliation: {metadata.contributors[0].affiliations[0].name}")
print(
    "Contributor affiliation identifier: "
    f"{metadata.contributors[0].affiliations[0].affiliation_identifier}"
)

# Inspect the first title.
print(f"Title 1 text: {metadata.titles[0].title}")
print(f"Title 1 language: {metadata.titles[0].lang}")
print(f"Title 1 type: {metadata.titles[0].type}")

# Inspect the second title.
print(f"Title 2 text: {metadata.titles[1].title}")
print(f"Title 2 language: {metadata.titles[1].lang}")
print(f"Title 2 type: {metadata.titles[1].type}")

# Inspect the resource types.
print(f"Resource type: {metadata.types.resource_type}")
print(f"Resource type general: {metadata.types.resource_type_general}")

# Inspect the subjects.
print(f"Subject 1 text: {metadata.subjects[0].subject}")
print(f"Subject 1 language: {metadata.subjects[0].lang}")
print(f"Subject 2 text: {metadata.subjects[1].subject}")
print(f"Subject 2 scheme: {metadata.subjects[1].subject_scheme}")
print(f"Subject 2 classification code: {metadata.subjects[1].classification_code}")

# Inspect the dates.
print(f"Date 1 value: {metadata.dates[0].date}")
print(f"Date 1 type: {metadata.dates[0].date_type}")
print(f"Date 2 value: {metadata.dates[1].date}")
print(f"Date 2 type: {metadata.dates[1].date_type}")
print(f"Date 2 information: {metadata.dates[1].date_information}")

# Inspect the descriptions.
print(f"Description 1 text: {metadata.descriptions[0].description}")
print(f"Description 1 type: {metadata.descriptions[0].description_type}")
print(f"Description 1 language: {metadata.descriptions[0].lang}")
print(f"Description 2 text: {metadata.descriptions[1].description}")
print(f"Description 2 type: {metadata.descriptions[1].description_type}")
print(f"Description 2 language: {metadata.descriptions[1].lang}")

# Inspect the geolocations.
print(
    f"Geolocation 1 place: {metadata.geolocations[0].geolocation_place}"
)

print(
    f"Geolocation 2 point latitude: {metadata.geolocations[1].geolocation_point.point_latitude}"
)

print(
    f"Geolocation 2 point longitude: {metadata.geolocations[1].geolocation_point.point_longitude}"
)

print(
    f"Geolocation 3 box west longitude: {metadata.geolocations[2].geolocation_box.west_bound_longitude}"
)

print(
    f"Geolocation 3 box east longitude: {metadata.geolocations[2].geolocation_box.east_bound_longitude}"
)

print(
    f"Geolocation 3 box north latitude: {metadata.geolocations[2].geolocation_box.north_bound_latitude}"
)

print(
    f"Geolocation 3 box south latitude: {metadata.geolocations[2].geolocation_box.south_bound_latitude}"
)


# Inspect the publisher and its explicit identifier fields.
print(f"Publisher name: {metadata.publisher.name}")
print(
    f"Publisher identifier scheme: {metadata.publisher.publisher_identifier_scheme}"
)
print(f"Publisher scheme URI: {metadata.publisher.scheme_uri}")
print(f"Publisher language: {metadata.publisher.lang}")

# Inspect the resource publication year.
print(f"Publication year: {metadata.publication_year}")
print(f"Metadata language: {metadata.language}")

# Inspect the resource sizes and formats.
print(f"Metadata sizes: {metadata.sizes}")
print(f"Metadata formats: {metadata.formats}")

# Inspect the resource version.
print(f"Metadata version: {metadata.version}")  

# Inspect the funding references.
print(f"Funding reference 1 funder: {metadata.funding_references[0].funder_name}")
print(
    "Funding reference 1 identifier: "
    f"{metadata.funding_references[0].funder_identifier}"
)
print(
    "Funding reference 1 identifier type: "
    f"{metadata.funding_references[0].funder_identifier_type}"
)
print(f"Funding reference 1 award title: {metadata.funding_references[0].award_title}")
print(f"Funding reference 1 award number: {metadata.funding_references[0].award_number}")
print(f"Funding reference 1 award URI: {metadata.funding_references[0].award_uri}")

# Inspect the rights.
print(f"Rights 1 identifier: {metadata.rights_list[0].rights_identifier}")
print(f"Rights 1 URI: {metadata.rights_list[0].rights_uri}")
