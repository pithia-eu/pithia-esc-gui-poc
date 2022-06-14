from mongodb import db

def CurrentOrganisation():
    return db['current-organisations']

def CurrentIndividual():
    return db['current-individuals']

def CurrentProject():
    return db['current-projects']

def CurrentPlatform():
    return db['current-platforms']

def CurrentInstrument():
    return db['current-instruments']

def CurrentOperation():
    return db['current-operations']

def CurrentAcquisition():
    return db['current-acquisitions']

def CurrentComputation():
    return db['current-computations']

def CurrentProcess():
    return db['current-processes']

def CurrentDataCollection():
    return db['current-data-collections']

def OrganisationRevision():
    return db['organisation-revisions']

def IndividualRevision():
    return db['individual-revisions']

def ProjectRevision():
    return db['project-revisions']

def PlatformRevision():
    return db['platform-revisions']

def InstrumentRevision():
    return db['instrument-revisions']

def OperationRevision():
    return db['operation-revisions']

def AcquisitionRevision():
    return db['acquisition-revisions']

def ComputationRevision():
    return db['computation-revisions']

def ProcessRevision():
    return db['processe-revisions']

def DataCollectionRevision():
    return db['data-collection-revisions']