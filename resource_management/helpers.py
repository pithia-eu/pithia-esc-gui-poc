def get_lower_level_resource_types(resource_type):
    resource_types = [
        'organisation',
        'individual',
        'project',
        'platform',
        'instrument',
        'operation',
        'acquisition',
        'computation',
        'process',
        'data_collection',
    ]
    return resource_types[:resource_types.index(resource_type)]

def get_mongodb_models_from_resource_types(resource_types):
    