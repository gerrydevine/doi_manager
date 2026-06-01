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


### Use

```python
from doi_manager import (
    Creator,
    Metadata,
    Publisher,
    Record,
    Title,
    Types,
    create_draft_and_assign_doi,
)

metadata = Metadata(
    creators=[
        Creator(
            creator_name="Ada Lovelace",
            name_type="Personal",
        )
    ],
    titles=[
        Title(title="Example research dataset"),
    ],
    publisher=Publisher(name="Example University"),
    publication_year="2026",
    types=Types(
        resource_type="Dataset",
        resource_type_general="Dataset",
    ),
)

record = Record(metadata=metadata)

identifier = create_draft_and_assign_doi(record)

print(identifier.identifier_value)
```

`create_draft_and_assign_doi` creates a draft DOI in DataCite, stores the
returned DOI on `record.metadata.identifier`, and returns the new identifier.
