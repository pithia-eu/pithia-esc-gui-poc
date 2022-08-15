from register.mongodb_models import CurrentIndividual


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

def create_resource_url(namespace, resource_type, localid):
    return f'https://metadata.pithia.eu/resources/2.2/{namespace}/{resource_type}/{localid}'

def get_individuals_referencing_resource_url(resource_url):
    return CurrentIndividual.find_one({
        
    })