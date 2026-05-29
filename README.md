## doi_manager

`doi_manager` is a small library for building DOI metadata records and sending
them to DataCite.

### Install

Install the latest version from the default branch:

```bash
python -m pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

Install from a specific branch:

```bash
python -m pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO.git@main
```

Install from a specific release tag:

```bash
python -m pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO.git@v0.1.0
```

Replace `YOUR_USERNAME/YOUR_REPO` with the GitHub owner and repository name.

### Local development

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

### Use

```python
from doi_manager import (
    Affiliation,
    Creator,
    Metadata,
    Record,
    Publisher,
    Title,
    Types,
    create_draft_and_assign_doi,
)

record = Record(metadata=metadata)
identifier = create_draft_and_assign_doi(
    record,
    doi_prefix="10.80402",
    datacite_url="https://api.test.datacite.org/dois",
)
```
