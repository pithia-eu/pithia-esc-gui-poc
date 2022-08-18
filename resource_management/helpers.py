from common.mongodb_models import CurrentIndividual, CurrentProject


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
    # TODO: Change after testing
    return f'https://resources.pithia.eu/2.2/{namespace}/{resource_type}/{localid}'

def get_individuals_referencing_organisation_url(organisation_url):
    return CurrentIndividual.find({
        'organisation.xlink:href': organisation_url
    })

def get_projects_referencing_individual_url(individual_url):
    return CurrentProject.find({
        'relatedParty': {
            'ResponsiblePartyInfo.party.xlink:href': individual_url
        }
    })