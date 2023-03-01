def get_resource_by_pithia_identifier_components(resource_mongodb_model, localid, namespace):
    return resource_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.localID': localid,
        'identifier.PITHIA_Identifier.namespace': namespace,
    })

def get_resource_by_pithia_identifier_components_and_op_mode_id(resource_mongodb_model, localid, namespace, op_mode_id):
    # resource_mongodb_model should be CurrentInstrument, but this may be different
    # if a user made an error whilst inputting URLs into the metadata file.
    return resource_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.localID': localid,
        'identifier.PITHIA_Identifier.namespace': namespace,
        'operationalMode.InstrumentOperationalMode.id': op_mode_id,
    })

def divide_resource_url_into_main_components(resource_url):
    resource_url_split = resource_url.split('/')
    return {
        'url_base': '/'.join(resource_url_split[:-3]),
        'resource_type': resource_url_split[-3],
        'namespace': resource_url_split[-2],
        'localid': resource_url_split[-1],
    }

def divide_catalogue_related_resource_url_into_main_components(resource_url):
    resource_url_split = resource_url.split('/')
    return {
        'url_base': '/'.join(resource_url_split[:-4]),
        'resource_type': resource_url_split[-4],
        'namespace': resource_url_split[-3],
        'event': resource_url_split[-2],
        'localid': resource_url_split[-1],
    }

def divide_resource_url_from_op_mode_id(resource_url_with_op_mode_id):
    resource_url_with_op_mode_id_split = resource_url_with_op_mode_id.split('#')
    return {
        'resource_url': '#'.join(resource_url_with_op_mode_id_split[:-1]),
        'op_mode_id': resource_url_with_op_mode_id_split[-1],
    }