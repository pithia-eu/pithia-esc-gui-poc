from validation.metadata_validation import parse_xml_file

def generate_doi(resource_detail_url):
    # doi = DoiAPI.create_doi(resource_detail_url)
    # return doi
    doi = {
        'kernelMetadata': {
            'registrationAgencyDoiName': '10.1000/ra-5',
            'issueDate': '2015-01-07',
            'issueNumber': '7',
            'referentCreation': {
                'name': {
                    '@primaryLanguage': 'en',
                    'value': 'Test',
                    'type': 'Title',
                },
                'identifier': {
                    'nonUriValue': '10.5240/B94E-F500-7164-57DB-82F5-6',
                    'uri': [
                        {
                            '@returnType': 'text/html',
                            '#text': 'https://ui.eidr.org/view/content?id=10.5240/B94E-F500-7164-57DB-82F5-6',
                        },
                        {
                            '@returnType': 'text/html',
                            '#text': 'https://ui.eidr.org/view/content?id=10.5240/B94E-F500-7164-57DB-82F5-6',
                        }
                    ],
                    'type': 'EidrContentID',
                }
            },
        }
    }
    return doi

def add_doi_to_xml_file(xml_file, doi):
    # Use lxml to add or fill out the doi element
    # Add makes more sense
    # xml_file_with_doi = xml_file
    # return xml_file_with_doi
    xml_file_parsed = parse_xml_file(xml_file)
    root = xml_file_parsed.getroot()
    print(root)
    return