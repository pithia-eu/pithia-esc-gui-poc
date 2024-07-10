from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class PithiaIdentifierMetadataUpdate:
    localid: Optional[str] = None
    namespace: Optional[str] = None
    version: Optional[str] = '1'
    creation_date: Optional[str] = None
    last_modification_date: Optional[str] = None


@dataclass(kw_only=True)
class ContactInfoAddressMetadataUpdate:
    delivery_point: Optional[str] = None
    city: Optional[str] = None
    administrative_area: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    electronic_mail_address: Optional[str] = None


@dataclass(kw_only=True)
class ContactInfoMetadataUpdate:
    phone: Optional[str] = None
    address: Optional[ContactInfoAddressMetadataUpdate] = ContactInfoAddressMetadataUpdate()
    online_resource: Optional[str] = None
    hours_of_service: Optional[str] = None
    contact_instructions: Optional[str] = None
