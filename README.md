## DOI Manager

`doi_manager` is a small library for building DOI metadata records and sending
them to DataCite for DOI allocation.

### Install

Install the latest version from the default branch:

```bash
python -m pip install git+https://github.com/gerrydevine/doi_manager.git
```

### DataCite credentials

`doi_manager` expects DataCite credentials to be stored in a `.env` file in the
directory where your script is run:

```dotenv
DATACITE_USERNAME=your.datacite.username
DATACITE_PASSWORD=your.datacite.password
```

Exercise caution in exposing this file.

### DataCite config

`doi_manager` expects the DataCite API URL and DOI prefix to be defined in a
`config.py` file in your own project, alongside the script that uses the
library:

```python
DATACITE_URL = "https://api.test.datacite.org/dois"
DOI_PREFIX = "10.80402"
```

### Example Use

```python
from doi_manager import (
    Affiliation,
    Creator,
    Contributor,
    Description,
    Metadata,
    Record,
    Date,
    Publisher,
    Subject,
    NameIdentifier,
    FundingReference,
    AlternateIdentifier,
    RelatedIdentifier,
    Title,
    Types,
    create_draft_and_assign_doi,
)

# Create affiliation and name identifier for creator 1.
affiliation_1 = Affiliation(
    name="UNSW Sydney",
    affiliation_identifier="https://ror.org/03r8z3t63",
    affiliation_identifier_scheme="ROR",
    scheme_uri="https://ror.org/",
)
name_identifier_1 = NameIdentifier(
    name_identifier="https://orcid.org/0000-0002-1825-0097",
    name_identifier_scheme="ORCID",
    scheme_uri="https://orcid.org",
)

# Create name identifier for creator 2.
name_identifier_2 = NameIdentifier(
    name_identifier="https://orcid.org/0000-0002-1825-0097",
    name_identifier_scheme="ORCID",
    scheme_uri="https://orcid.org",
)

# Create Personal Creator 1 with an ORCID name identifier and affiliation.
creator_1 = Creator(
    creator_name="Josiah Carberry",
    name_type="Personal",
    name_identifiers=[name_identifier_1],
    affiliations=[affiliation_1],
)

creator_2 = Creator(
    creator_name="Janet White",
    name_type="Personal",
    name_identifiers=[name_identifier_2],
)

# Create Organizational Creator with an ROR name identifier.
name_identifier_3 = NameIdentifier(
    name_identifier="https://ror.org/03r8z3t63",
    name_identifier_scheme="ROR",
    scheme_uri="https://ror.org",
)
contributor_1 = Contributor(
    contributor_name="UNSW",
    name_type="Organizational",
    contributor_type="HostingInstitution",
    name_identifiers=[name_identifier_3],
)

# Create a Publisher entry
publisher = Publisher(
    name="UNSW Sydney",
    publisher_identifier="https://ror.org/03r8z3t63",
    publisher_identifier_scheme="ROR",
    scheme_uri = "https://ror.org/",
    lang="en",
)

# Create an abstract
description_1 = Description(
    description="""
        The Thermo Scientific Orbitrap Exploris 240 is a high-resolution accurate-mass LC-MS/MS mass 
        spectrometer designed for research labs that need strong qualitative identification and reliable 
        quantitative performance across complex samples.
        It uses Thermo Fishers High-Field Orbitrap mass analyzer to deliver high mass resolution, 
        accurate mass measurement, and high-quality MS/MS spectra. Thermo Fisher positions it as a 
        versatile “workhorse” system for applications such as proteomics, translational proteomics, 
        metabolomics, biotherapeutic characterization, intact protein analysis, clinical research, 
        food/beverage testing, environmental analysis, and PFAS-related workflows.
    """,
    description_type="Abstract",
)

# Create a Subject entry 1
subject_1 = Subject(
    subject="Climate change processes",
    scheme_uri="https://www.abs.gov.au/statistics/classifications/australian-and-new-zealand-standard-research-classification-anzsrc",
    subject_scheme="ANZSRC Fields of Research",
    classification_code="370201",
)
# Create a Subject entry 2
subject_2 = Subject(
    subject="Climatalogy",
    scheme_uri="https://www.abs.gov.au/statistics/classifications/australian-and-new-zealand-standard-research-classification-anzsrc",
    subject_scheme="ANZSRC Fields of Research",
    classification_code="370202",
)

# Add Funding
funding_reference_1 = FundingReference(
    funder_name="Australian Research Council",
    funder_identifier="https://ror.org/05mmh0f86",
    funder_identifier_type="ROR",
    award_title="ARC LIEF Award 123ABC",
    award_number="AWD-123",
    award_uri="https://example.com/awards/AWD-123",
)

# Add an alternate identifier for the record.
alternate_identifier = AlternateIdentifier(
    alternate_identifier_type="local identifier",
    alternate_identifier="SOSNTV6-63BSTDB",
)

# Add a related identifier
related_identifier_1 = RelatedIdentifier(
    related_identifier="https://doi.org/10.123/5435493",
    related_identifier_type="DOI",
    relation_type="IsDescribedBy",
    resource_type_general="JournalArticle",
    relation_type_information="Documentation journal article",
)

# Add a date issued
date_1 = Date(
    date="2026", 
    date_type="Issued"
)

metadata = Metadata(
    creators=[creator_1, creator_2],
    titles=[
        Title(title="Thermo Fisher Scientific Orbitrap Exploris 240"),
    ],
    publisher=publisher,
    publication_year="2026",
    types=Types(
        resource_type="Instrument",
        resource_type_general="Instrument",
    ),
    subjects=[subject_1, subject_2],
    descriptions=[description_1],
    funding_references=[funding_reference_1],
    dates=[date_1],
    alternate_identifiers=[alternate_identifier],
    related_identifiers=[related_identifier_1,],
    language="en"
)

record = Record(metadata=metadata)
identifier = create_draft_and_assign_doi(record)

print(identifier.identifier_value)
```

`create_draft_and_assign_doi` creates a __draft__ record in DataCite, generates a DOI and returns the Datacite response.
