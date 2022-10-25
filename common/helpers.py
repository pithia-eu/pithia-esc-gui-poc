from bson import ObjectId
from .mongodb_models import CurrentAcquisitionCapability, CurrentInstrument

def create_resource_url(resource_type, namespace, localid):
    if resource_type.lower() == 'computationcapabilities' and not localid.startswith('computationCapabilities_'):
        localid = f'computationCapabilities_{localid}'
    if resource_type.lower() == 'acquisitioncapabilities' and not localid.startswith('acquisitionCapabilities_'):
        localid = f'acquisitionCapabilities_{localid}'
    if not resource_type.lower() == 'computationcapabilities' and not resource_type.lower() == 'acquisitioncapabilities' and not localid.startswith(f'{resource_type.capitalize()}_'):
        localid = f'{resource_type.capitalize()}_{localid}'
    return f'https://metadata.pithia.eu/resources/2.2/{resource_type}/{namespace}/{localid}'

def get_acquisition_capabilities_referencing_instrument_operational_ids(instrument_id: ObjectId) -> list:
    instrument = CurrentInstrument.find_one({
        '_id': ObjectId(instrument_id)
    }, {
        'identifier': True,
        'operationalMode': True
    })
    if 'operationalMode' not in instrument:
        return []
    instrument_url = create_resource_url('instrument', instrument['identifier']['PITHIA_Identifier']['namespace'], instrument['identifier']['PITHIA_Identifier']['localID'])
    instrument_urls_with_operational_mode_ids = []
    for om in instrument['operationalMode']:
        iom = om['InstrumentOperationalMode']
        instrument_urls_with_operational_mode_ids.append(f'{instrument_url}#{iom["id"]}')
    current_acquisition_capabilities_referencing_instrument_operational_ids = list(CurrentAcquisitionCapability.find({
        'instrumentModePair.InstrumentOperationalModePair.mode.@xlink:href': {
            '$in': instrument_urls_with_operational_mode_ids
        }
    }))

    return current_acquisition_capabilities_referencing_instrument_operational_ids