from common.models import StaticDatasetEntry


def _get_localid_from_url(url):
    return [
        url_part
        for url_part in url.split('/')
        if url_part
    ][-1]

def get_registered_features_of_interest():
    registered_static_dataset_entries = list(StaticDatasetEntry.objects.all())
    return list(set(
        _get_localid_from_url(url)
        for sde in registered_static_dataset_entries
        for url in sde.properties.features_of_interest
    ))