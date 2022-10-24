def create_resource_url(resource_type, namespace, localid):
    if resource_type.lower() == 'computationcapabilities' and not localid.startswith('ComputationCapabilities_'):
        localid = f'ComputationCapabilities_{localid}'
    if resource_type.lower() == 'acquisitioncapabilities' and not localid.startswith('AcquisitionCapabilities_'):
        localid = f'AcquisitionCapabilities_{localid}'
    if not resource_type.lower() == 'computationcapabilities' and not resource_type.lower() == 'acquisitioncapabilities' and not localid.startswith(f'{resource_type.capitalize()}_'):
        localid = f'{resource_type.capitalize()}_{localid}'
    return f'https://metadata.pithia.eu/resources/2.2/{resource_type}/{namespace}/{localid}'