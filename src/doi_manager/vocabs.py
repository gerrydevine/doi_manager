# Allowed values for the identifier type attribute.
IDENTIFIER_TYPE_ATTR_VALUES = ["doi"]

# Allowed values for the creator name type.
CREATOR_NAME_TYPE_VALUES = ["Personal", "Organizational"]

# Allowed values for the contributor name type.
CONTRIBUTOR_NAME_TYPE_VALUES = ["Personal", "Organizational"]

# Allowed values for the contributor type.
CONTRIBUTOR_TYPE_VALUES = [
    "ContactPerson",
    "DataCollector",
    "DataCurator",
    "DataManager",
    "Distributor",
    "Editor",
    "HostingInstitution",
    "Producer",
    "ProjectLeader",
    "ProjectManager",
    "ProjectMember",
    "RegistrationAgency",
    "RegistrationAuthority",
    "RelatedPerson",
    "Researcher",
    "ResearchGroup",
    "RightsHolder",
    "Sponsor",
    "Supervisor",
    "Translator",
    "WorkPackageLeader",
    "Other",
]

# Allowed values for the date type.
DATE_TYPE_VALUES = [
    "Accepted",
    "Available",
    "Copyrighted",
    "Collected",
    "Coverage",
    "Created",
    "Issued",
    "Submitted",
    "Updated",
    "Valid",
    "Withdrawn",
    "Other",
]

# Allowed values for the general resource type.
RESOURCE_TYPE_GENERAL_VALUES = [
    "Audiovisual",
    "Award",
    "Book",
    "BookChapter",
    "Collection",
    "ComputationalNotebook",
    "ConferencePaper",
    "ConferenceProceeding",
    "DataPaper",
    "Dataset",
    "Dissertation",
    "Event",
    "Image",
    "InteractiveResource",
    "Instrument",
    "Journal",
    "JournalArticle",
    "Model",
    "OutputManagementPlan",
    "PeerReview",
    "PhysicalObject",
    "Poster",
    "Preprint",
    "Presentation",
    "Project",
    "Report",
    "Service",
    "Software",
    "Sound",
    "Standard",
    "StudyRegistration",
    "Text",
    "Workflow",
    "Other",
]

# Allowed values for the related identifier type.
RELATED_IDENTIFIER_TYPE_VALUES = [
    "ARK",
    "arXiv",
    "bibcode",
    "CSTR",
    "DOI",
    "EAN13",
    "EISSN",
    "Handle",
    "IGSN",
    "ISBN",
    "ISSN",
    "ISTC",
    "LISSN",
    "LSID",
    "PMID",
    "PURL",
    "RAiD",
    "RRID",
    "SWHID",
    "UPC",
    "URL",
    "URN",
    "w3id",
]

# Allowed values for the relation type.
RELATION_TYPE_VALUES = [
    "IsCitedBy",
    "Cites",
    "IsSupplementTo",
    "IsSupplementedBy",
    "IsContinuedBy",
    "Continues",
    "IsDescribedBy",
    "Describes",
    "HasMetadata",
    "IsMetadataFor",
    "HasVersion",
    "IsVersionOf",
    "IsNewVersionOf",
    "IsPreviousVersionOf",
    "IsPartOf",
    "HasPart",
    "IsPublishedIn",
    "IsReferencedBy",
    "References",
    "IsDocumentedBy",
    "Documents",
    "IsCompiledBy",
    "Compiles",
    "IsVariantFormOf",
    "IsOriginalFormOf",
    "IsIdenticalTo",
    "IsReviewedBy",
    "Reviews",
    "IsDerivedFrom",
    "IsSourceOf",
    "IsRequiredBy",
    "Requires",
    "IsObsoletedBy",
    "Obsoletes",
    "IsCollectedBy",
    "Collects",
    "IsTranslationOf",
    "HasTranslation",
    "Other",
]

# Allowed URL prefixes for creator name identifiers.
CREATOR_NAME_IDENTIFIER_PREFIXES = [
    "https://orcid.org/",
    "https://ror.org/",
    "https://isni.org/"
]

# Allowed URL prefixes for affiliation identifiers.
AFFILIATION_IDENTIFIER_PREFIXES = [
    "https://ror.org/",
    "https://isni.org/"
]

# Allowed values for affiliation identifier schemes.
AFFILIATION_IDENTIFIER_SCHEME_VALUES = [
    "ROR",
    "ISNI"
]

# Allowed values for affiliation identifier schemes.
AFFILIATION_SCHEME_URI_VALUES = [
    "https://ror.org/",
    "https://isni.org/"
]

# Allowed URL prefixes for publisher identifiers.
PUBLISHER_IDENTIFIER_PREFIXES = ["https://ror.org/"]

# Allowed values for title type.
TITLE_TYPE_VALUES = ["AlternativeTitle", "Subtitle", "TranslatedTitle", "Other"]

# Allowed values for the description type.
DESCRIPTION_TYPE_VALUES = [
    "Abstract",
    "Methods",
    "SeriesInformation",
    "TableOfContents",
    "TechnicalInfo",
    "Other",
]

# Allowed values for the funder identifier type.
FUNDER_IDENTIFIER_TYPE_VALUES = [
    "Crossref Funder ID",
    "GRID",
    "ISNI",
    "ROR",
    "Other",
]

# Allowed values for the Rights Identifier.
RIGHTS_IDENTIFIER_VALUES = [
    "CC0",
    "CC BY 4.0",
    "CC BY-SA 4.0",
    "CC BY-ND 4.0",
    "CC BY-NC 4.0",
    "CC BY-NC-SA 4.0",
    "CC BY-NC-ND 4.0",
]

NAME_IDENTIFIER_PREFIXES = [
    "https://orcid.org",
    "https://isni.org",
    "https://ror.org",
]

NAME_IDENTIFIER_SCHEME_VALUES = [
    "ORCID",
    "ISNI",
    "ROR"
]

NAME_IDENTIFIER_SCHEME_URI_VALUES = [
    "https://orcid.org",
    "https://isni.org",
    "https://ror.org",
]