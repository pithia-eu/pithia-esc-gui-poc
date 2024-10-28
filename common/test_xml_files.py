from django.core.files.uploadedfile import SimpleUploadedFile


# ORGANISATIONS
ORGANISATION_METADATA_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                    </CI_Telephone>
                </phone>           
                <address>
                    <CI_Address>                   
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
                <hoursOfService><gco:CharacterString>0:00am-0:00am</gco:CharacterString></hoursOfService>
                <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)

ORGANISATION_ALTERNATE_METADATA_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                    </CI_Telephone>
                </phone>           
                <address>
                    <CI_Address>
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
                <hoursOfService><gco:CharacterString>0:00am-0:00am</gco:CharacterString></hoursOfService>
                <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)

ORGANISATION_CONTACT_INFO_1_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone>
                        <voice>
                            <gco:CharacterString>+1 000-000-0000</gco:CharacterString>
                        </voice>
                        <voice>
                            <gco:CharacterString>+2 000-000-0000</gco:CharacterString>
                        </voice>
                        <facsimile>
                            <gco:CharacterString>+2 000-000-0001</gco:CharacterString>
                        </facsimile>
                        <!-- telephone -->
                    </CI_Telephone>
                </phone>
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)

ORGANISATION_CONTACT_INFO_2_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test</name>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)

ORGANISATION_MULTIPLE_ADDRESSES_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <address>
                    <CI_Address>
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <address>
                    <CI_Address>
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)

ORGANISATION_UPDATED_METADATA_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test Update</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                    </CI_Telephone>
                </phone>           
                <address>
                    <CI_Address>                   
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
                <hoursOfService><gco:CharacterString>0:00am-0:00am</gco:CharacterString></hoursOfService>
                <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)
ORGANISATION_2_METADATA_XML = SimpleUploadedFile(
    'Organisation_Test_2.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test_2</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                    </CI_Telephone>
                </phone>           
                <address>
                    <CI_Address>                   
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
                <hoursOfService><gco:CharacterString>0:00am-0:00am</gco:CharacterString></hoursOfService>
                <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)

ORGANISATION_WITH_INVALID_SYNTAX_METADATA_XML = SimpleUploadedFile(
    'Organisation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Organisation 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Organisation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T12:50:00Z</creationDate>
                <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Organisation Test Invalid Syntax</name>
        <contactInfo
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                    </CI_Telephone>
                </phone>           
                <address>
                    <CI_Address>                   
                        <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
                <hoursOfService><gco:CharacterString>0:00am-0:00am</gco:CharacterString></hoursOfService>
                <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
            </CI_Contact>
        </contactInfo>
        <shortName>TEST</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
    </Organisation>
    '''
)


# INDIVIDUALS
INDIVIDUAL_METADATA_XML = SimpleUploadedFile(
    'Individual_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Individual 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >
    
        <identifier>
            <PITHIA_Identifier>
                <localID>Individual_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-03T11:00:00Z</creationDate>
                <lastModificationDate>2022-02-03T11:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>  
        <name>Individual Test</name>
        <contactInfo>
            <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
                <phone>
                    <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                    </CI_Telephone>
                </phone>           
                <address>
                    <CI_Address>                   
                        <deliveryPoint><gco:CharacterString>123 Xyz St., Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                        <city><gco:CharacterString>City</gco:CharacterString></city>
                        <administrativeArea><gco:CharacterString>ZZ</gco:CharacterString></administrativeArea>
                        <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                        <country><gco:CharacterString>Country</gco:CharacterString></country>
                        <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                    </CI_Address>
                </address>
                <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
                <hoursOfService><gco:CharacterString>0:00am-0:00pm</gco:CharacterString></hoursOfService>
                <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
            </CI_Contact>
        </contactInfo>
        <positionName>Test, Test</positionName>
        <organisation xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"></organisation> <!-- link to the organisation that this individual has the position name -->
    </Individual>
    '''
)


# PROJECTS
PROJECT_METADATA_XML = SimpleUploadedFile(
    'Project_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Project 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >    
        <identifier>
            <PITHIA_Identifier>
                <localID>Project_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-23T08:27:00Z</creationDate>
                <lastModificationDate>2022-08-23T08:27:49Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Project Test</name>
        <shortName>Pr_Test</shortName>
        <abstract>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Test update
        </abstract>
        <description>
        </description>
        <URL><gmd:URL>http://test.test/</gmd:URL></URL>
        <documentation>
            <Citation>
                <gmd:title><gco:CharacterString>Project Test (Pr_Test)</gco:CharacterString></gmd:title>
                <date xmlns="http://www.isotc211.org/2005/gmd">
                    <CI_Date>
                        <date><gco:Date>2018-02-09</gco:Date></date>
                        <dateType>
                            <CI_DateTypeCode codeList="" codeListValue="">Publication Date</CI_DateTypeCode>
                        </dateType>
                    </CI_Date>
                </date>
                <identifier xmlns="http://www.isotc211.org/2005/gmd">
                <MD_Identifier><code><gco:CharacterString>doi:10.5047/eps.2011.03.001</gco:CharacterString></code></MD_Identifier>
                </identifier>
                <gmd:otherCitationDetails>
                <gco:CharacterString>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                        labore et dolore magna aliqua.
                </gco:CharacterString>
                </gmd:otherCitationDetails>
                <onlineResource>
                <CI_OnlineResource xmlns="http://www.isotc211.org/2005/gmd">
                    <linkage>
                        <URL>http://www.isotc211.org/2005/gmd</URL>
                    </linkage>
                </CI_OnlineResource>
                </onlineResource>
            </Citation>
        </documentation>    
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>   
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>       
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>    
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>     
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test"/> <!-- NB changed namespace from pithia to lgdc -->
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <status xlink:href="https://metadata.pithia.eu/ontology/2.2/status/OnGoing"/> 
    </Project>
    '''
)

PROJECT_METADATA_WITH_INVALID_METADATA_URLS_XML = SimpleUploadedFile(
    'Project_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Project 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco" >    
        <identifier>
            <PITHIA_Identifier>
                <localID>Project_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-23T08:27:00Z</creationDate>
                <lastModificationDate>2022-08-23T08:27:49Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Project Test</name>
        <shortName>Pr_Test</shortName>
        <abstract>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </abstract>
        <description>
        </description>
        <URL><gmd:URL>http://test.test/</gmd:URL></URL>
        <documentation>
            <Citation>
                <gmd:title><gco:CharacterString>Project Test (Pr_Test)</gco:CharacterString></gmd:title>
                <date xmlns="http://www.isotc211.org/2005/gmd">
                    <CI_Date>
                        <date><gco:Date>2018-02-09</gco:Date></date>
                        <dateType>
                            <CI_DateTypeCode codeList="" codeListValue="">Publication Date</CI_DateTypeCode>
                        </dateType>
                    </CI_Date>
                </date>
                <identifier xmlns="http://www.isotc211.org/2005/gmd">
                <MD_Identifier><code><gco:CharacterString>doi:10.5047/eps.2011.03.001</gco:CharacterString></code></MD_Identifier>
                </identifier>
                <gmd:otherCitationDetails>
                <gco:CharacterString>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                        labore et dolore magna aliqua.
                </gco:CharacterString>
                </gmd:otherCitationDetails>
                <onlineResource>
                <CI_OnlineResource xmlns="http://www.isotc211.org/2005/gmd">
                    <linkage>
                        <URL>http://www.isotc211.org/2005/gmd</URL>
                    </linkage>
                </CI_OnlineResource>
                </onlineResource>
            </Citation>
        </documentation>    
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>   
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>       
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>    
        <keywords>
            <MD_Keywords xmlns="http://www.isotc211.org/2005/gmd">
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <keyword><gco:CharacterString>Test</gco:CharacterString></keyword>
                <type><MD_KeywordTypeCode codeList="#test1" codeListValue="Test"/></type>
            </MD_Keywords>
        </keywords>     
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/pithia/individual/Individual_PITHIA_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/pithia/organisation/Organisation_PITHIA"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/relatedPartyRole/PointOfContact"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/pithia/individual/Individual_PITHIA_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/relatedPartyRole/DataProvider"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/pithia/organisation/Organisation_PITHIA"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="http://metadata.pithia.eu/ontology/relatedPartyRole/DataProvider"/> 
                <party xlink:href="http://metadata.pithia.eu/resources/pithia/organisation/Organisation_PITHIA"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <status xlink:href="https://metadata.pithia.eu/ontology/2.2/status/OnGoing"/> 
    </Project>
    '''
)


# PLATFORMS
PLATFORM_METADATA_XML = SimpleUploadedFile(
    'Platform_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Platform
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        gml:id="p_n11">
        <identifier>
            <PITHIA_Identifier>
                <localID>Platform_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-03-14T16:00:00Z</creationDate>
                <lastModificationDate>2022-03-14T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Platform Test</name>
        <shortName>PT</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/platformType/GroundBasedStation" />
        <location>
            <Location>
                <geometryLocation>
                    <gml:Point gml:id="n11"
                        srsName="https://metadata.pithia.eu/ontology/2.2/crs/WGS84spherical">
                        <gml:pos></gml:pos>
                    </gml:Point>
                </geometryLocation>
                <nameLocation>
                    <EX_GeographicDescription xmlns="http://www.isotc211.org/2005/gmd">
                        <geographicIdentifier>
                            <MD_Identifier>
                                <code>
                                    <gco:CharacterString>Polar orbit in the magnetosphere and solar wind</gco:CharacterString>
                                </code>
                            </MD_Identifier>
                        </geographicIdentifier>
                    </EX_GeographicDescription>
                </nameLocation>
            </Location>
        </location>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact" />
                <party
                    xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test" />
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/Operator" />
                <party
                    xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test" />
            </ResponsiblePartyInfo>
        </relatedParty>
    </Platform>
    '''
)

PLATFORM_WITH_CHILD_PLATFORMS_METADATA_XML = SimpleUploadedFile(
    'Platform_Test_with_Child_Platforms.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Platform
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        gml:id="p_n11">
        <identifier>
            <PITHIA_Identifier>
                <localID>Platform_Test_with_Child_Platforms</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-03-14T16:00:00Z</creationDate>
                <lastModificationDate>2022-03-14T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Platform Test</name>
        <shortName>PT</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/platformType/GroundBasedStation" />
        <location>
            <Location>
                <geometryLocation>
                    <gml:Point gml:id="n11"
                        srsName="https://metadata.pithia.eu/ontology/2.2/crs/WGS84spherical">
                        <gml:pos></gml:pos>
                    </gml:Point>
                </geometryLocation>
                <nameLocation>
                    <EX_GeographicDescription xmlns="http://www.isotc211.org/2005/gmd">
                        <geographicIdentifier>
                            <MD_Identifier>
                                <code>
                                    <gco:CharacterString>Polar orbit in the magnetosphere and solar wind</gco:CharacterString>
                                </code>
                            </MD_Identifier>
                        </geographicIdentifier>
                    </EX_GeographicDescription>
                </nameLocation>
            </Location>
        </location>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact" />
                <party
                    xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test" />
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/Operator" />
                <party
                    xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test" />
            </ResponsiblePartyInfo>
        </relatedParty>
        <childPlatform xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test"></childPlatform>
    </Platform>
    '''
)

PLATFORM_WITH_POS_METADATA_XML = SimpleUploadedFile(
    'Platform_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Platform
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        gml:id="p_n11">
        <identifier>
            <PITHIA_Identifier>
                <localID>Platform_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-03-14T16:00:00Z</creationDate>
                <lastModificationDate>2022-03-14T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Platform Test</name>
        <shortName>PT</shortName>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/platformType/GroundBasedStation" />
        <location>
            <Location>
                <geometryLocation>
                    <gml:Point gml:id="n11"
                        srsName="https://metadata.pithia.eu/ontology/2.2/crs/WGS84spherical">
                        <gml:pos>50.09 4.59</gml:pos>
                    </gml:Point>
                </geometryLocation>
                <nameLocation>
                    <EX_GeographicDescription xmlns="http://www.isotc211.org/2005/gmd">
                        <geographicIdentifier>
                            <MD_Identifier>
                                <code>
                                    <gco:CharacterString>Polar orbit in the magnetosphere and solar wind</gco:CharacterString>
                                </code>
                            </MD_Identifier>
                        </geographicIdentifier>
                    </EX_GeographicDescription>
                </nameLocation>
            </Location>
        </location>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact" />
                <party
                    xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test" />
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/Operator" />
                <party
                    xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test" />
            </ResponsiblePartyInfo>
        </relatedParty>
    </Platform>
    '''
)


# OPERATIONS
OPERATION_METADATA_XML = SimpleUploadedFile(
    'Operation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Operation
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        gml:id="o_esr_dsnd">
        <identifier>
            <PITHIA_Identifier>
                <localID>Operation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-04T11:00:00Z</creationDate>
                <lastModificationDate>2022-08-04T12:22:06Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Operation Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <operationTime>
            <gml:TimePeriod gml:id="t_esr_dsnd">
                <gml:begin><gml:TimeInstant gml:id="ti1"><gml:timePosition>2000-03-07</gml:timePosition></gml:TimeInstant></gml:begin>
                <gml:end><gml:TimeInstant gml:id="ti2"><gml:timePosition>2050-12-31</gml:timePosition></gml:TimeInstant></gml:end>
            </gml:TimePeriod>
        </operationTime>
        <status xlink:href="https://metadata.pithia.eu/ontology/2.2/status/OnGoing"/>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <platform xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test"></platform>
    </Operation>
    '''
)


OPERATION_METADATA_WITH_TIME_INTERVAL_XML = SimpleUploadedFile(
    'Operation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Operation
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        gml:id="o_esr_dsnd">
        <identifier>
            <PITHIA_Identifier>
                <localID>Operation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-04T11:00:00Z</creationDate>
                <lastModificationDate>2022-08-04T12:22:06Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Operation Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <operationTime>
            <gml:TimePeriod gml:id="t_esr_dsnd">
                <gml:begin><gml:TimeInstant gml:id="ti1"><gml:timePosition>2000-03-07</gml:timePosition></gml:TimeInstant></gml:begin>
                <gml:end><gml:TimeInstant gml:id="ti2"><gml:timePosition>2050-12-31</gml:timePosition></gml:TimeInstant></gml:end>
                <gml:timeInterval unit="second">25</gml:timeInterval>
            </gml:TimePeriod>
        </operationTime>
        <status xlink:href="https://metadata.pithia.eu/ontology/2.2/status/OnGoing"/>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <platform xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test"></platform>
    </Operation>
    '''
)


# INSTRUMENTS
INSTRUMENT_METADATA_XML = SimpleUploadedFile(
    'Instrument_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Instrument 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >
        
        <identifier>
            <PITHIA_Identifier>
                <localID>Instrument_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2013-04-25T14:00:00Z</creationDate>
                <lastModificationDate>2013-04-25T14:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>   
        <name>Instrument Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder"/> <!-- use the instrumentType ontology to describe the type of the instrument -->
        
        <operationalMode>
            <InstrumentOperationalMode>
                <id>instrumentoperationalmode1</id> <!-- the id should not  include any space characters. It is used to be referenced by Acquisition -->
                <name>Instrument Operational Mode 1</name> <!-- it would be preferable the name of the mode not to include any space characters -->
                <description>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                    labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                    laboris nisi ut aliquip ex ea commodo consequat.
                </description>
            </InstrumentOperationalMode> 
        </operationalMode>
        <operationalMode>
            <InstrumentOperationalMode>
                <id>instrumentoperationalmode2</id> <!-- the id should not  include any space characters. It is used to be referenced by Acquisition -->
                <name>Instrument Operational Mode 2</name>
                <description>
                    Duis aute irure dolor in reprehenderit in
                    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
                    non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </description>
            </InstrumentOperationalMode>
        </operationalMode>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
    </Instrument>
    '''
)

INSTRUMENT_WITH_NO_OP_MODES_METADATA_XML = SimpleUploadedFile(
    'Instrument_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Instrument 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >
        
        <identifier>
            <PITHIA_Identifier>
                <localID>Instrument_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2013-04-25T14:00:00Z</creationDate>
                <lastModificationDate>2013-04-25T14:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>   
        <name>Instrument Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder"/> <!-- use the instrumentType ontology to describe the type of the instrument -->
    </Instrument>
    '''
)


# ACQUISITION CAPABILITIES
ACQUISITION_CAPABILITIES_METADATA_XML = SimpleUploadedFile(
    'AcquisitionCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <AcquisitionCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >

        <identifier>
            <PITHIA_Identifier>
                <localID>AcquisitionCapabilities_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-10-04T16:00:00Z</creationDate>
                <lastModificationDate>2022-10-04T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition capabilities of Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <capabilities>
            <processCapability>
                <name>Signal Strength</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <units xlink:href="https://metadata.pithia.eu/ontology/2.2/unit/dB"/> 
            </processCapability>
            <processCapability>
                <name>Signal Polarization</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Doppler Frequency</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Angle of Arrival</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction"/> 
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <!-- <crs xlink:href="https://metadata.pithia.eu/ontology/2.2/crs/Az-Zenith"/> -->
            </processCapability>
        </capabilities>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0"/>
        </qualityAssessment>
        <!-- Instrument that has these acquisition capabilities -->
        <instrumentModePair>
            <InstrumentOperationalModePair>
                <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test"/>
                <mode xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test#instrumentoperationalmode1"/>
            </InstrumentOperationalModePair>
        </instrumentModePair>    
    </AcquisitionCapabilities>
    '''
)

ACQUISITION_CAPABILITIES_WITH_INVALID_OP_MODE_URLS_METADATA_XML = SimpleUploadedFile(
    'AcquisitionCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <AcquisitionCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >

        <identifier>
            <PITHIA_Identifier>
                <localID>AcquisitionCapabilities_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-10-04T16:00:00Z</creationDate>
                <lastModificationDate>2022-10-04T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition capabilities of Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <capabilities>
            <processCapability>
                <name>Signal Strength</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <units xlink:href="https://metadata.pithia.eu/ontology/2.2/unit/dB"/> 
            </processCapability>
            <processCapability>
                <name>Signal Polarization</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Doppler Frequency</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Angle of Arrival</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction"/> 
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <!-- <crs xlink:href="https://metadata.pithia.eu/ontology/2.2/crs/Az-Zenith"/> -->
            </processCapability>
        </capabilities>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0"/>
        </qualityAssessment>
        <!-- Instrument that has these acquisition capabilities -->
        <instrumentModePair>
            <InstrumentOperationalModePair>
                <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test"/>
                <mode xlink:href="https://metadata.pithia.eu/resources/instrument/test/Instrument_Test#instrumentoperationalmodexyz"/>
            </InstrumentOperationalModePair>
        </instrumentModePair>    
    </AcquisitionCapabilities>
    '''
)

ACQUISITION_CAPABILITIES_MULTIPLE_INSTRUMENT_MODE_PAIRS_METADATA_XML = SimpleUploadedFile(
    'AcquisitionCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <AcquisitionCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >

        <identifier>
            <PITHIA_Identifier>
                <localID>AcquisitionCapabilities_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-10-04T16:00:00Z</creationDate>
                <lastModificationDate>2022-10-04T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition capabilities of Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <capabilities>
            <processCapability>
                <name>Signal Strength</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <units xlink:href="https://metadata.pithia.eu/ontology/2.2/unit/dB"/> 
            </processCapability>
            <processCapability>
                <name>Signal Polarization</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Doppler Frequency</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Angle of Arrival</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction"/> 
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <!-- <crs xlink:href="https://metadata.pithia.eu/ontology/2.2/crs/Az-Zenith"/> -->
            </processCapability>
        </capabilities>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0"/>
        </qualityAssessment>
        <!-- Instrument that has these acquisition capabilities -->
        <instrumentModePair>
            <InstrumentOperationalModePair>
                <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test"/>
                <mode xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test#instrumentoperationalmode1"/>
            </InstrumentOperationalModePair>
        </instrumentModePair>
        <instrumentModePair>
            <InstrumentOperationalModePair>
                <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_2"/>
                <mode xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_2#instrumentoperationalmode2"/>
            </InstrumentOperationalModePair>
        </instrumentModePair>
    </AcquisitionCapabilities>
    '''
)

ACQUISITION_CAPABILITIES_MULTIPLE_INSTRUMENT_MODE_PAIRS_2_METADATA_XML = SimpleUploadedFile(
    'AcquisitionCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <AcquisitionCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >

        <identifier>
            <PITHIA_Identifier>
                <localID>AcquisitionCapabilities_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-10-04T16:00:00Z</creationDate>
                <lastModificationDate>2022-10-04T16:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition capabilities of Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <capabilities>
            <processCapability>
                <name>Signal Strength</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <units xlink:href="https://metadata.pithia.eu/ontology/2.2/unit/dB"/> 
            </processCapability>
            <processCapability>
                <name>Signal Polarization</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Doppler Frequency</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Angle of Arrival</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction"/> 
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <!-- <crs xlink:href="https://metadata.pithia.eu/ontology/2.2/crs/Az-Zenith"/> -->
            </processCapability>
        </capabilities>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ0"/>
        </qualityAssessment>
        <!-- Instrument that has these acquisition capabilities -->
        <instrumentModePair>
            <InstrumentOperationalModePair>
                <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test"/>
                <mode xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test#instrumentoperationalmode1"/>
            </InstrumentOperationalModePair>
            <InstrumentOperationalModePair>
                <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_2"/>
                <mode xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_2#instrumentoperationalmode2"/>
            </InstrumentOperationalModePair>
        </instrumentModePair>
    </AcquisitionCapabilities>
    '''
)


# ACQUISITIONS
ACQUISITION_METADATA_XML = SimpleUploadedFile(
    'Acquisition_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Acquisition
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">

        <identifier>
            <PITHIA_Identifier>
                <localID>Acquisition_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-28T10:00:00Z</creationDate>
                <lastModificationDate>2022-02-28T10:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
            cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!--
            Need to specify all platform-instrument pairings for the whole GIRO ionosonde
        network here
            Historic data also included
        -->
        <capabilityLinks>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <acquisitionCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test" />
            </capabilityLink>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <acquisitionCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test" />
            </capabilityLink>
        </capabilityLinks>
    </Acquisition>
    '''
)

ACQUISITION_WITH_INSTRUMENT_METADATA_XML = SimpleUploadedFile(
    'Acquisition_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Acquisition
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">

        <identifier>
            <PITHIA_Identifier>
                <localID>Acquisition_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-28T10:00:00Z</creationDate>
                <lastModificationDate>2022-02-28T10:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
            cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!--
            Need to specify all platform-instrument pairings for the whole GIRO ionosonde
        network here
            Historic data also included
        -->
        <capabilityLinks>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <acquisitionCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test" />
            </capabilityLink>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <acquisitionCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test" />
            </capabilityLink>
        </capabilityLinks>
        <instrument xlink:href="https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test"/>
    </Acquisition>
    '''
)

ACQUISITION_WITH_TIME_SPANS_METADATA_XML = SimpleUploadedFile(
    'Acquisition_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Acquisition
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2">

        <identifier>
            <PITHIA_Identifier>
                <localID>Acquisition_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-28T10:00:00Z</creationDate>
                <lastModificationDate>2022-02-28T10:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Acquisition Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
            cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!--
            Need to specify all platform-instrument pairings for the whole GIRO ionosonde
        network here
            Historic data also included
        -->
        <capabilityLinks>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <acquisitionCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test" />
            </capabilityLink>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <acquisitionCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/test/AcquisitionCapabilities_Test" />
                <timeSpan>
                    <gml:beginPosition>2024-11-11</gml:beginPosition>
                    <gml:endPosition indeterminatePosition="after" />
                </timeSpan>
                <timeSpan>
                    <gml:beginPosition>2024-11-11</gml:beginPosition>
                    <gml:endPosition />
                </timeSpan>
            </capabilityLink>
        </capabilityLinks>
    </Acquisition>
    '''
)


# COMPUTATION CAPABILITIES
COMPUTATION_CAPABILITIES_METADATA_XML = SimpleUploadedFile(
    'ComputationCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <ComputationCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <!--
    The computation process that produces observed properties from its input data.
    Input data may be an acquisition or some other computatation, not listed here yet. TODO: add input specification
    Each newly computed observed property that this computation can produce is defined as its *capability*.
    The list of capabilities is all-inclusive, even though not every computation can engage all capabilities.
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>ComputationCapabilities_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-16T07:55:00Z</creationDate>
                <lastModificationDate>2022-08-16T07:55:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Capabilities Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!-- There are no new capabilities here to list, this is manual verification to produce L2V data -->
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual" />
        <version />
        <softwareReference />
        <processingInput />
        <algorithm />
    </ComputationCapabilities>
    '''
)

COMPUTATION_CAPABILITIES_2_METADATA_XML = SimpleUploadedFile(
    'ComputationCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <ComputationCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <!--
    The computation process that produces observed properties from its input data.
    Input data may be an acquisition or some other computatation, not listed here yet. TODO: add input specification
    Each newly computed observed property that this computation can produce is defined as its *capability*.
    The list of capabilities is all-inclusive, even though not every computation can engage all capabilities.
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>ComputationCapabilities_Test_2</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-16T07:55:00Z</creationDate>
                <lastModificationDate>2022-08-16T07:55:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Capabilities Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!-- There are no new capabilities here to list, this is manual verification to produce L2V data -->
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual" />
        <version />
        <softwareReference />
        <processingInput />
        <algorithm />
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test"/>
    </ComputationCapabilities>
    '''
)

COMPUTATION_CAPABILITIES_3_METADATA_XML = SimpleUploadedFile(
    'ComputationCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <ComputationCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <!--
    The computation process that produces observed properties from its input data.
    Input data may be an acquisition or some other computatation, not listed here yet. TODO: add input specification
    Each newly computed observed property that this computation can produce is defined as its *capability*.
    The list of capabilities is all-inclusive, even though not every computation can engage all capabilities.
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>ComputationCapabilities_Test_3</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-16T07:55:00Z</creationDate>
                <lastModificationDate>2022-08-16T07:55:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Capabilities Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!-- There are no new capabilities here to list, this is manual verification to produce L2V data -->
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual" />
        <version />
        <softwareReference />
        <processingInput />
        <algorithm />
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test_2"/>
    </ComputationCapabilities>
    '''
)

COMPUTATION_CAPABILITIES_4_METADATA_XML = SimpleUploadedFile(
    'ComputationCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <ComputationCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <!--
    The computation process that produces observed properties from its input data.
    Input data may be an acquisition or some other computatation, not listed here yet. TODO: add input specification
    Each newly computed observed property that this computation can produce is defined as its *capability*.
    The list of capabilities is all-inclusive, even though not every computation can engage all capabilities.
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>ComputationCapabilities_Test_4</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-16T07:55:00Z</creationDate>
                <lastModificationDate>2022-08-16T07:55:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Capabilities Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!-- There are no new capabilities here to list, this is manual verification to produce L2V data -->
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual" />
        <version />
        <softwareReference />
        <processingInput />
        <algorithm />
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test_3"/>
    </ComputationCapabilities>
    '''
)

COMPUTATION_CAPABILITIES_4a_METADATA_XML = SimpleUploadedFile(
    'ComputationCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <ComputationCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <!--
    The computation process that produces observed properties from its input data.
    Input data may be an acquisition or some other computatation, not listed here yet. TODO: add input specification
    Each newly computed observed property that this computation can produce is defined as its *capability*.
    The list of capabilities is all-inclusive, even though not every computation can engage all capabilities.
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>ComputationCapabilities_Test_4a</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-16T07:55:00Z</creationDate>
                <lastModificationDate>2022-08-16T07:55:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Capabilities Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <!-- There are no new capabilities here to list, this is manual verification to produce L2V data -->
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/Test" />
        <version />
        <softwareReference />
        <processingInput />
        <algorithm />
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test_3"/>
    </ComputationCapabilities>
    '''
)

COMPUTATION_CAPABILITIES_FULL_METADATA_XML = SimpleUploadedFile(
    'ComputationCapabilities_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <ComputationCapabilities
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        xmlns:gco19115="http://standards.iso.org/iso/19115/-3/gco/1.0"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:mrl="http://standards.iso.org/iso/19115/-3/mrl/1.0"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <!--
    The computation process that produces observed properties from its input data.
    Input data may be an acquisition or some other computatation, not listed here yet. TODO: add input specification
    Each newly computed observed property that this computation can produce is defined as its *capability*.
    The list of capabilities is all-inclusive, even though not every computation can engage all capabilities.
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>ComputationCapabilities_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-08-16T07:55:00Z</creationDate>
                <lastModificationDate>2022-08-16T07:55:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Capabilities Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <documentation>
            <Citation>
                <gmd:title>
                    <gco:CharacterString>Documentation title</gco:CharacterString>
                </gmd:title>
                <date xmlns="http://www.isotc211.org/2005/gmd">
                    <CI_Date>
                        <date>
                            <gco:Date>2024-08-01</gco:Date>
                        </date>
                        <dateType>
                            <CI_DateTypeCode codeList="" codeListValue="">Publication Date</CI_DateTypeCode>
                        </dateType>
                    </CI_Date>
                </date>
                <identifier xmlns="http://www.isotc211.org/2005/gmd">
                    <MD_Identifier>
                        <code>
                            <gco:CharacterString>doi:10.1234.5678/1234</gco:CharacterString>
                        </code>
                    </MD_Identifier>
                </identifier>
                <gmd:otherCitationDetails>
                    <gco:CharacterString>Other citation details</gco:CharacterString>
                </gmd:otherCitationDetails>
                <onlineResource>
                    <CI_OnlineResource xmlns="http://www.isotc211.org/2005/gmd">
                        <linkage>
                            <URL>https://www.example.com/</URL>
                        </linkage>
                    </CI_OnlineResource>
                </onlineResource>
            </Citation>
        </documentation>
        <capabilities>
            <processCapability>
                <name>Signal Strength</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <units xlink:href="https://metadata.pithia.eu/ontology/2.2/unit/dB"/> 
            </processCapability>
            <processCapability>
                <name>Signal Polarization</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Doppler Frequency</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Angle of Arrival</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction"/> 
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <!-- <crs xlink:href="https://metadata.pithia.eu/ontology/2.2/crs/Az-Zenith"/> -->
            </processCapability>
        </capabilities>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
            <metadataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual" />
        <version>934</version>
        <softwareReference>
            <Citation>
                <gmd:title>
                    <gco:CharacterString>Software Reference Title</gco:CharacterString>
                </gmd:title>
                <gmd:date>
                    <gmd:CI_Date>
                        <gmd:date>
                            <gco:Date>2024-08-01</gco:Date>
                        </gmd:date>
                        <gmd:dateType>
                            <gmd:CI_DateTypeCode codeList="" codeListValue="">Publication Date</gmd:CI_DateTypeCode>
                        </gmd:dateType>
                    </gmd:CI_Date>
                </gmd:date>
                <gmd:identifier>
                    <gmd:MD_Identifier>
                        <gmd:code>
                            <gco:CharacterString>doi:10.123456/4321</gco:CharacterString>
                        </gmd:code>
                    </gmd:MD_Identifier>
                </gmd:identifier>
                <gmd:otherCitationDetails>
                    <gco:CharacterString>Software reference full citation</gco:CharacterString>
                </gmd:otherCitationDetails>
                <onlineResource>
                    <gmd:CI_OnlineResource>
                        <gmd:linkage>
                            <gmd:URL>https://github.com/pithia-eu/pithia-esc-gui-poc/blob/main/docs/development.md</gmd:URL>
                        </gmd:linkage>
                    </gmd:CI_OnlineResource>
                </onlineResource>
            </Citation>
        </softwareReference>
        <processingInput>
            <InputOutput>
                <name>Processing input 1</name>
                <description>
                    <mrl:LE_Source>
                        <mrl:description>
                            <gco19115:CharacterString>Description of processing input 1</gco19115:CharacterString>
                        </mrl:description>
                    </mrl:LE_Source>
                </description>
            </InputOutput>
        </processingInput>
        <processingInput>
            <InputOutput>
                <name>Processing input 4</name>
                <description>
                    <mrl:LE_Source>
                        <mrl:description>
                            <gco19115:CharacterString>Description of processing input 4</gco19115:CharacterString>
                        </mrl:description>
                    </mrl:LE_Source>
                </description>
            </InputOutput>
        </processingInput>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PrincipalInvestigator"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/ingv/Individual_INGV_Pica"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/Director"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/noa/Individual_NOA_Belehaki"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/kul/ComputationCapabilities_KUL_EUHFORIA_Heliosphere"/>
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/kul/ComputationCapabilities_KUL_EUHFORIA_Corona"/>
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_Radiolink_MidpointCalculation"/>
        <childComputation xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/oe/ComputationCapabilities_hmF2_qModel"/>
        <softwareReference />
        <processingInput />
        <algorithm />
    </ComputationCapabilities>
    '''
)


# COMPUTATIONS
COMPUTATION_METADATA_XML = SimpleUploadedFile(
    'Computation_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Computation
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <identifier>
            <PITHIA_Identifier>
                <localID>Computation_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-28T10:00:00Z</creationDate>
                <lastModificationDate>2022-02-28T10:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Computation Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Non diam phasellus vestibulum lorem sed risus. Aliquet nibh praesent tristique magna sit amet purus.
            Rutrum quisque non tellus orci ac auctor augue. Sit amet nisl purus in mollis nunc sed id.
        </description>
        <capabilityLinks>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <computationCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test" />
            </capabilityLink>
            <capabilityLink>
                <platform
                    xlink:href="https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test" />
                <standardIdentifier authority="URSI">AT138</standardIdentifier>
                <computationCapabilities
                    xlink:href="https://metadata.pithia.eu/resources/2.2/computationCapabilities/test/ComputationCapabilities_Test" />
            </capabilityLink>
        </capabilityLinks>
    </Computation>
    '''
)


# PROCESSES
PROCESS_METADATA_XML = SimpleUploadedFile(
    'CompositeProcess_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <CompositeProcess 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >
        <!-- Instructions:
    This is a composite process that includes all data acquisitions and data computations involved in a single Observation. 
    1. If ObservationCollection is a model computation, acquisitionComponent is not defined
    2. Input parameters for the model or measurement are not listed here, they are in ObservationCollection
    3. ProcessCapability items are all-inclusive... everything that included computationComponents can potentially produce are listed here
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>CompositeProcess_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-13T14:30:00Z</creationDate>
                <lastModificationDate>2022-03-13T14:30:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Composite Process Test</name>  
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2A"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ2"/>
        </qualityAssessment>

        <!-- describe the Composite Process from which components is consisted of. You can put more than one computationComponent and more than one acquisitionComponent -->
        <acquisitionComponent xlink:href="https://metadata.pithia.eu/resources/2.2/acquisition/test/Acquisition_Test"/>
        <computationComponent xlink:href="https://metadata.pithia.eu/resources/2.2/computation/test/Computation_Test"/>
        
    </CompositeProcess>
    '''
)

PROCESS_FULL_METADATA_XML = SimpleUploadedFile(
    'CompositeProcess_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <CompositeProcess 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:gco="http://www.isotc211.org/2005/gco"
        xmlns:gco19115="http://standards.iso.org/iso/19115/-3/gco/1.0"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:xlink="http://www.w3.org/1999/xlink" >
        <!-- Instructions:
    This is a composite process that includes all data acquisitions and data computations involved in a single Observation. 
    1. If ObservationCollection is a model computation, acquisitionComponent is not defined
    2. Input parameters for the model or measurement are not listed here, they are in ObservationCollection
    3. ProcessCapability items are all-inclusive... everything that included computationComponents can potentially produce are listed here
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>CompositeProcess_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-13T14:30:00Z</creationDate>
                <lastModificationDate>2022-03-13T14:30:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Composite Process Test</name>  
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <documentation>
            <Citation>
                <gmd:title>
                    <gco:CharacterString>Documentation title</gco:CharacterString>
                </gmd:title>
                <date xmlns="http://www.isotc211.org/2005/gmd">
                    <CI_Date>
                        <date>
                            <gco:Date>2024-08-01</gco:Date>
                        </date>
                        <dateType>
                            <CI_DateTypeCode codeList="" codeListValue="">Publication Date</CI_DateTypeCode>
                        </dateType>
                    </CI_Date>
                </date>
                <identifier xmlns="http://www.isotc211.org/2005/gmd">
                    <MD_Identifier>
                        <code>
                            <gco:CharacterString>doi:10.1234.5678/1234</gco:CharacterString>
                        </code>
                    </MD_Identifier>
                </identifier>
                <gmd:otherCitationDetails>
                    <gco:CharacterString>Other citation details</gco:CharacterString>
                </gmd:otherCitationDetails>
                <onlineResource>
                    <CI_OnlineResource xmlns="http://www.isotc211.org/2005/gmd">
                        <linkage>
                            <URL>https://www.example.com/</URL>
                        </linkage>
                    </CI_OnlineResource>
                </onlineResource>
            </Citation>
        </documentation>
        <capabilities>
            <processCapability>
                <name>Signal Strength</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <units xlink:href="https://metadata.pithia.eu/ontology/2.2/unit/dB"/> 
            </processCapability>
            <processCapability>
                <name>Signal Polarization</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Doppler Frequency</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift"/>
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
            </processCapability>
            <processCapability>
                <name>Signal Angle of Arrival</name>
                <observedProperty xlink:href="https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction"/> 
                <dimensionalityInstance xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityInstance/2DImageIonogram"/>
                <dimensionalityTimeline xlink:href="https://metadata.pithia.eu/ontology/2.2/dimensionalityTimeline/2DAnimation"/>
                <!-- <crs xlink:href="https://metadata.pithia.eu/ontology/2.2/crs/Az-Zenith"/> -->
            </processCapability>
        </capabilities>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
            <metadataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PrincipalInvestigator"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/ingv/Individual_INGV_Pica"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/Director"/>
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/noa/Individual_NOA_Belehaki"/>
            </ResponsiblePartyInfo>
        </relatedParty>

        <!-- describe the Composite Process from which components is consisted of. You can put more than one computationComponent and more than one acquisitionComponent -->
        <acquisitionComponent xlink:href="https://metadata.pithia.eu/resources/2.2/acquisition/test/Acquisition_Test"/>
        <computationComponent xlink:href="https://metadata.pithia.eu/resources/2.2/computation/test/Computation_Test"/>
        
    </CompositeProcess>
    '''
)


# DATA COLLECTIONS
DATA_COLLECTION_METADATA_XML = SimpleUploadedFile(
    'DataCollection_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <DataCollection 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:om="http://www.opengis.net/om/2.0" >
        <!--
            First report some required elements from ISO standard for Observation
        -->
        <om:phenomenonTime/><!-- DO NOT USE, we report phenomenon time only in Catalogs -->
        <om:resultTime/>    <!-- DO NOT USE, we report result time only in Catalogs -->
        <om:procedure xlink:href="https://metadata.pithia.eu/resources/2.2/process/test/CompositeProcess_Test"/>
        <om:observedProperty/> <!-- DO NOT USE, we define all observed properties in the Procedure above -->
        <om:featureOfInterest>
            <FeatureOfInterest>
                <namedRegion xlink:href="https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_F-Region_Bottomside"/>
                <namedRegion xlink:href="https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_E-Region"/>
            </FeatureOfInterest>
        </om:featureOfInterest>
        <om:result/> <!-- DO NOT USE, we use the CollectionResults below to specify URLs to provider) -->
        <!--
            Now our Data Collection elements next
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>DataCollection_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-28T15:00:00Z</creationDate>
                <lastModificationDate>2022-05-17T05:30:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>DataCollection Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder"/>
        <project xlink:href="https://metadata.pithia.eu/resources/2.2/project/test/Project_Test"/>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <collectionResults>
            <source>
                <OnlineResource>
                    <!-- The function performed by the online resource is the landing page for the collection provider-->
                    <serviceFunction xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download"/> <!-- use the serviceFunction vocabulary -->
                    <linkage><gmd:URL>https://giro.uml.edu/didbase/</gmd:URL></linkage>
                    <name>Online Resource 1</name>
                    <protocol>HTTPS</protocol>
                    <description>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                        labore et dolore magna aliqua.
                    </description>
                    <dataFormat xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/image-png"/>
                </OnlineResource>
            </source>        
            <source>
                <OnlineResource>
                    <!-- The function performed by the online resource is the landing page for the collection provider-->
                    <serviceFunction xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download"/> <!-- use the serviceFunction vocabulary -->
                    <linkage><gmd:URL>https://ulcar.uml.edu/SAO-X/</gmd:URL></linkage>
                    <name>Online Resource 2</name>
                    <protocol>HTTPS</protocol>
                    <description>
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco
                        laboris nisi ut aliquip ex ea commodo consequat.
                    </description>
                    <dataFormat xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-html"/>
                </OnlineResource>
            </source>        
            <source>
                <OnlineResource>
                    <!-- The function performed by the online resource is the landing page for the collection provider-->
                    <serviceFunction xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download"/> <!-- use the serviceFunction vocabulary -->
                    <linkage><gmd:URL>https://giro.uml.edu/didbase/scaled.php</gmd:URL></linkage>
                    <name>Online Resource 3</name>
                    <protocol>HTTPS</protocol>
                    <description>
                        Duis aute irure dolor in reprehenderit in
                        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
                        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                    </description>
                    <dataFormat xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-plain"/>
                </OnlineResource>
            </source>        
        </collectionResults>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L0"/>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2A"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ2"/>
        </qualityAssessment>
        <permission xlink:href="https://metadata.pithia.eu/ontology/2.2/licence/LGDC_SpaceDataPolicies"/>
    </DataCollection>
    '''
)

DATA_COLLECTION_WITH_ORG_AS_FIRST_RP_METADATA_XML = SimpleUploadedFile(
    'DataCollection_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <DataCollection 
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" 
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:om="http://www.opengis.net/om/2.0" >
        <!--
            First report some required elements from ISO standard for Observation
        -->
        <om:phenomenonTime/><!-- DO NOT USE, we report phenomenon time only in Catalogs -->
        <om:resultTime/>    <!-- DO NOT USE, we report result time only in Catalogs -->
        <om:procedure xlink:href="https://metadata.pithia.eu/resources/2.2/process/test/CompositeProcess_Test"/>
        <om:observedProperty/> <!-- DO NOT USE, we define all observed properties in the Procedure above -->
        <om:featureOfInterest>
            <FeatureOfInterest>
                <namedRegion xlink:href="https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_F-Region_Bottomside"/>
                <namedRegion xlink:href="https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_E-Region"/>
            </FeatureOfInterest>
        </om:featureOfInterest>
        <om:result/> <!-- DO NOT USE, we use the CollectionResults below to specify URLs to provider) -->
        <!--
            Now our Data Collection elements next
        -->
        <identifier>
            <PITHIA_Identifier>
                <localID>DataCollection_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-02-28T15:00:00Z</creationDate>
                <lastModificationDate>2022-05-17T05:30:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>DataCollection Test</name>
        <description>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
            non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </description>
        <type xlink:href="https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder"/>
        <project xlink:href="https://metadata.pithia.eu/resources/2.2/project/test/Project_Test"/>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <relatedParty>
            <ResponsiblePartyInfo>
                <role xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact"/> 
                <party xlink:href="https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test"/>
            </ResponsiblePartyInfo>
        </relatedParty>
        <collectionResults>
            <source>
                <OnlineResource>
                    <!-- The function performed by the online resource is the landing page for the collection provider-->
                    <serviceFunction xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download"/> <!-- use the serviceFunction vocabulary -->
                    <linkage><gmd:URL>https://giro.uml.edu/didbase/</gmd:URL></linkage>
                    <name>Online Resource 1</name>
                    <protocol>HTTPS</protocol>
                    <description>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                        labore et dolore magna aliqua.
                    </description>
                    <dataFormat xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/image-png"/>
                </OnlineResource>
            </source>        
            <source>
                <OnlineResource>
                    <!-- The function performed by the online resource is the landing page for the collection provider-->
                    <serviceFunction xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download"/> <!-- use the serviceFunction vocabulary -->
                    <linkage><gmd:URL>https://ulcar.uml.edu/SAO-X/</gmd:URL></linkage>
                    <name>Online Resource 2</name>
                    <protocol>HTTPS</protocol>
                    <description>
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco
                        laboris nisi ut aliquip ex ea commodo consequat.
                    </description>
                    <dataFormat xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-html"/>
                </OnlineResource>
            </source>        
            <source>
                <OnlineResource>
                    <!-- The function performed by the online resource is the landing page for the collection provider-->
                    <serviceFunction xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download"/> <!-- use the serviceFunction vocabulary -->
                    <linkage><gmd:URL>https://giro.uml.edu/didbase/scaled.php</gmd:URL></linkage>
                    <name>Online Resource 3</name>
                    <protocol>HTTPS</protocol>
                    <description>
                        Duis aute irure dolor in reprehenderit in
                        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
                        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                    </description>
                    <dataFormat xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-plain"/>
                </OnlineResource>
            </source>        
        </collectionResults>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L0"/>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L1"/>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2A"/>
        <qualityAssessment>
        <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ2"/>
        </qualityAssessment>
        <permission xlink:href="https://metadata.pithia.eu/ontology/2.2/licence/LGDC_SpaceDataPolicies"/>
    </DataCollection>
    '''
)


# CATALOGUES
CATALOGUE_METADATA_XML = SimpleUploadedFile(
    'Catalogue_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Catalogue
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink">

        <identifier>
            <PITHIA_Identifier>
                <localID>Catalogue_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-07-08T09:00:00Z</creationDate>
                <lastModificationDate>2022-07-08T09:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Test</name>
        <description>
            An event list of tests.
        </description>
        <!-- Uncomment the following <catalogueCategory> when the URL becomes available -->
        <!-- <catalogueCategory
        xlink:href="https://metadata.pithia.eu/ontology/2.2/catalogCategory/VolcanoEruption"/> -->
        <!-- Remove the following <catalogCategory> when the above URL becomes available -->
        <catalogueCategory xlink:href="https://metadata.pithia.eu/ontology/2.2/computationType/Model" />
    </Catalogue>
    '''
)


# CATALOGUE ENTRIES
CATALOGUE_ENTRY_METADATA_XML = SimpleUploadedFile(
    'CatalogueEntry_Test_2023-01-01.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <CatalogueEntry
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:om="http://www.opengis.net/om/2.0"
        gml:id="ce1">

        <identifier>
            <PITHIA_Identifier>
                <localID>CatalogueEntry_Test_2023-01-01</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-07-08T09:00:00Z</creationDate>
                <lastModificationDate>2022-07-08T09:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <entryName>Test_2022-01-15</entryName>
        <entryDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
            voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
            cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </entryDescription>
        <catalogueIdentifier
            xlink:href="https://metadata.pithia.eu/resources/2.2/catalogue/test/Test/Catalogue_Test" />
        <phenomenonTime>
            <gml:TimePeriod gml:id="tp1">
                <gml:begin>
                    <gml:TimeInstant gml:id="b1">
                        <gml:timePosition>2022-01-15T04:14:45Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:begin>
                <gml:end>
                    <gml:TimeInstant gml:id="e1">
                        <gml:timePosition>2022-01-15T04:30:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:end>
            </gml:TimePeriod>
        </phenomenonTime>
    </CatalogueEntry>
    '''
)


# CATALOGUE DATA SUBSETS
CATALOGUE_DATA_SUBSET_METADATA_XML = SimpleUploadedFile(
    'DataSubset_Test-2023-01-01_DataCollectionTest.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <DataSubset
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:om="http://www.opengis.net/om/2.0"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:doi="http://www.doi.org/2010/DOISchema"
        gml:id="es1">

        <identifier>
            <PITHIA_Identifier>
                <localID>DataSubset_Test-2023-01-01_DataCollectionTest</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-07-08T09:00:00Z</creationDate>
                <lastModificationDate>2023-02-14T08:34:03Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <entryIdentifier
            xlink:href="https://metadata.pithia.eu/resources/2.2/catalogue/test/Test/CatalogueEntry_Test_2023-01-01" />
        <dataSubsetName>Test</dataSubsetName>
        <dataSubsetDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua.
        </dataSubsetDescription>
        <dataCollection
            xlink:href="https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test" />
        <resultTime>
            <gml:TimePeriod gml:id="tp2">
                <gml:begin>
                    <gml:TimeInstant gml:id="b2">
                        <gml:timePosition>2022-01-14T00:00:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:begin>
                <gml:end>
                    <gml:TimeInstant gml:id="e2">
                        <gml:timePosition>2022-01-16T00:00:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:end>
            </gml:TimePeriod>
        </resultTime>
        <source>
            <OnlineResource>
                <!-- The function performed by the online resource is the landing page for the
                collection
            provider-->
                <serviceFunction
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download" /> <!--
            use the serviceFunction vocabulary -->
                <linkage>
                    <gmd:URL>https://ulcar.uml.edu/SAO-X/</gmd:URL>
                </linkage>
                <name>SAO Explorer for DIDBase ionograms</name>
                <protocol>HTTPS</protocol>
                <description>
                    SAO Explorer is the main visualization and editing tool for ionogram and
                    ionogram-derived
                    data in DIDBase. URL points to the SAO Explorer download, installation and
                    documentation
                    page. IMPORTANT: ONce access to DIDBase is established, retrieval of the relevant
                    data
                    for this subset requires correct selection of (a) station name, (b) time interval
                    (see
                    resultTime above), and (c) the "Manual data only" checkbox.
                </description>
                <dataFormat
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-html" />
            </OnlineResource>
        </source>
        <!-- <doi> -->
            <!-- Bogus data for testing only -->
            <!-- <doi:referentDoiName>10.1000/my-doi</doi:referentDoiName>
            <doi:primaryReferentType>Creation</doi:primaryReferentType>
            <doi:registrationAgencyDoiName>10.1000/ra-5</doi:registrationAgencyDoiName>
            <doi:issueDate>2015-01-07</doi:issueDate>
            <doi:issueNumber>7</doi:issueNumber>
            <doi:referentCreation>
                <doi:name primaryLanguage="en">
                    <doi:value>DIDBase Ionograms</doi:value>
                    <doi:type>Title</doi:type>
                </doi:name>
                <doi:identifier>
                    <doi:nonUriValue>10.5240/B94E-F500-7164-57DB-82F5-6</doi:nonUriValue>
                    <doi:uri returnType="text/html">
                        https://ui.eidr.org/view/content?id=10.5240/B94E-F500-7164-57DB-82F5-6</doi:uri>
                    <doi:uri returnType="application/xml">
                        https://doi.org/10.5240/B94E-F500-7164-57DB-82F5-6</doi:uri>
                    <doi:type>EidrContentID</doi:type>
                </doi:identifier>
                <doi:structuralType>Digital</doi:structuralType>
                <doi:mode>Visual</doi:mode>
                <doi:character>Image</doi:character>
                <doi:type>Dataset</doi:type>
                <doi:principalAgent>
                    <doi:name> -->
                        <!-- <doi:value>Lowell GIRO Data Center</doi:value> -->
                        <!-- <doi:type>Name</doi:type>
                    </doi:name>
                </doi:principalAgent>
            </doi:referentCreation>
        </doi> -->
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
    </DataSubset>
    '''
)

CATALOGUE_DATA_SUBSET_WITH_DOI_METADATA_XML = SimpleUploadedFile(
    'DataSubset_Test-2023-01-01_DataCollectionTest.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <DataSubset
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:om="http://www.opengis.net/om/2.0"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:doi="http://www.doi.org/2010/DOISchema"
        gml:id="es1">

        <identifier>
            <PITHIA_Identifier>
                <localID>DataSubset_Test-2023-01-01_DataCollectionTest</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-07-08T09:00:00Z</creationDate>
                <lastModificationDate>2023-02-14T08:34:03Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <entryIdentifier
            xlink:href="https://metadata.pithia.eu/resources/2.2/catalogue/test/Test/CatalogueEntry_Test-2023-01-01" />
        <dataSubsetName>Test</dataSubsetName>
        <dataSubsetDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua.
        </dataSubsetDescription>
        <dataCollection
            xlink:href="https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test" />
        <resultTime>
            <gml:TimePeriod gml:id="tp2">
                <gml:begin>
                    <gml:TimeInstant gml:id="b2">
                        <gml:timePosition>2022-01-14T00:00:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:begin>
                <gml:end>
                    <gml:TimeInstant gml:id="e2">
                        <gml:timePosition>2022-01-16T00:00:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:end>
            </gml:TimePeriod>
        </resultTime>
        <source>
            <OnlineResource>
                <!-- The function performed by the online resource is the landing page for the
                collection
            provider-->
                <serviceFunction
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download" /> <!--
            use the serviceFunction vocabulary -->
                <linkage>
                    <gmd:URL>https://ulcar.uml.edu/SAO-X/</gmd:URL>
                </linkage>
                <name>SAO Explorer for DIDBase ionograms</name>
                <protocol>HTTPS</protocol>
                <description>
                    SAO Explorer is the main visualization and editing tool for ionogram and
                    ionogram-derived
                    data in DIDBase. URL points to the SAO Explorer download, installation and
                    documentation
                    page. IMPORTANT: ONce access to DIDBase is established, retrieval of the relevant
                    data
                    for this subset requires correct selection of (a) station name, (b) time interval
                    (see
                    resultTime above), and (c) the "Manual data only" checkbox.
                </description>
                <dataFormat
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-html" />
            </OnlineResource>
        </source>
        <doi>
            <!-- Bogus data for testing only -->
            <doi:referentDoiName>10.1000/my-doi</doi:referentDoiName>
            <doi:primaryReferentType>Creation</doi:primaryReferentType>
            <doi:registrationAgencyDoiName>10.1000/ra-5</doi:registrationAgencyDoiName>
            <doi:issueDate>2015-01-07</doi:issueDate>
            <doi:issueNumber>7</doi:issueNumber>
            <doi:referentCreation>
                <doi:name primaryLanguage="en">
                    <doi:value>DIDBase Ionograms</doi:value>
                    <doi:type>Title</doi:type>
                </doi:name>
                <doi:identifier>
                    <doi:nonUriValue>10.5240/B94E-F500-7164-57DB-82F5-6</doi:nonUriValue>
                    <doi:uri returnType="text/html">
                        https://ui.eidr.org/view/content?id=10.5240/B94E-F500-7164-57DB-82F5-6</doi:uri>
                    <doi:uri returnType="application/xml">
                        https://doi.org/10.5240/B94E-F500-7164-57DB-82F5-6</doi:uri>
                    <doi:type>EidrContentID</doi:type>
                </doi:identifier>
                <doi:structuralType>Digital</doi:structuralType>
                <doi:mode>Visual</doi:mode>
                <doi:character>Image</doi:character>
                <doi:type>Dataset</doi:type>
                <doi:principalAgent>
                    <doi:name>
                        <doi:value>Lowell GIRO Data Center</doi:value>
                        <doi:type>Name</doi:type>
                    </doi:name>
                </doi:principalAgent>
            </doi:referentCreation>
        </doi>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
    </DataSubset>
    '''
)

CATALOGUE_DATA_SUBSET_WITH_HANDLE_METADATA_XML = SimpleUploadedFile(
    'DataSubset_Test-2023-01-01_DataCollectionTest.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <DataSubset
        xmlns="https://metadata.pithia.eu/schemas/2.2"
        xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:gml="http://www.opengis.net/gml/3.2"
        xmlns:om="http://www.opengis.net/om/2.0"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:doi="http://www.doi.org/2010/DOISchema"
        gml:id="es1">

        <identifier>
            <PITHIA_Identifier>
                <localID>DataSubset_Test-2023-01-01_DataCollectionTest</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2022-07-08T09:00:00Z</creationDate>
                <lastModificationDate>2023-02-14T08:34:03Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <entryIdentifier
            xlink:href="https://metadata.pithia.eu/resources/2.2/catalogue/test/Test/CatalogueEntry_Test-2023-01-01" />
        <dataSubsetName>Test</dataSubsetName>
        <dataSubsetDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
            labore et dolore magna aliqua.
        </dataSubsetDescription>
        <dataCollection
            xlink:href="https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test" />
        <resultTime>
            <gml:TimePeriod gml:id="tp2">
                <gml:begin>
                    <gml:TimeInstant gml:id="b2">
                        <gml:timePosition>2022-01-14T00:00:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:begin>
                <gml:end>
                    <gml:TimeInstant gml:id="e2">
                        <gml:timePosition>2022-01-16T00:00:00Z</gml:timePosition>
                    </gml:TimeInstant>
                </gml:end>
            </gml:TimePeriod>
        </resultTime>
        <source>
            <OnlineResource>
                <!-- The function performed by the online resource is the landing page for the
                collection
            provider-->
                <serviceFunction
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/serviceFunction/Download" /> <!--
            use the serviceFunction vocabulary -->
                <linkage>
                    <gmd:URL>https://ulcar.uml.edu/SAO-X/</gmd:URL>
                </linkage>
                <name>SAO Explorer for DIDBase ionograms</name>
                <protocol>HTTPS</protocol>
                <description>
                    SAO Explorer is the main visualization and editing tool for ionogram and
                    ionogram-derived
                    data in DIDBase. URL points to the SAO Explorer download, installation and
                    documentation
                    page. IMPORTANT: ONce access to DIDBase is established, retrieval of the relevant
                    data
                    for this subset requires correct selection of (a) station name, (b) time interval
                    (see
                    resultTime above), and (c) the "Manual data only" checkbox.
                </description>
                <dataFormat
                    xlink:href="https://metadata.pithia.eu/ontology/2.2/resultDataFormat/text-html" />
            </OnlineResource>
        </source>
        <doi>
            <!-- Bogus data for testing only -->
            <doi:referentDoiName>21.15112/DATASUBSET_TEST-2023-01-01_DATACOLLECTIONTEST</doi:referentDoiName>
            <doi:primaryReferentType>Creation</doi:primaryReferentType>
            <doi:registrationAgencyDoiName>10.1000/ra-5</doi:registrationAgencyDoiName>
            <doi:issueDate>2015-01-07</doi:issueDate>
            <doi:issueNumber>7</doi:issueNumber>
            <doi:referentCreation>
                <doi:name primaryLanguage="en">
                    <doi:value>DIDBase Ionograms</doi:value>
                    <doi:type>Title</doi:type>
                </doi:name>
                <doi:identifier>
                    <doi:nonUriValue>21.15112/DATASUBSET_TEST-2023-01-01_DATACOLLECTIONTEST</doi:nonUriValue>
                    <doi:uri returnType="text/html">
                        https://ui.eidr.org/view/content?id=21.15112/DATASUBSET_TEST-2023-01-01_DATACOLLECTIONTEST</doi:uri>
                    <doi:uri returnType="application/xml">
                        https://doi.org/21.15112/DATASUBSET_TEST-2023-01-01_DATACOLLECTIONTEST</doi:uri>
                    <doi:type>EidrContentID</doi:type>
                </doi:identifier>
                <doi:structuralType>Digital</doi:structuralType>
                <doi:mode>Visual</doi:mode>
                <doi:character>Image</doi:character>
                <doi:type>Dataset</doi:type>
                <doi:principalAgent>
                    <doi:name>
                        <doi:value>Lowell GIRO Data Center</doi:value>
                        <doi:type>Name</doi:type>
                    </doi:name>
                </doi:principalAgent>
            </doi:referentCreation>
        </doi>
        <dataLevel xlink:href="https://metadata.pithia.eu/ontology/2.2/dataLevel/L2V" />
        <qualityAssessment>
            <dataQualityFlag xlink:href="https://metadata.pithia.eu/ontology/2.2/dataQualityFlag/DQ3" />
        </qualityAssessment>
    </DataSubset>
    '''
)

WORKFLOW_METADATA_XML = SimpleUploadedFile(
    'Workflow_Test.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <Workflow
        xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:xlink="http://www.w3.org/1999/xlink" >

        <identifier>
            <PITHIA_Identifier>
                <localID>Workflow_Test</localID>
                <namespace>test</namespace>
                <version>1</version>
                <creationDate>2023-12-12T09:00:00Z</creationDate>
                <lastModificationDate>2023-12-12T09:00:00Z</lastModificationDate>
            </PITHIA_Identifier>
        </identifier>
        <name>Test Workflow</name>
        <description>
            This is a test workflow with two collections.
        </description>
        <dataCollection xlink:href="https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test" />
        <dataCollection xlink:href="https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test_2" />
        <dataCollection xlink:href="https://metadata.pithia.eu/resources/2.2/collection/test/DataCollection_Test_3" />
        <workflowDetails xlink:href="https://www.example.com/" />
    </Workflow>
    '''
)


# URL Testing
METADATA_AND_ONTOLOGY_URLS_XML = SimpleUploadedFile(
    'valid_and_invalid_urls.xml',
    b'''<?xml version="1.0" encoding="UTF-8"?>
    <urltest xmlns:xlink="http://www.w3.org/1999/xlink">
        <!-- Valid ontology URLs -->
        <url xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider"/>

        <!-- Invalid ontology URLs -->
        <url xlink:href="https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/test"/>

        <!-- Valid resource URLs -->
        <url xlink:hreef="https://metadata.pithia.eu/resources/2.2/process/eiscat/CompositeProcess_EISCAT_Vector_VHF"/>

        <!-- Invalid resource URLs -->
        <url xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_Test"/>
        <url xlink:href="https://metadata.pithia.eu/resources/2.2/individual/pithia/Individual_TEST_Test"/>
        <url xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/pithia/Individual_TEST_Test"/>

        <!-- Invalid resource URLs with operational mode IDs -->
        <url xlink:href="https://metadata.pithia.eu/resources/2.2/collection/pithia/Organisation_Test#Test"/>
        <url xlink:href="https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_Test#Test"/>
    </urltest>
    '''
)