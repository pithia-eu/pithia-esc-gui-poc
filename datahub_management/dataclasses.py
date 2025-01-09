from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class CatalogueDataSubsetOnlineResource:
    name: Optional[str] = None
    file_input_name: Optional[str] = None

@dataclass
class CatalogueDataSubsetOnlineResourceUpdate(CatalogueDataSubsetOnlineResource):
    datahub_file_name: Optional[bool] = None
    is_existing_datahub_file_used: Optional[bool] = False