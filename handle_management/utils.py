from common.mongodb_models import HandleUrlMapping

def add_handle_to_url_mapping(handle: str, url: str, session=None):
    HandleUrlMapping.insert_one({
        'handle_name': handle,
        'url': url,
    }, session=session)