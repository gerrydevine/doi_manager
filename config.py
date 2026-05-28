from pathlib import Path

DATACITE_URL = 'https://api.test.datacite.org/dois'
DOI_PREFIX = '10.80402'

# Resolve the spreadsheet relative to this config file, not the current shell.
INPUT_EXCEL = Path(__file__).resolve().parent / 'inputs' / 'inputs.xlsx'
