import datetime
import os
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv
# import pkg_resources
# from github import Github
# import pandas as pd
# from ..config import GIT_BRANCH, GITHUB_REPO

load_dotenv()


DOI_LOGO = '''
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 130 130">
        <circle style="fill:#fcb425" cx="65" cy="65" r="64"/>
        <path style="fill:#231f20" d="m 49.819127,84.559148 -11.854304,0 0,-4.825665 c -1.203594,1.510894 -4.035515,3.051053 -5.264716,3.742483 -2.151101,1.203585 -5.072066,1.987225 -7.812161,1.987225 -4.430246,0 -8.373925,-1.399539 -11.831057,-4.446924 -4.1229464,-3.636389 -6.0602455,-9.19576 -6.0602455,-15.188113 0,-6.094791 2.1126913,-10.960381 6.3380645,-14.59676 3.354695,-2.893745 7.457089,-5.209795 11.810505,-5.209795 2.535231,0 5.661807,0.227363 7.889738,1.302913 1.280414,0.614601 3.572628,2.060721 4.929872,3.469179 l 0,-25.420177 11.854304,0 z m -12.1199,-18.692584 c 0,-2.253538 -0.618258,-4.951555 -2.205973,-6.513663 -1.587724,-1.587724 -4.474153,-2.996182 -6.727691,-2.996182 -2.509615,0 -4.834476,1.825511 -6.447807,3.720535 -1.306031,1.536501 -1.959041,3.905269 -1.959041,5.877114 0,1.971835 0.740815,4.165004 2.046836,5.701505 1.587714,1.895025 3.297985,3.193739 5.833216,3.193739 2.279145,0 4.989965,-0.956662 6.552083,-2.51877 1.587714,-1.562108 2.908377,-4.185134 2.908377,-6.464278 z"/>
        <path style="fill:#fff" d="m 105.42764,25.617918 c -1.97184,0 -3.64919,0.69142 -5.03204,2.074271 -1.357247,1.357245 -2.035864,3.021779 -2.035864,4.993633 0,1.971835 0.678617,3.649193 2.035864,5.032034 1.38285,1.382861 3.0602,2.074281 5.03204,2.074281 1.99744,0 3.67479,-0.678627 5.03203,-2.035861 1.38285,-1.382861 2.07428,-3.073012 2.07428,-5.070454 0,-1.971854 -0.69143,-3.636388 -2.07428,-4.993633 -1.38285,-1.382851 -3.0602,-2.074271 -5.03203,-2.074271 z M 74.219383,45.507921 c -7.323992,0 -12.970625,2.283009 -16.939921,6.848949 -3.277876,3.782438 -4.916803,8.118252 -4.916803,13.008406 0,5.430481 1.626124,10.009834 4.878383,13.738236 3.943689,4.538918 9.475093,6.808622 16.59421,6.808622 7.093512,0 12.612122,-2.269704 16.555801,-6.808622 3.252259,-3.728402 4.878393,-8.1993 4.878393,-13.413648 0,-5.160323 -1.638938,-9.604602 -4.916803,-13.332994 -4.020509,-4.56594 -9.398263,-6.848949 -16.13326,-6.848949 z m 24.908603,1.386686 0,37.634676 12.599304,0 0,-37.634676 -12.599304,0 z M 73.835252,56.975981 c 2.304752,0 4.263793,0.852337 5.877124,2.554426 1.638928,1.675076 2.458402,3.727881 2.458402,6.159457 0,2.458578 -0.806671,4.538022 -2.419992,6.240111 -1.613331,1.675086 -3.585175,2.514099 -5.915534,2.514099 -2.612051,0 -4.737546,-1.027366 -6.376474,-3.080682 -1.331637,-1.648053 -1.997451,-3.539154 -1.997451,-5.673528 0,-2.107362 0.665814,-3.985138 1.997451,-5.633201 1.638928,-2.053316 3.764423,-3.080682 6.376474,-3.080682 z"/>
    </svg>
'''
ORCID_LOGO = '''
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Layer_1" x="0px" y="0px" viewBox="0 0 256 256" style="enable-background:new 0 0 256 256;" width="20" height="20">
        <style type="text/css">
            .st0{fill:#A6CE39;}
            .st1{fill:#FFFFFF;}
        </style>
        <path class="st0" d="M256,128c0,70.7-57.3,128-128,128C57.3,256,0,198.7,0,128C0,57.3,57.3,0,128,0C198.7,0,256,57.3,256,128z"/>
        <g>
            <path class="st1" d="M86.3,186.2H70.9V79.1h15.4v48.4V186.2z"/>
            <path class="st1" d="M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5   c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z"/>
            <path class="st1" d="M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1   C84.2,46.7,88.7,51.3,88.7,56.8z"/>
        </g>
    </svg>
'''
ROR_LOGO = '''
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:serif="http://www.serif.com/" width="4%" height="4%" viewBox="0 0 164 118" version="1.1" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
        <g transform="matrix(0.994301,0,0,0.989352,0,0)">
            <rect x="0" y="0" width="82.47" height="59.8" style="fill:white;"/>
        </g>
        <g transform="matrix(1,0,0,1,-0.945,-0.815)">
            <path d="M68.65,4.16L56.52,22.74L44.38,4.16L68.65,4.16Z" style="fill:rgb(83,186,161);fill-rule:nonzero;"/>
            <path d="M119.41,4.16L107.28,22.74L95.14,4.16L119.41,4.16Z" style="fill:rgb(83,186,161);fill-rule:nonzero;"/>
            <path d="M44.38,115.47L56.52,96.88L68.65,115.47L44.38,115.47Z" style="fill:rgb(83,186,161);fill-rule:nonzero;"/>
            <path d="M95.14,115.47L107.28,96.88L119.41,115.47L95.14,115.47Z" style="fill:rgb(83,186,161);fill-rule:nonzero;"/>
            <path d="M145.53,63.71C149.83,62.91 153.1,61 155.33,57.99C157.57,54.98 158.68,51.32 158.68,47.03C158.68,43.47 158.06,40.51 156.83,38.13C155.6,35.75 153.93,33.86 151.84,32.45C149.75,31.05 147.31,30.04 144.53,29.44C141.75,28.84 138.81,28.54 135.72,28.54L112.16,28.54L112.16,47.37C111.97,46.82 111.77,46.28 111.55,45.74C109.92,41.79 107.64,38.42 104.71,35.64C101.78,32.86 98.32,30.72 94.3,29.23C90.29,27.74 85.9,26.99 81.14,26.99C76.38,26.99 72,27.74 67.98,29.23C63.97,30.72 60.5,32.86 57.57,35.64C54.95,38.13 52.85,41.1 51.27,44.54C51.04,42.07 50.46,39.93 49.53,38.13C48.3,35.75 46.63,33.86 44.54,32.45C42.45,31.05 40.01,30.04 37.23,29.44C34.45,28.84 31.51,28.54 28.42,28.54L4.87,28.54L4.87,89.42L18.28,89.42L18.28,65.08L24.9,65.08L37.63,89.42L53.71,89.42L38.24,63.71C42.54,62.91 45.81,61 48.04,57.99C48.14,57.85 48.23,57.7 48.33,57.56C48.31,58.03 48.3,58.5 48.3,58.98C48.3,63.85 49.12,68.27 50.75,72.22C52.38,76.17 54.66,79.54 57.59,82.32C60.51,85.1 63.98,87.24 68,88.73C72.01,90.22 76.4,90.97 81.16,90.97C85.92,90.97 90.3,90.22 94.32,88.73C98.33,87.24 101.8,85.1 104.73,82.32C107.65,79.54 109.93,76.17 111.57,72.22C111.79,71.69 111.99,71.14 112.18,70.59L112.18,89.42L125.59,89.42L125.59,65.08L132.21,65.08L144.94,89.42L161.02,89.42L145.53,63.71ZM36.39,50.81C35.67,51.73 34.77,52.4 33.68,52.83C32.59,53.26 31.37,53.52 30.03,53.6C28.68,53.69 27.41,53.73 26.2,53.73L18.29,53.73L18.29,39.89L27.06,39.89C28.26,39.89 29.5,39.98 30.76,40.15C32.02,40.32 33.14,40.65 34.11,41.14C35.08,41.63 35.89,42.33 36.52,43.25C37.15,44.17 37.47,45.4 37.47,46.95C37.47,48.6 37.11,49.89 36.39,50.81ZM98.74,66.85C97.85,69.23 96.58,71.29 94.91,73.04C93.25,74.79 91.26,76.15 88.93,77.13C86.61,78.11 84.01,78.59 81.15,78.59C78.28,78.59 75.69,78.1 73.37,77.13C71.05,76.16 69.06,74.79 67.39,73.04C65.73,71.29 64.45,69.23 63.56,66.85C62.67,64.47 62.23,61.85 62.23,58.98C62.23,56.17 62.67,53.56 63.56,51.15C64.45,48.74 65.72,46.67 67.39,44.92C69.05,43.17 71.04,41.81 73.37,40.83C75.69,39.86 78.28,39.37 81.15,39.37C84.02,39.37 86.61,39.86 88.93,40.83C91.25,41.8 93.24,43.17 94.91,44.92C96.57,46.67 97.85,48.75 98.74,51.15C99.63,53.56 100.07,56.17 100.07,58.98C100.07,61.85 99.63,64.47 98.74,66.85ZM143.68,50.81C142.96,51.73 142.06,52.4 140.97,52.83C139.88,53.26 138.66,53.52 137.32,53.6C135.97,53.69 134.7,53.73 133.49,53.73L125.58,53.73L125.58,39.89L134.35,39.89C135.55,39.89 136.79,39.98 138.05,40.15C139.31,40.32 140.43,40.65 141.4,41.14C142.37,41.63 143.18,42.33 143.81,43.25C144.44,44.17 144.76,45.4 144.76,46.95C144.76,48.6 144.4,49.89 143.68,50.81Z" style="fill:rgb(32,40,38);fill-rule:nonzero;"/>
        </g>
    </svg>
'''



def push_to_github(name, filename, git_branch, github_repo, delete_local=True):
    ''' Push webpage to github pages '''

    token = os.environ.get('GITHUB_ACCESS_TOKEN')
    g = Github(token)
    repo = g.get_user().get_repo(github_repo)

    all_files = []
    contents = repo.get_contents("")

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    with open(filename, 'r') as file:
        content = file.read()

    # Upload or replace on github
    if f"docs/instruments/{filename}" in all_files:
        repo_contents = repo.get_contents(f"docs/instruments/{filename}")
        repo.update_file(repo_contents.path, "committing files", content, repo_contents.sha, branch=git_branch)
    else:
        repo.create_file(f"docs/instruments/{filename}", "committing files", content, branch=git_branch)
        
        # Update main index 
        index_contents = repo.get_contents("docs/index.html")
        added_link = f'''
            <p><a href="instruments/{filename.split('.')[0]}">{name}</a></p>
        '''
        html_split = index_contents.decoded_content.decode().split('<div id="break"></div>')

        repo.update_file(index_contents.path, "committing files", f'{html_split[0]} {added_link} <div id="break"></div> {html_split[1]}', index_contents.sha, branch=git_branch)

    # Delete local file
    if delete_local:
        os.remove(filename)


def get_dates_html(metadata):
    ''' Return a html blurb of date details '''
    
    html = '<ul>'
    for date in metadata.dates:
        html += f"<li><span style='font-weight: bold;'>{date.date_type}:</span> {date.date}</li>"

    html += '</ul>'

    return html

def get_subjects_html(metadata):
    ''' Return a html blurb of subject details '''
    
    html = '<ul>'
    for subject in metadata.subjects:
        if subject.subject_scheme:
            html += f"<li>{subject.subject} ({subject.subject_scheme})</li>"
        else:
            html += f"<li>{subject.subject}</li>"

    html += '</ul>'

    return html


def get_creators_html(metadata):
    ''' Return a html blurb of creator details '''
    
    html = ''
    if len(metadata.creators):  
        html += '<ul>'
        for creator in metadata.creators:
            creator_html = creator.creator_name

            if len(creator.name_identifiers):
                identifiers_html = ''
                for identifier in creator.name_identifiers:
                    if identifier.startswith('https://orcid.org/'):
                        identifiers_html += f" <a href='{identifier}'>{identifier}</a> {ORCID_LOGO}"
                    elif identifier.startswith('https://ror.org/'):
                        identifiers_html += f" <a href='{identifier}'>{identifier}</a> {ROR_LOGO}"

                creator_html = f"{creator_html} ({identifiers_html})"

            if len(creator.affiliations):
                creator_html += "<ul>"
                for affiliation in creator.affiliations:
                    if affiliation.identifier:
                        creator_html += f"<li><a href='{affiliation.identifier}'>{affiliation.name}</a>{ROR_LOGO}</li>"
                    else:
                        creator_html += f"<li>{affiliation.name}</li>"

                creator_html += "</ul>"

            html += f"<li>{creator_html}</li>"

        html += f"</ul>"
        
    return html


def get_publisher_html(metadata):
    ''' Return a html blurb of publisher details '''
    
    html = ''

    if metadata.publisher.identifier:
        ror = metadata.publisher.identifier
        name = metadata.publisher.name
        publisher_html = f"<p><a href='{ror}' target='_blank'>{name}</a> {ROR_LOGO}</p>"
    else:
        name = metadata.publisher.name
        publisher_html = f"<p>{name}</p>"

    return publisher_html


def get_alternate_identifiers_html(metadata):
    ''' Return a html blurb of alternate identifier details '''
    
    html = ''
    if len(metadata.descriptions):  
        html += '<ul>'
        for alternate_identifier in metadata.alternate_identifiers:
            alternate_identifier_html = f"<li><span style='font-weight: bold;'>{alternate_identifier.alternate_identifier_type}:</span> {alternate_identifier.alternate_identifier}</li>"
            html += alternate_identifier_html

    return html


def get_descriptions_html(metadata):
    ''' Return a html blurb of description details '''
    
    html = ''
    if len(metadata.descriptions):  
        html += '<ul>' 
        for description in metadata.descriptions:
            description_html = f"<li><span style='font-weight: bold;'>{description.description_type}:</span> {description.description}</li>"
            html += description_html

        html += '</ul>'

    return html


def get_related_identifiers_html(metadata):
    ''' Return a html blurb of related identifiers details '''
    
    html = ''
    if len(metadata.related_identifiers):  
        html += '<ul>' 

        for related_identifier in metadata.related_identifiers:
            if related_identifier.related_identifier_type == 'DOI':
                related_identifier_html = f"<li><span style='font-weight: bold;'>{related_identifier.relation_type}:</span> <a href='{related_identifier.related_identifier}'>{related_identifier.related_identifier}{DOI_LOGO}</a></li>"
            else:
                related_identifier_html = f"<li><span style='font-weight: bold;'>{related_identifier.relation_type}:</span> {related_identifier.related_identifier} ({related_identifier.related_identifier_type})</li>"
            html += related_identifier_html

        html += '</ul>'

    return html


def get_sizes_html(metadata):
    ''' Return a html blurb of size details '''
    
    html = ''
    if len(metadata.sizes):  
        html += '<ul>' 

        for size in metadata.sizes:
            size_html = f"<li>{size}</li>"
            html += size_html

        html += '</ul>'

    return html


def get_formats_html(metadata):
    ''' Return a html blurb of formats details '''
    
    html = ''
    if len(metadata.formats):
        html += '<ul>'

        for format in metadata.formats:
            format_html = f"<li>{format}</li>"
            html += format_html

        html += '</ul>'

    return html


def get_rights_html(metadata):
    ''' Return a html blurb of rights details '''

    html = ''
    if len(metadata.rights_list):
        html += '<ul>'

        for rights in metadata.rights_list:
            if rights.rights_identifier:
                right_html = f"<li><a href='{rights.rights_uri}'>{rights.rights} </a> ({rights.rights_identifier})</li>"
                html += right_html

        html += '</ul>'

    return html


def get_fundings_html(metadata):
    ''' Return a html blurb of funding details '''

    html = ''
    if len(metadata.funding_references):  
        html += '<ul>'
        for funding in metadata.funding_references:
            if funding.award_title and funding.award_uri:
                funding_html = f"<li><span style='font-weight: bold;'>{funding.funder_name}:</span> <a href='{funding.award_uri}'>{funding.award_title}</a></li>"
            else:
                funding_html = f"<li>{funding.funder_name}</li>"
            html += funding_html

        html += '</ul>'

    return html


def generate_landing_page(record):
    ''' Generate a web landing page for a DOI record '''

    BASE_DIR = Path(__file__).resolve().parent
    # template_path = BASE_DIR / "templates" / "unsw_template_1.html"
    template_path = BASE_DIR / "templates" / "unsw_template_1.html"
    Path("landing_pages").mkdir(parents=True, exist_ok=True)
    output_path = BASE_DIR / "landing_pages" / f"{record.identifier}.html"
    
    html = template_path.read_text(encoding="utf-8")

    # TITLE
    html = html.replace("{{ title }}", record.metadata.titles[0].title)

    # DOI / IDENTIFIER
    if record.metadata.identifier.identifier_value:
        html = html.replace("{{ doi }}", f"<a href='https://doi.org/{record.metadata.identifier.identifier_value}' target='_blank'>https://doi.org/{record.metadata.identifier.identifier_value}</a> {DOI_LOGO}")
    else:
        html = html.replace("{{ doi }}", 'No DOI Allocated')

    # RESOURCE TYPE
    html = html.replace("{{ resource_type }}", record.metadata.types.resource_type_general)

    # PUBLISHER
    publisher_html = get_publisher_html(record.metadata)
    html = html.replace("{{ publisher }}", publisher_html)

    # PUBLICATION YEAR
    html = html.replace("{{ publication_year }}", record.metadata.publication_year)

    # CREATOR(S)
    creators_html = get_creators_html(record.metadata)
    html = html.replace("{{ creators }}", creators_html)

    # SUBJECT(S)
    subjects_html = get_subjects_html(record.metadata)
    html = html.replace("{{ subjects }}", subjects_html)

    # DATE(S)
    dates_html = get_dates_html(record.metadata)
    html = html.replace("{{ dates }}", dates_html)

    # ALTERNATE IDENTIFIER(S)
    alternate_identifiers_html = get_alternate_identifiers_html(record.metadata)
    html = html.replace("{{ alternate_identifiers }}", alternate_identifiers_html)

    # DESCRIPTION(S)
    descriptions_html = get_descriptions_html(record.metadata)
    html = html.replace("{{ descriptions }}", descriptions_html)

    # LANGUAGE
    html = html.replace("{{ language }}", record.metadata.language)

    # RELATED IDENTIFIER(S)
    related_identifiers_html = get_related_identifiers_html(record.metadata)
    html = html.replace("{{ related_identifiers }}", related_identifiers_html)

    # SIZE(S)
    sizes_html = get_sizes_html(record.metadata)
    html = html.replace("{{ sizes }}", sizes_html)

    # FORMAT(S)
    formats_html = get_formats_html(record.metadata)
    html = html.replace("{{ formats }}", formats_html)

    # RIGHTS(S)
    rights_html = get_rights_html(record.metadata)
    html = html.replace("{{ rights }}", rights_html)

    # FUNDING(S)
    fundings_html = get_fundings_html(record.metadata)
    html = html.replace("{{ fundings }}", fundings_html)

    # # SET INSTRUMENT NAME/TITLE
    # html = html.replace("__INSTRUMENT_NAME__", instrument.name)

    # # SET DESCRIPTION
    # if instrument.description:
    #     html = html.replace("__INSTRUMENT_DESCRIPTION__", instrument.description)
    # else:
    #     html = html.replace("__INSTRUMENT_DESCRIPTION__", '')

    # # SET INSTRUMENT OWNERS
    # if hasattr(instrument, 'owners'):
    #     owners_html = get_owners_html(instrument.owners)
    #     html = html.replace("__INSTRUMENT_OWNERS__", owners_html)
    # else:
    #     html = html.replace("__INSTRUMENT_OWNERS__", '')

    # # SET INSTRUMENT MANUFACTURERS
    # if hasattr(instrument, 'manufacturers'):
    #     manufacturers_html = get_manufacturers_html(instrument.manufacturers)
    #     html = html.replace("__INSTRUMENT_MANUFACTURERS__", manufacturers_html)
    # else:
    #     html = html.replace("__INSTRUMENT_MANUFACTURERS__", '')

    # # SET INSTRUMENT MODEL
    # if hasattr(instrument, 'model'):
    #     model_html = get_model_html(instrument.model)
    #     html = html.replace("__INSTRUMENT_MODEL__", model_html)
    # else:
    #     html = html.replace("__INSTRUMENT_MODEL__", '')

    # # SET RELATED IDENTIFIERS
    # if hasattr(instrument, 'related_identifiers'):
    #     related_identifiers_html = get_related_identifiers_html(instrument.related_identifiers)
    #     html = html.replace("__RELATED_IDENTIFIERS__", related_identifiers_html)
    # else:
    #     html = html.replace("__RELATED_IDENTIFIERS__", '')  

    # # SET ALTERNATE IDENTIFIERS
    # if hasattr(instrument, 'alternate_identifiers'):
    #     alternate_identifiers_html = get_alternate_identifiers_html(instrument.alternate_identifiers)
    #     html = html.replace("__ALTERNATE_IDENTIFIERS__", alternate_identifiers_html)
    # else:
    #     html = html.replace("__ALTERNATE_IDENTIFIERS__", '')  

    # # SET DATES
    # if hasattr(instrument, 'dates'):
    #     dates_html = get_dates_html(instrument.dates)
    #     html = html.replace("__DATES__", dates_html)
    # else:
    #     html = html.replace("__DATES__", '')  

    # # SET INSTRUMENT TYPES
    # if hasattr(instrument, 'instrument_types'):
    #     instrument_types_html = get_instrument_types_html(instrument.instrument_types)
    #     html = html.replace("__INSTRUMENT_TYPES__", instrument_types_html)
    # else:
    #     html = html.replace("__INSTRUMENT_TYPES__", '')  






    # WRITE HTML FILE
    # with open(f"{instrument.local_id}.html", "w") as fp:
        # fp.write(html)
    output_path.write_text(html, encoding="utf-8")

    # if use_github:
        # push_to_github(instrument.name, f"{instrument.local_id}.html", git_branch, github_repo)

    
