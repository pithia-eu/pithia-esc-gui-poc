from common.models import HandleURLMapping
from common.mongodb_models import HandleUrlMapping

def add_handle_to_url_mapping(handle: str, url: str):
    handle_url_mapping = HandleURLMapping(
        handle_name=handle,
        url=url
    )
    handle_url_mapping.save()

def add_handle_to_url_mapping_old(handle: str, url: str, session=None):
    HandleUrlMapping.insert_one({
        'handle_name': handle,
        'url': url,
    }, session=session)