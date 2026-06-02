## doi_manager

`doi_manager` is a small library for building DOI metadata records and sending
them to DataCite.

### Install

Install the latest version from the default branch:

```bash
python -m pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

Replace `YOUR_USERNAME/YOUR_REPO` with the GitHub owner and repository name.

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

For example:

```text
my_project/
+-- config.py
+-- create_doi.py
```


### Example Use

```python
from doi_manager import (
    Affiliation,
    Creator,
    Metadata,
    Record,
    Publisher,
    NameIdentifier,
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
    name_identifier="https://ror.org/01trzbr20",
    name_identifier_scheme="ROR",
    scheme_uri="https://ror.org",
)

# Create Personal Creator with an ORCID name identifier and affiliation.
creator_1 = Creator(
    creator_name="Josiah Carberry",
    name_type="Personal",
    name_identifiers=[name_identifier_1],
    affiliations=[affiliation_1],
)

# Create Organizational Creator with an ROR name identifier.
creator_2 = Creator(
    creator_name="Mark Wainwright Analytical Centre",
    name_type="Organizational",
    name_identifiers=[name_identifier_2],
)

# Create a Publisher entry
publisher = Publisher(
    name="UNSW Sydney",
    publisher_identifier="https://ror.org/03r8z3t63",
    publisher_identifier_scheme="ROR",
    scheme_uri = "https://ror.org/",
    lang="en",
)

# Create Subject entries
subject_1 = Subject(
    subject="Climate change processes",
    schemeUri="https://www.abs.gov.au/statistics/classifications/australian-and-new-zealand-standard-research-classification-anzsrc",
    subject_scheme="ANZSRC Fields of Research",
    classification_code="370201",
)
# Create a Subject entry 2
subject_2 = Subject(
    subject="Climatalogy",
    schemeUri="https://www.abs.gov.au/statistics/classifications/australian-and-new-zealand-standard-research-classification-anzsrc",
    subject_scheme="ANZSRC Fields of Research",
    classification_code="370202",
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
    language="en"
)

record = Record(metadata=metadata)
identifier = create_draft_and_assign_doi(record)

print(identifier.identifier_value)
```

`create_draft_and_assign_doi` creates a draft DOI in DataCite, stores the
returned DOI on `record.metadata.identifier`, and returns the new identifier.
