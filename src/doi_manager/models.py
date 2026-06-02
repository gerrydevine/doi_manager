import uuid
from datetime import datetime
from .vocabs import (
    AFFILIATION_IDENTIFIER_PREFIXES,
    AFFILIATION_IDENTIFIER_SCHEME_VALUES,
    AFFILIATION_SCHEME_URI_VALUES,
    CONTRIBUTOR_NAME_TYPE_VALUES,
    CONTRIBUTOR_TYPE_VALUES,
    CREATOR_NAME_TYPE_VALUES,
    DATE_TYPE_VALUES,
    DESCRIPTION_TYPE_VALUES,
    FUNDER_IDENTIFIER_TYPE_VALUES,
    IDENTIFIER_TYPE_ATTR_VALUES,
    NAME_IDENTIFIER_SCHEME_VALUES,
    NAME_IDENTIFIER_PREFIXES,
    NAME_IDENTIFIER_SCHEME_URI_VALUES,
    PUBLISHER_IDENTIFIER_PREFIXES,
    PUBLISHER_IDENTIFIER_SCHEME_VALUES,
    PUBLISHER_IDENTIFIER_SCHEME_URI_VALUES,
    RELATED_IDENTIFIER_TYPE_VALUES,
    RELATION_TYPE_VALUES,
    RESOURCE_TYPE_GENERAL_VALUES,
    TITLE_TYPE_VALUES,
    RIGHTS_IDENTIFIER_VALUES,
)


class Identifier:
    def __init__(self, *, identifier_value: str, identifier_type_attr: str):
        if identifier_type_attr not in IDENTIFIER_TYPE_ATTR_VALUES:
            values = ", ".join(IDENTIFIER_TYPE_ATTR_VALUES)
            raise ValueError(f"identifier_type_attr must be one of: {values}")

        self.identifier_value = identifier_value
        self.identifier_type_attr = identifier_type_attr


class AlternateIdentifier:
    def __init__(self, *, alternate_identifier_type: str, alternate_identifier: str):
        if not isinstance(alternate_identifier_type, str):
            raise TypeError("alternate_identifier_type must be a string")

        if not isinstance(alternate_identifier, str):
            raise TypeError("alternate_identifier must be a string")

        self.alternate_identifier_type = alternate_identifier_type
        self.alternate_identifier = alternate_identifier


class RelatedIdentifier:
    def __init__(
        self,
        *,
        related_identifier: str,
        related_identifier_type: str,
        relation_type: str,
        resource_type_general: str | None = None,
        relation_type_information: str | None = None,
    ):
        if not isinstance(related_identifier, str):
            raise TypeError("related_identifier must be a string")

        if not isinstance(related_identifier_type, str):
            raise TypeError("related_identifier_type must be a string")

        if related_identifier_type not in RELATED_IDENTIFIER_TYPE_VALUES:
            values = ", ".join(RELATED_IDENTIFIER_TYPE_VALUES)
            raise ValueError(f"related_identifier_type must be one of: {values}")

        if not isinstance(relation_type, str):
            raise TypeError("relation_type must be a string")

        if relation_type not in RELATION_TYPE_VALUES:
            values = ", ".join(RELATION_TYPE_VALUES)
            raise ValueError(f"relation_type must be one of: {values}")

        if resource_type_general is not None:
            if not isinstance(resource_type_general, str):
                raise TypeError("resource_type_general must be a string")

            if resource_type_general not in RESOURCE_TYPE_GENERAL_VALUES:
                values = ", ".join(RESOURCE_TYPE_GENERAL_VALUES)
                raise ValueError(f"resource_type_general must be one of: {values}")

        if relation_type_information is not None and not isinstance(
            relation_type_information,
            str,
        ):
            raise TypeError("relation_type_information must be a string")

        self.related_identifier = related_identifier
        self.related_identifier_type = related_identifier_type
        self.relation_type = relation_type
        self.resource_type_general = resource_type_general
        self.relation_type_information = relation_type_information


class Title:
    def __init__(self, *, title: str, lang: str = "en", type: str | None = None):
        if not isinstance(title, str):
            raise TypeError("title must be a string")

        if not isinstance(lang, str):
            raise TypeError("lang must be a string")

        if type is not None and type not in TITLE_TYPE_VALUES:
            values = ", ".join(TITLE_TYPE_VALUES)
            raise ValueError(f"type must be one of: {values}")

        self.title = title
        self.lang = lang
        self.type = type


class Types:
    def __init__(self, *, resource_type: str, resource_type_general: str):
        if not isinstance(resource_type, str):
            raise TypeError("resource_type must be a string")

        if not isinstance(resource_type_general, str):
            raise TypeError("resource_type_general must be a string")

        if resource_type_general not in RESOURCE_TYPE_GENERAL_VALUES:
            values = ", ".join(RESOURCE_TYPE_GENERAL_VALUES)
            raise ValueError(f"resource_type_general must be one of: {values}")

        self.resource_type = resource_type
        self.resource_type_general = resource_type_general


class Subject:
    def __init__(
        self,
        *,
        subject: str,
        lang: str | None = None,
        scheme_uri: str | None = None,
        value_uri: str | None = None,
        subject_scheme: str | None = None,
        classification_code: str | None = None,
    ):
        if not isinstance(subject, str):
            raise TypeError("subject must be a string")

        if lang is not None and not isinstance(lang, str):
            raise TypeError("lang must be a string")

        optional_strings = {
            "scheme_uri": scheme_uri,
            "value_uri": value_uri,
            "subject_scheme": subject_scheme,
            "classification_code": classification_code,
        }

        for field_name, field_value in optional_strings.items():
            if field_value is not None and not isinstance(field_value, str):
                raise TypeError(f"{field_name} must be a string")

        self.subject = subject
        self.lang = lang
        self.scheme_uri = scheme_uri
        self.value_uri = value_uri
        self.subject_scheme = subject_scheme
        self.classification_code = classification_code


class Date:
    def __init__(
        self,
        *,
        date: str,
        date_type: str,
        date_information: str | None = None,
    ):
        if not isinstance(date, str):
            raise TypeError("date must be a string")

        is_year = len(date) == 4 and date.isdigit()
        is_full_date = (
            len(date) == 10
            and date[4] == "-"
            and date[7] == "-"
            and date[:4].isdigit()
            and date[5:7].isdigit()
            and date[8:].isdigit()
        )

        if not is_year and not is_full_date:
            raise ValueError("date must be in YYYY or YYYY-MM-DD format")

        if date_type is None:
            raise ValueError("date_type is required when date is supplied")

        if not isinstance(date_type, str):
            raise TypeError("date_type must be a string")

        if date_type not in DATE_TYPE_VALUES:
            values = ", ".join(DATE_TYPE_VALUES)
            raise ValueError(f"date_type must be one of: {values}")

        if date_information is not None and not isinstance(date_information, str):
            raise TypeError("date_information must be a string")

        self.date = date
        self.date_type = date_type
        self.date_information = date_information


class Description:
    def __init__(
        self,
        *,
        description: str,
        description_type: str,
        lang: str = "en",
    ):
        if not isinstance(description, str):
            raise TypeError("description must be a string")

        if not isinstance(description_type, str):
            raise TypeError("description_type must be a string")

        if description_type not in DESCRIPTION_TYPE_VALUES:
            values = ", ".join(DESCRIPTION_TYPE_VALUES)
            raise ValueError(f"description_type must be one of: {values}")

        if not isinstance(lang, str):
            raise TypeError("lang must be a string")

        self.description = description
        self.description_type = description_type
        self.lang = lang


class GeoLocationPoint:
    def __init__(
        self,
        *,
        point_longitude: float,
        point_latitude: float,
    ):
        if not isinstance(point_longitude, float):
            raise TypeError("point_longitude must be a float")

        if point_longitude < -180.0 or point_longitude > 180.0:
            raise ValueError("point_longitude must be between -180.0 and 180.0")

        if not isinstance(point_latitude, float):
            raise TypeError("point_latitude must be a float")

        if point_latitude < -90.0 or point_latitude > 90.0:
            raise ValueError("point_latitude must be between -90.0 and 90.0")

        self.point_longitude = point_longitude
        self.point_latitude = point_latitude


class GeoLocationBox:
    def __init__(
        self,
        *,
        west_bound_longitude: float,
        east_bound_longitude: float,
        south_bound_latitude: float,
        north_bound_latitude: float,
    ):
        if not isinstance(west_bound_longitude, float):
            raise TypeError("west_bound_longitude must be a float")

        if west_bound_longitude < -180.0 or west_bound_longitude > 180.0:
            raise ValueError(
                "west_bound_longitude must be between -180.0 and 180.0"
            )

        if not isinstance(east_bound_longitude, float):
            raise TypeError("east_bound_longitude must be a float")

        if east_bound_longitude < -180.0 or east_bound_longitude > 180.0:
            raise ValueError(
                "east_bound_longitude must be between -180.0 and 180.0"
            )

        if not isinstance(south_bound_latitude, float):
            raise TypeError("south_bound_latitude must be a float")

        if south_bound_latitude < -90.0 or south_bound_latitude > 90.0:
            raise ValueError("south_bound_latitude must be between -90.0 and 90.0")

        if not isinstance(north_bound_latitude, float):
            raise TypeError("north_bound_latitude must be a float")

        if north_bound_latitude < -90.0 or north_bound_latitude > 90.0:
            raise ValueError("north_bound_latitude must be between -90.0 and 90.0")

        self.west_bound_longitude = west_bound_longitude
        self.east_bound_longitude = east_bound_longitude
        self.south_bound_latitude = south_bound_latitude
        self.north_bound_latitude = north_bound_latitude


class PolygonPoint:
    def __init__(
        self,
        *,
        point_longitude: float,
        point_latitude: float,
    ):
        if not isinstance(point_longitude, float):
            raise TypeError("point_longitude must be a float")

        if point_longitude < -180.0 or point_longitude > 180.0:
            raise ValueError("point_longitude must be between -180.0 and 180.0")

        if not isinstance(point_latitude, float):
            raise TypeError("point_latitude must be a float")

        if point_latitude < -90.0 or point_latitude > 90.0:
            raise ValueError("point_latitude must be between -90.0 and 90.0")

        self.point_longitude = point_longitude
        self.point_latitude = point_latitude


# class PolygonPoint_Instance:
#     def __init__(
#         self,
#         *,
#         polygon_point: PolygonPoint,
#     ):
#         if not isinstance(polygon_point, PolygonPoint):
#             raise TypeError("polygon_point must be an instance of PolygonPoint")

#         self.polygon_point = polygon_point


class GeoLocation:
    def __init__(
        self,
        *,
        geolocation_place: str | None = None,
        geolocation_point: GeoLocationPoint | None = None,
        geolocation_box: GeoLocationBox | None = None,
        geolocation_polygon: list[PolygonPoint] | None = None,
    ):
        if geolocation_place is not None and not isinstance(geolocation_place, str):
            raise TypeError("geolocation_place must be a string")

        if geolocation_point is not None and not isinstance(
            geolocation_point,
            GeoLocationPoint,
        ):
            raise TypeError("geolocation_points must be a GeoLocationPoint object")

        if geolocation_box is not None and not isinstance(
            geolocation_box,
            GeoLocationBox,
        ):
            raise TypeError("geolocation_box must be a GeoLocationBox object")

        if geolocation_polygon is not None:
            if len(geolocation_polygon) < 4:
                raise ValueError("geolocation_polygon must contain at least four polygon points")

            if not isinstance(geolocation_polygon, list):
                raise TypeError("geolocation_polygon must be a list")

        self.geolocation_place = geolocation_place
        self.geolocation_point = geolocation_point
        self.geolocation_box = geolocation_box
        self.geolocation_polygon = geolocation_polygon


class Rights:
    def __init__(
        self,
        *,
        rights: str,
        rights_uri: str | None = None,
        rights_identifier: str | None = None,
        rights_identifier_scheme: str | None = None,
        scheme_uri: str | None = None,
        lang: str | None = None,
    ):
        if rights_identifier not in RIGHTS_IDENTIFIER_VALUES:
            values = ", ".join(RIGHTS_IDENTIFIER_VALUES)
            raise ValueError(f"rights_identifier must be one of: {values}")

        self.rights = rights
        self.rights_uri = rights_uri
        self.rights_identifier = rights_identifier
        self.rights_identifier_scheme = rights_identifier_scheme
        self.scheme_uri = scheme_uri
        self.lang = lang


class FundingReference:
    def __init__(
        self,
        *,
        funder_name: str,
        funder_identifier: str | None = None,
        funder_identifier_type: str | None = None,
        award_title: str | None = None,
        award_number: str | None = None,
        award_uri: str | None = None,
    ):
        if not isinstance(funder_name, str):
            raise TypeError("funder_name must be a string")

        if funder_identifier is not None:
            if not isinstance(funder_identifier, str):
                raise TypeError("funder_identifier must be a string")

            if funder_identifier_type is None:
                raise ValueError(
                    "funder_identifier_type is required when "
                    "funder_identifier is supplied"
                )

        if funder_identifier_type is not None:
            if not isinstance(funder_identifier_type, str):
                raise TypeError("funder_identifier_type must be a string")

            if funder_identifier_type not in FUNDER_IDENTIFIER_TYPE_VALUES:
                values = ", ".join(FUNDER_IDENTIFIER_TYPE_VALUES)
                raise ValueError(f"funder_identifier_type must be one of: {values}")

        optional_strings = {
            "award_title": award_title,
            "award_number": award_number,
            "award_uri": award_uri,
        }

        for field_name, field_value in optional_strings.items():
            if field_value is not None and not isinstance(field_value, str):
                raise TypeError(f"{field_name} must be a string")

        self.funder_name = funder_name
        self.funder_identifier = funder_identifier
        self.funder_identifier_type = funder_identifier_type
        self.award_title = award_title
        self.award_number = award_number
        self.award_uri = award_uri


class Affiliation:
    def __init__(
        self,
        *,
        name: str,
        affiliation_identifier: str | None = None,
        affiliation_identifier_scheme: str | None = None,
        scheme_uri: str | None = None,
    ):
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if affiliation_identifier is not None:
            if not isinstance(affiliation_identifier, str):
                raise TypeError("affiliation_identifier must be a string")

            if not affiliation_identifier.startswith(
                tuple(AFFILIATION_IDENTIFIER_PREFIXES)
            ):
                values = ", ".join(AFFILIATION_IDENTIFIER_PREFIXES)
                raise ValueError(
                    f"affiliation_identifier must begin with one of: {values}"
                )

        if affiliation_identifier is not None:
            if affiliation_identifier_scheme is None:
                raise ValueError(
                    "affiliation_identifier_scheme is required when "
                    "affiliation_identifier is supplied"
                )

        if affiliation_identifier_scheme is not None:
            if not isinstance(affiliation_identifier_scheme, str):
                raise TypeError("affiliation_identifier_scheme must be a string")

            if affiliation_identifier_scheme not in AFFILIATION_IDENTIFIER_SCHEME_VALUES:
                values = ", ".join(AFFILIATION_IDENTIFIER_SCHEME_VALUES)
                raise ValueError(
                    f"affiliation_identifier_scheme must be one of: {values}"
                )

        if scheme_uri is not None:
            if not isinstance(scheme_uri, str):
                raise TypeError("scheme_uri must be a string")

            if scheme_uri not in AFFILIATION_SCHEME_URI_VALUES:
                values = ", ".join(AFFILIATION_SCHEME_URI_VALUES)
                raise ValueError(f"scheme_uri must be one of: {values}")

        self.affiliation_identifier = affiliation_identifier
        self.name = name
        self.affiliation_identifier_scheme = affiliation_identifier_scheme
        self.scheme_uri = scheme_uri



class NameIdentifier:
    def __init__(
        self,
        *,
        name_identifier: str,
        name_identifier_scheme: str,
        scheme_uri: str | None = None,
    ):
        if not isinstance(name_identifier, str):
            raise TypeError("name_identifier must be a string")

        if not isinstance(name_identifier_scheme, str):
            raise TypeError("name_identifier_scheme must be a string")

        if not name_identifier.startswith(tuple(NAME_IDENTIFIER_PREFIXES)):
            values = ", ".join(NAME_IDENTIFIER_PREFIXES)
            raise ValueError(f"name_identifier must begin with one of: {values}")

        if name_identifier_scheme not in NAME_IDENTIFIER_SCHEME_VALUES:
            values = ", ".join(NAME_IDENTIFIER_SCHEME_VALUES)
            raise ValueError(f"name_identifier_scheme must be one of: {values}")

        if scheme_uri is not None:
            if not isinstance(scheme_uri, str):
                raise TypeError("scheme_uri must be a string")

            if scheme_uri not in NAME_IDENTIFIER_SCHEME_URI_VALUES:
                values = ", ".join(NAME_IDENTIFIER_SCHEME_URI_VALUES)
                raise ValueError(f"scheme_uri must be one of: {values}")

        self.name_identifier = name_identifier
        self.name_identifier_scheme = name_identifier_scheme
        self.scheme_uri = scheme_uri


class Creator:
    def __init__(
        self,
        *,
        creator_name: str,
        name_type: str,
        lang: str | None = None,
        given_name: str | None = None,
        family_name: str | None = None,
        name_identifiers: list[NameIdentifier] | None = None,
        affiliations: list[Affiliation] | None = None,
    ):
        if not isinstance(creator_name, str):
            raise TypeError("creator_name must be a string")

        if name_type not in CREATOR_NAME_TYPE_VALUES:
            values = ", ".join(CREATOR_NAME_TYPE_VALUES)
            raise ValueError(f"name_type must be one of: {values}")

        if name_identifiers is None:
            name_identifiers = []

        if not isinstance(name_identifiers, list):
            raise TypeError("name_identifiers must be a list")

        for name_identifier in name_identifiers:
            if not isinstance(name_identifier, NameIdentifier):
                raise TypeError(
                    "name_identifiers must contain only NameIdentifier objects"
                )

        if affiliations is None:
            affiliations = []

        if not isinstance(affiliations, list):
            raise TypeError("affiliations must be a list")

        for item_affiliation in affiliations:
            if not isinstance(item_affiliation, Affiliation):
                raise TypeError("affiliations must contain only affiliation objects")

        self.creator_name = creator_name
        self.name_type = name_type
        self.given_name = given_name
        self.family_name = family_name
        self.lang = lang
        self.name_identifiers = name_identifiers
        self.affiliations = affiliations


class Contributor:
    def __init__(
        self,
        *,
        contributor_name: str,
        name_type: str,
        contributor_type: str,
        name_identifiers: list[NameIdentifier] | None = None,
        affiliations: list[Affiliation] | None = None,
    ):
        if not isinstance(contributor_name, str):
            raise TypeError("contributor_name must be a string")

        if name_type not in CONTRIBUTOR_NAME_TYPE_VALUES:
            values = ", ".join(CONTRIBUTOR_NAME_TYPE_VALUES)
            raise ValueError(f"name_type must be one of: {values}")

        if not isinstance(contributor_type, str):
            raise TypeError("contributor_type must be a string")

        if contributor_type not in CONTRIBUTOR_TYPE_VALUES:
            values = ", ".join(CONTRIBUTOR_TYPE_VALUES)
            raise ValueError(f"contributor_type must be one of: {values}")

        if name_identifiers is None:
            name_identifiers = []

        if not isinstance(name_identifiers, list):
            raise TypeError("name_identifiers must be a list")

        for name_identifier in name_identifiers:
            if not isinstance(name_identifier, NameIdentifier):
                raise TypeError(
                    "name_identifiers must contain only NameIdentifier objects"
                )

        if affiliations is None:
            affiliations = []

        if not isinstance(affiliations, list):
            raise TypeError("affiliations must be a list")

        for item_affiliation in affiliations:
            if not isinstance(item_affiliation, Affiliation):
                raise TypeError("affiliations must contain only affiliation objects")

        self.contributor_name = contributor_name
        self.name_type = name_type
        self.contributor_type = contributor_type
        self.name_identifiers = list(name_identifiers)
        self.affiliations = list(affiliations)


class Publisher:
    def __init__(
        self,
        *,
        name: str,
        publisher_identifier: str | None = None,
        publisher_identifier_scheme: str | None = None,
        scheme_uri: str | None = None,
        lang: str | None = None,
    ):
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if publisher_identifier is not None:
            if not isinstance(publisher_identifier, str):
                raise TypeError("publisher_identifier must be a string")

            if not publisher_identifier.startswith(
                tuple(PUBLISHER_IDENTIFIER_PREFIXES)
            ):
                values = ", ".join(PUBLISHER_IDENTIFIER_PREFIXES)
                raise ValueError(
                    f"publisher_identifier must begin with one of: {values}"
                )

            if publisher_identifier_scheme is None:
                raise ValueError(
                    "publisher_identifier_scheme is required when "
                    "publisher_identifier is supplied"
                )

        if (
            publisher_identifier_scheme is not None
            and publisher_identifier_scheme not in PUBLISHER_IDENTIFIER_SCHEME_VALUES
        ):
            values = ", ".join(PUBLISHER_IDENTIFIER_SCHEME_VALUES)
            raise ValueError(
                f"publisher_identifier_scheme must be one of: {values}"
            )

        if scheme_uri is not None:
            if not isinstance(scheme_uri, str):
                raise TypeError("scheme_uri must be a string")

            if scheme_uri not in PUBLISHER_IDENTIFIER_SCHEME_URI_VALUES:
                values = ", ".join(PUBLISHER_IDENTIFIER_SCHEME_URI_VALUES)
                raise ValueError(f"scheme_uri must be one of: {values}")

        if lang is not None and not isinstance(lang, str):
            raise TypeError("lang must be a string")

        self.name = name
        self.publisher_identifier = publisher_identifier
        self.publisher_identifier_scheme = publisher_identifier_scheme
        self.scheme_uri = scheme_uri
        self.lang = lang


class Metadata:
    def __init__(
        self,
        *,
        creators: list[Creator],
        titles: list[Title],
        publisher: Publisher,
        types: Types,
        publication_year: str | None = None,
        identifier: Identifier | None = None,
        language: str | None = None,
        subjects: list[Subject] | None = None,
        contributors: list[Contributor] | None = None,
        dates: list[Date] | None = None,
        alternate_identifiers: list[AlternateIdentifier] | None = None,
        related_identifiers: list[RelatedIdentifier] | None = None,
        sizes: list[str] | None = None,
        formats: list[str] | None = None,
        version: str | None = None,
        descriptions: list[Description] | None = None,
        geolocations: list[GeoLocation] | None = None,
        funding_references: list[FundingReference] | None = None,
        rights_list: list[Rights] | None = None,
    ):
        if publication_year is None:
            publication_year = str(datetime.now().year)

        if not isinstance(publication_year, str):
            raise TypeError("publication_year must be a string")

        if len(publication_year) != 4 or not publication_year.isdigit():
            raise ValueError("publication_year must be a four digit year")

        if language is not None and not isinstance(language, str):
            raise TypeError("language must be a string")

        if identifier is not None and not isinstance(identifier, Identifier):
            raise TypeError("identifier must be an Identifier object")

        if not creators:
            raise ValueError("metadata must have at least one creator")

        if not titles:
            raise ValueError("metadata must have at least one title")

        if not isinstance(publisher, Publisher):
            raise TypeError("publisher must be a Publisher object")

        if not isinstance(types, Types):
            raise TypeError("types must be a Types object")

        if subjects is None:
            subjects = []

        if not isinstance(subjects, list):
            raise TypeError("subjects must be a list")

        for item_subject in subjects:
            if not isinstance(item_subject, Subject):
                raise TypeError("subjects must contain only Subject objects")

        if contributors is None:
            contributors = []

        if not isinstance(contributors, list):
            raise TypeError("contributors must be a list")

        for item_contributor in contributors:
            if not isinstance(item_contributor, Contributor):
                raise TypeError("contributors must contain only Contributor objects")

        if dates is None:
            dates = []

        if not isinstance(dates, list):
            raise TypeError("dates must be a list")

        for item_date in dates:
            if not isinstance(item_date, Date):
                raise TypeError("dates must contain only Date objects")

        if alternate_identifiers is None:
            alternate_identifiers = []

        if not isinstance(alternate_identifiers, list):
            raise TypeError("alternate_identifiers must be a list")

        for alternate_identifier in alternate_identifiers:
            if not isinstance(alternate_identifier, AlternateIdentifier):
                raise TypeError(
                    "alternate_identifiers must contain only "
                    "AlternateIdentifier objects"
                )

        if related_identifiers is None:
            related_identifiers = []

        if not isinstance(related_identifiers, list):
            raise TypeError("related_identifiers must be a list")

        for related_identifier in related_identifiers:
            if not isinstance(related_identifier, RelatedIdentifier):
                raise TypeError(
                    "related_identifiers must contain only "
                    "RelatedIdentifier objects"
                )

        if sizes:
            if not isinstance(sizes, list):
                raise TypeError("sizes must be a list")

            if len(sizes):
                for item_size in sizes:
                    if not isinstance(item_size, str):
                        raise TypeError("sizes must contain only strings")
        else:
            sizes = []

        if formats:
            if not isinstance(formats, list):
                raise TypeError("formats must be a list")

            if len(formats):
                for item_format in formats:
                    if not isinstance(item_format, str):
                        raise TypeError("formats must contain only strings")
        else:
            formats = []

        if version:
            if not isinstance(version, str):
                raise TypeError("version must be a string")

        if descriptions is None:
            descriptions = []

        if not isinstance(descriptions, list):
            raise TypeError("descriptions must be a list")

        for item_description in descriptions:
            if not isinstance(item_description, Description):
                raise TypeError("descriptions must contain only Description objects")

        if geolocations is None:
            geolocations = []

        if not isinstance(geolocations, list):
            raise TypeError("geolocations must be a list")

        for item_geolocation in geolocations:
            if not isinstance(item_geolocation, GeoLocation):
                raise TypeError("geolocations must contain only GeoLocation objects")

        if funding_references is None:
            funding_references = []

        if not isinstance(funding_references, list):
            raise TypeError("funding_references must be a list")

        for item_funding_reference in funding_references:
            if not isinstance(item_funding_reference, FundingReference):
                raise TypeError(
                    "funding_references must contain only FundingReference objects"
                )

        # allow callers to omit rights_list (default None)
        if rights_list is None:
            rights_list = []

        if not isinstance(rights_list, list):
            raise TypeError("rights_list must be a list")

        for item_rights in rights_list:
            if not isinstance(item_rights, Rights):
                raise TypeError("rights_list must contain only Rights objects")

        self.identifier = identifier
        self.creators = creators
        self.titles = titles
        self.publisher = publisher
        self.publication_year = publication_year
        self.types = types
        self.language = language
        self.subjects = list(subjects)
        self.contributors = list(contributors)
        self.dates = list(dates)
        self.alternate_identifiers = list(alternate_identifiers)
        self.related_identifiers = list(related_identifiers)
        self.sizes = sizes
        self.formats = formats  
        self.version = version
        self.descriptions = list(descriptions)
        self.geolocations = list(geolocations)
        self.funding_references = list(funding_references)
        self.rights_list = list(rights_list)


class Record:
    def __init__(self, *, metadata: Metadata | None = None):
        object.__setattr__(self, "_identifier", str(uuid.uuid4()))
        self.metadata = metadata

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def metadata(self) -> Metadata | None:
        return self._metadata

    @metadata.setter
    def metadata(self, value: Metadata | None):
        if value is not None and not isinstance(value, Metadata):
            raise TypeError("metadata must be a Metadata object")

        object.__setattr__(self, "_metadata", value)

    def __setattr__(self, name, value):
        if name in {"identifier", "_identifier"}:
            raise AttributeError("identifier is read-only")

        super().__setattr__(name, value)
