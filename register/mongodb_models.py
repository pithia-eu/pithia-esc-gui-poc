from mongodb import db

CurrentOrganisation = db['current-organisations']
CurrentIndividual = db['current-individuals']
CurrentProject = db['current-projects']
CurrentPlatform = db['current-platforms']
CurrentInstrument = db['current-instruments']
CurrentOperation = db['current-operations']
CurrentAcquisition = db['current-acquisitions']
CurrentComputation = db['current-computations']
CurrentProcess = db['current-processes']
CurrentDataCollection = db['current-data-collections']

OrganisationRevision = db['organisation-revisions']
IndividualRevision = db['individual-revisions']
ProjectRevision = db['project-revisions']
PlatformRevision = db['platform-revisions']
InstrumentRevision = db['instrument-revisions']
OperationRevision = db['operation-revisions']
AcquisitionRevision = db['acquisition-revisions']
ComputationRevision = db['computation-revisions']
ProcessRevision = db['processe-revisions']
DataCollectionRevision = db['data-collection-revisions']