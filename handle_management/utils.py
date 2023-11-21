import os

from common.models import HandleURLMapping


def add_handle_to_url_mapping(handle: str, url: str):
    handle_url_mapping = HandleURLMapping(
        id=handle,
        handle_name=handle,
        url=url
    )
    handle_url_mapping.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])