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