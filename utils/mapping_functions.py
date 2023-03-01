def prepare_resource_for_template(resource):
    if '_id' in resource:
        resource['id'] = resource['_id']
    if 'entryName' in resource:
        resource['name'] = resource['entryName']
    if 'entryDescription' in resource:
        resource['description'] = resource['entryDescription']
    if 'dataSubsetName' in resource:
        resource['name'] = resource['dataSubsetName']
    if 'dataSubsetDescription' in resource:
        resource['description'] = resource['dataSubsetDescription']
    return resource