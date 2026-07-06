from .models import Record


def generate_datacite_payload(record: Record, doi_prefix: str) -> dict:
    if not isinstance(record, Record):
        raise TypeError("record must be a Record object")

    if record.metadata is None:
        raise ValueError("record must have metadata before creating a DataCite payload")

    if not doi_prefix:
        raise ValueError("doi_prefix is required")

    metadata = record.metadata
    attrs = _compact(
        {
            "prefix": doi_prefix,
            "creators": [_creator_to_payload(creator) for creator in metadata.creators],
            "titles": [_title_to_payload(title) for title in metadata.titles],
            "publisher": _publisher_to_payload(metadata.publisher),
            "publicationYear": int(metadata.publication_year),
            "types": {
                "resourceType": metadata.types.resource_type,
                "resourceTypeGeneral": metadata.types.resource_type_general,
            },
            "language": metadata.language,
        }
    )

    if metadata.identifier is not None and metadata.identifier.identifier_value:
        attrs["doi"] = metadata.identifier.identifier_value

    optional_fields = {
        "subjects": [_subject_to_payload(subject) for subject in metadata.subjects],
        "contributors": [
            _contributor_to_payload(contributor)
            for contributor in metadata.contributors
        ],
        "dates": [_date_to_payload(date) for date in metadata.dates],
        "alternateIdentifiers": [
            _alternate_identifier_to_payload(alternate_identifier)
            for alternate_identifier in metadata.alternate_identifiers
        ],
        "relatedIdentifiers": [
            _related_identifier_to_payload(related_identifier)
            for related_identifier in metadata.related_identifiers
        ],
        "sizes": metadata.sizes,
        "formats": metadata.formats,
        "version": metadata.version,
        "url": metadata.url,
        "descriptions": [
            _description_to_payload(description)
            for description in metadata.descriptions
        ],
        "geoLocations": [
            _geolocation_to_payload(geolocation)
            for geolocation in metadata.geolocations
        ],
        "fundingReferences": [
            _funding_reference_to_payload(funding_reference)
            for funding_reference in metadata.funding_references
        ],
        "rightsList": [
            _rights_to_payload(rights)
            for rights in metadata.rights_list
        ],
    }

    attrs.update(_compact(optional_fields))

    return {
        "data": {
            "type": "dois",
            "attributes": attrs,
        }
    }


def _compact(values: dict) -> dict:
    return {
        key: value
        for key, value in values.items()
        if value is not None and value != []
    }


def _creator_to_payload(creator) -> dict:
    return _compact(
        {
            "name": creator.creator_name,
            "nameType": creator.name_type,
            "nameIdentifiers": [
                _name_identifier_to_payload(name_identifier)
                for name_identifier in creator.name_identifiers
            ],
            "affiliation": [
                _affiliation_to_payload(affiliation)
                for affiliation in creator.affiliations
            ],
        }
    )


def _contributor_to_payload(contributor) -> dict:
    return _compact(
        {
            "name": contributor.contributor_name,
            "nameType": contributor.name_type,
            "contributorType": contributor.contributor_type,
            "nameIdentifiers": [
                _name_identifier_to_payload(name_identifier)
                for name_identifier in contributor.name_identifiers
            ],
            "affiliation": [
                _affiliation_to_payload(affiliation)
                for affiliation in contributor.affiliations
            ],
        }
    )


def _name_identifier_to_payload(name_identifier) -> dict:
    return _compact(
        {
            "nameIdentifier": name_identifier.name_identifier,
            "nameIdentifierScheme": name_identifier.name_identifier_scheme,
            "schemeUri": name_identifier.scheme_uri,
        }
    )


def _affiliation_to_payload(affiliation) -> dict:
    return _compact(
        {
            "name": affiliation.name,
            "affiliationIdentifier": affiliation.affiliation_identifier,
            "affiliationIdentifierScheme": affiliation.affiliation_identifier_scheme,
            "schemeUri": affiliation.scheme_uri,
        }
    )


def _title_to_payload(title) -> dict:
    return _compact(
        {
            "title": title.title,
            "lang": title.lang,
            "titleType": title.type,
        }
    )


def _publisher_to_payload(publisher) -> dict:
    return _compact(
        {
            "name": publisher.name,
            "publisherIdentifier": publisher.publisher_identifier,
            "publisherIdentifierScheme": publisher.publisher_identifier_scheme,
            "schemeUri": publisher.scheme_uri,
            "lang": publisher.lang,
        }
    )


def _subject_to_payload(subject) -> dict:
    return _compact(
        {
            "subject": subject.subject,
            "lang": subject.lang,
            "schemeUri": subject.scheme_uri,
            "valueUri": subject.value_uri,
            "subjectScheme": subject.subject_scheme,
            "classificationCode": subject.classification_code,
        }
    )


def _date_to_payload(date) -> dict:
    return _compact(
        {
            "date": date.date,
            "dateType": date.date_type,
            "dateInformation": date.date_information,
        }
    )


def _alternate_identifier_to_payload(alternate_identifier) -> dict:
    return {
        "alternateIdentifier": alternate_identifier.alternate_identifier,
        "alternateIdentifierType": alternate_identifier.alternate_identifier_type,
    }


def _related_identifier_to_payload(related_identifier) -> dict:
    return _compact(
        {
            "relatedIdentifier": related_identifier.related_identifier,
            "relatedIdentifierType": related_identifier.related_identifier_type,
            "relationType": related_identifier.relation_type,
            "resourceTypeGeneral": related_identifier.resource_type_general,
            "relationTypeInformation": (
                related_identifier.relation_type_information
            ),
        }
    )


def _description_to_payload(description) -> dict:
    return {
        "description": description.description,
        "descriptionType": description.description_type,
        "lang": description.lang,
    }


def _geolocation_to_payload(geolocation) -> dict:
    return _compact(
        {
            "geoLocationPlace": geolocation.geolocation_place,
            "geoLocationPoint": _geolocation_point_to_payload(
                geolocation.geolocation_point
            ),
            "geoLocationBox": _geolocation_box_to_payload(geolocation.geolocation_box),
            "geoLocationPolygon": _geolocation_polygon_to_payload(
                geolocation.geolocation_polygon
            ),
        }
    )


def _geolocation_point_to_payload(point) -> dict | None:
    if point is None:
        return None

    return {
        "pointLongitude": point.point_longitude,
        "pointLatitude": point.point_latitude,
    }


def _geolocation_box_to_payload(box) -> dict | None:
    if box is None:
        return None

    return {
        "westBoundLongitude": box.west_bound_longitude,
        "eastBoundLongitude": box.east_bound_longitude,
        "southBoundLatitude": box.south_bound_latitude,
        "northBoundLatitude": box.north_bound_latitude,
    }


def _geolocation_polygon_to_payload(polygon) -> list[dict] | None:
    if polygon is None:
        return None

    return [
        {"polygonPoint": _polygon_point_to_payload(point)}
        for point in polygon
    ]


def _polygon_point_to_payload(point) -> dict:
    if isinstance(point, dict):
        return {
            "pointLongitude": point["point_longitude"],
            "pointLatitude": point["point_latitude"],
        }

    return {
        "pointLongitude": point.point_longitude,
        "pointLatitude": point.point_latitude,
    }


def _funding_reference_to_payload(funding_reference) -> dict:
    return _compact(
        {
            "funderName": funding_reference.funder_name,
            "funderIdentifier": funding_reference.funder_identifier,
            "funderIdentifierType": funding_reference.funder_identifier_type,
            "awardTitle": funding_reference.award_title,
            "awardNumber": funding_reference.award_number,
            "awardUri": funding_reference.award_uri,
        }
    )


def _rights_to_payload(rights) -> dict:
    return {
        "rights": rights.rights,
        "rightsUri": rights.rights_uri,
        "schemeUri": rights.scheme_uri,
        "rightsIdentifier": rights.rights_identifier,
        "rightsIdentifierScheme": rights.rights_identifier_scheme,
        "lang": rights.lang,
    }
