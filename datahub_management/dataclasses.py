from dataclasses import dataclass, field
from typing import Optional


@dataclass(kw_only=True)
class CatalogueDataSubsetOnlineResource:
    name: Optional[str] = None
    file_input_name: Optional[str] = None