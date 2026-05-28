#!/usr/bin/env python3

from pathlib import Path
import sys

import pandas as pd

from config import INPUT_EXCEL

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import DATACITE_URL, DOI_PREFIX
from landing_page_utils import generate_landing_page
from datacite_client import allocate_doi
from models import (
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


def read_excel_with_tabs(excel_file):
    """
    Reads an Excel spreadsheet with multiple tabs and returns a dictionary of DataFrames.

    Parameters:
        excel_file (str): The path to or name of the Excel file.

    Returns:
        dict: A dictionary where the keys are sheet names and the values are DataFrames.
    """
    try:
        # Use pandas to read the Excel file with all sheets
        sheets = pd.read_excel(excel_file, sheet_name=None)
        return sheets
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None


def _split_ids(value):
    if pd.isna(value):
        return []

    if isinstance(value, str):
        return [item.strip() for item in value.split("|") if item.strip()]

    return [str(value)]


def _first_cell(frame, column_name):
    return frame[column_name].values[0]


def handle_creator(creator_id):
    creator = creators_df.loc[creators_df['ID'] == creator_id]

    creator_name = _first_cell(creator, 'creatorName')
    name_type = _first_cell(creator, 'nameType')
    name_identifier = _first_cell(creator, 'nameIdentifier')

    # TODO implement multiple identifiers in spreadsheet cell (seperated by |)
    return Creator(
        creator_name = creator_name,
        name_type = name_type,
        name_identifiers = [name_identifier]
    )


# READ IN SPREADSHEET
# BATCH_FILE = Path(__file__).resolve().with_name('inputs.xlsx')
data = read_excel_with_tabs(INPUT_EXCEL)

for sheet_name, df in data.items():
    globals()[f"{sheet_name.replace(' ', '_').lower()}_df"] = df

# Loop through main records sheet/dataframe
for index, row in records_df.iterrows():
    # Get Title
    title = Title(title=row['Title'])

    # Get Resource Type
    resource_type = Types(
        resource_type=row['Type'],
        resource_type_general=row['Type'],
    )

    # Get Publisher (Hard-coded)
    publisher = Publisher(
        name="UNSW Sydney",
        identifier="https://ror.org/03r8z3t63",
    )

    # Get Creator(s)
    creators = []
    creator_ids = _split_ids(row['Creators'])

    for creator_id in creator_ids:
        creator_details = handle_creator(int(creator_id))
        creators.append(creator_details)

    # Create a new record
    record = Record()

    # Create metadata and attach to record.
    metadata = Metadata(
        creators=creators,
        titles=[title],
        publisher=publisher,
        types=resource_type,
    )

    # Attach the record metadata to the record
    record.metadata = metadata

    # Allocate a DOI through DataCite and store it on the record metadata.
    allocated_identifier = allocate_doi(record, DOI_PREFIX, DATACITE_URL)
    print(f"Allocated DOI = {allocated_identifier.identifier_value}")

    # Generate a landing page for the record.
    generate_landing_page(record)
    print(f"Landing Page: {record.identifier}.html")


print('Done')
    