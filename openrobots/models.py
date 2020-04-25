from django.db import models

from django.contrib.auth.models import User
from . import openrobots_config #OPENROBOTS_TEMPLATE_DIRECTORY, OPENROBOTS_OUTPUT_DIRECTORY
import distutils

class Stations (models.Model):
    stationName = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.stationName)

    def get_station_name(self):
        return '%s' %(self.stationName)


class ModuleType (models.Model):
    moduleType = models.CharField(max_length = 30)
    vendor = models.CharField(max_length = 30)
    description = models.CharField(max_length = 255, null = True, blank = True)
    witePapers = models.FileField(upload_to = openrobots_config.OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY , null = True , blank = True)
    manualGuide = models.FileField(upload_to = openrobots_config.OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY , null = True , blank = True)
    moduleImage = models.FileField(upload_to = openrobots_config.OPENROBOTS_MODULE_TYPE_GUIDES_DIRECTORY , null = True , blank = True)

    def __str__ (self):
        return '%s' %(self.moduleType)

    def get_module_type_name(self):
        return '%s' %(self.moduleType)

    def get_module_vendor(self):
        return '%s' %(self.vendor)

    def get_minimum_module_data(self):
        data = []
        data.append(self.moduleType)
        data.append(self.vendor)
        data.append(self.pk)
        return data

    def get_main_module_data(self):
        data = []
        data.append(self.moduleType)
        data.append(self.vendor)
        data.append(self.description)
        return data

    def get_image(self):
        return '%s' %(self.moduleImage)

    def get_documents (self):
        data = []
        data.append(self.witePapers)
        data.append(self.manualGuide)
        return data

class ModulesInLab (models.Model):
    moduleType = models.ForeignKey(
                        ModuleType,
                        on_delete=models.CASCADE)
    moduleID = models.CharField(max_length = 30)
    description = models.CharField(max_length =255, null = True, blank = True)

    def __str__ (self):
        return '%s_%s' %(self.moduleType ,self.moduleID)

    def get_module_type (self):
        return '%s' %(self.moduleType.get_module_type_name())

    def get_module_type_and_ID (self):
        return '%s_%s' %(self.moduleType ,self.moduleID)

    def get_moduleID (self):
        return '%s' %(self.moduleID)

    def get_module_id (self):
        return '%s' %(self.pk)

class RobotsInventoryManager (models.Manager):

    def create_robot(self, robot_data):
        configuration_obj = Stations.objects.get(stationName__exact = robot_data['configuration'])
        new_robot = self.create( userName = robot_data['userName'], configuration = configuration_obj, location = robot_data['location'],
                robots = robot_data['robots'], serialNumber= robot_data['serialNumber'],
                IP_address = robot_data['IP_address'], hostName= robot_data['hostName'],
                computer_mac = robot_data['computer_mac'], rightPipette= robot_data['rightPipette'], leftPipette = robot_data['leftPipette'],
                rightPipetteID = robot_data['rightPipetteID'], leftPipetteID = robot_data['leftPipetteID'],
                neededPlugs = robot_data['neededPlugs'], observations = robot_data['observations'] )
        return new_robot

class RobotsInventory (models.Model):
    userName = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    configuration = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    modules = models.ManyToManyField(ModulesInLab, blank = True)
    location = models.CharField(max_length = 255)
    robots = models.CharField(max_length = 255)
    serialNumber = models.CharField(max_length = 255)
    IP_address = models.CharField(max_length = 50)
    hostName = models.CharField(max_length = 50)
    computer_mac = models.CharField(max_length = 50)
    rightPipette = models.CharField(max_length = 20, null = True, blank = True)
    leftPipette = models.CharField(max_length = 20, null = True, blank = True)
    rightPipetteID = models.CharField(max_length = 20, null = True, blank = True)
    leftPipetteID = models.CharField(max_length = 255, null = True, blank = True)
    neededPlugs  = models.CharField(max_length = 255, null = True, blank = True)
    observations = models.CharField(max_length = 255, null = True, blank = True)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.robots)

    def get_robot_name (self):
        return '%s' %(self.robots)

    def get_robot_id (self):
        return '%s'  %(self.pk)

    def get_minimum_robot_data(self):
        data = []
        data.append(self.robots)
        data.append(self.location)
        data.append(self.configuration.get_station_name())
        data.append(self.pk)
        return data

    def get_basic_robot_data(self):
        data = []
        data.append(self.robots)
        data.append(self.location)
        data.append(self.configuration.get_station_name())
        data.append(self.serialNumber)
        data.append(self.observations)
        return data

    def get_network_data(self):
        data = []
        data.append(self.IP_address)
        data.append(self.hostName)
        data.append(self.computer_mac)
        return data

    def get_pipette_data(self):
        data = []
        data.append(self.rightPipette)
        data.append(self.rightPipetteID)
        data.append(self.leftPipette)
        data.append(self.leftPipetteID)
        return data

    def get_modules_obj(self):

        return self.modules

    def get_plugs_data(self):
        data = []
        data.append(self.neededPlugs)
        return data

    def set_module(self, module_obj) :
        self.modules.add(module_obj)
        self.save()
        return

    objects = RobotsInventoryManager()

class ProtocolsType (models.Model):
    protocolTypeName = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.protocolTypeName)

    def get_name(self):
        return '%s' %(self.protocolTypeName)

class ProtocolTemplateFilesManager(models.Manager) :
    def create_protocol_template (self, protocol_data):
        protocol_obj = ProtocolsType.objects.get(protocolTypeName__exact = protocol_data['typeOfProtocol'])
        station_obj = Stations.objects.get(stationName__exact = protocol_data['station'])
        new_protocol_template = self.create(userName = protocol_data ['user'],station = station_obj,  typeOfProtocol = protocol_obj,
                    protocolTemplateFileName = protocol_data['file_name'], protocolName = protocol_data['protocolName'],
                    authors= protocol_data['author'], source = protocol_data['source'], apiLevel= protocol_data['apiLevel'],
                    prepareMasterMix = protocol_data['prepare_mastermix'],transferMasterMix= protocol_data['transfer_mastermix'],
                    transferSamples= protocol_data['transfer_samples'])
        return new_protocol_template

class ProtocolTemplateFiles (models.Model):
    userName = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    station = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    typeOfProtocol = models.ForeignKey(
                        ProtocolsType,
                        on_delete=models.CASCADE)
    protocolTemplateFileName = models.FileField(upload_to = openrobots_config.OPENROBOTS_TEMPLATE_DIRECTORY )
    protocolName = models.CharField(max_length = 255)
    authors = models.CharField(max_length = 255)
    source = models.CharField(max_length = 255)
    apiLevel = models.CharField(max_length = 50)
    prepareMasterMix = models.BooleanField(default = False)
    transferMasterMix = models.BooleanField(default = False)
    transferSamples = models.BooleanField(default = False)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.protocolTemplateFileName)

    def get_protocol_file_name(self):
        return '%s' %(self.protocolTemplateFileName)

    def get_protocol_type(self):
        return '%s' %(self.typeOfProtocol.get_name())

    def get_station(self):
        return '%s' %(self.station.get_station_name())

    def get_main_data(self):
        data = []
        data.append(self.id)
        data.append(self.typeOfProtocol.get_name())
        data.append(self.station.get_station_name())
        data.append(self.userName)
        data.append(self.protocolTemplateFileName)
        return data

    def get_metadata(self):
        data = []
        data.append(self.protocolName)
        data.append(self.authors)
        data.append(self.source)
        data.append(self.apiLevel)
        return data

    def get_functions(self):
        data = []
        data.append(self.prepareMasterMix)
        data.append(self.transferMasterMix)
        data.append(self.transferSamples)
        return data

    objects = ProtocolTemplateFilesManager()

class ElutionHardware (models.Model):
    hardwareType = models.CharField(max_length = 80)

    def __str__ (self):
        return '%s' %(self.hardwareType)

    def get_hardware_type(self):
        return '%s' %(self.hardwareType)

class MasterMixType (models.Model):
    MasterMixType = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255, null = True, blank = True )

    def __str__ (self):
        return '%s' %(self.MasterMixType)

    def get_master_mix_type (self):
        return '%s' %(self.MasterMixType)

class MasterMixLabware (models.Model):
    MasterMixLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.MasterMixLabwareType)

    def get_mastermix_labware_type (self):
        return '%s' %(self.MasterMixLabwareType)

class MasterMixTube (models.Model):
    MasterMixTube = models.CharField(max_length = 80)
    MasterMixRadius = models.CharField(max_length = 80)

    def __str__ (self):
        return '%s' %(self.MasterMixTube)
    def get_mastermix_tube (self):
        return '%s' %(self.MasterMixTube)

class PCR_plateLabware (models.Model):
    PCR_plateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.PCR_plateLabwareType)

    def get_pcr_plate_labware_type (self):
        return '%s' %(self.PCR_plateLabwareType)


class MagPlate_Labware(models.Model):
    mag_plateLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.mag_plateLabwareType)


class Elution_LabwareManager(models.Manager):
    def create_elution_labware(self,data):
        elutionhwtype = ElutionHardware.objects.get(hardwareType__exact = data['elutionhwtype'])
        new_elution_labware = self.create( elutionHW_type = elutionhwtype, elution_LabwareType = data['displayName'],
                valueInCode = data['loadName'], brand = data['brand'], category= data['displayCategory'],
                x_dimension = data['xDimension'], y_dimension = data['yDimension'], z_dimension = data['zDimension'],
                num_columns= data['colums'],  num_rows = data['rows'], spacing_col = data['spacing_col'],
                spacing_row = data['spacing_row'], well_depth = data['depth'], well_shape = data['shape'],
                well_volume = data['totalLiquidVolume'], well_diameter = data['diameter'], num_wells = data['num_wells'],
                jsonFile= data['jsonFile'], pythonFile = data['pythonFile'], imageFile = data['imageFile'] )

        return new_elution_labware

class Elution_Labware (models.Model):
    elutionHW_type =  models.ForeignKey (
                        ElutionHardware,
                        on_delete=models.CASCADE, max_length = 80, null = True, blank = True )
    elution_LabwareType = models.CharField(max_length = 80)
    valueInCode = models.CharField(max_length = 255)
    brand = models.CharField(max_length = 80)
    category = models.CharField(max_length = 80)
    x_dimension = models.CharField(max_length = 10)
    y_dimension = models.CharField(max_length = 10)
    z_dimension = models.CharField(max_length = 10)
    num_columns = models.CharField(max_length = 5)
    num_rows = models.CharField(max_length = 5)
    num_wells = models.CharField(max_length = 5)
    spacing_col = models.CharField(max_length = 10)
    spacing_row = models.CharField(max_length = 10)
    well_depth = models.CharField(max_length = 5)
    well_shape = models.CharField(max_length = 20)
    well_volume = models.CharField(max_length = 10)
    well_diameter = models.CharField(max_length = 10)
    jsonFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_LABWARE_JSON_DIRECTORY , null = True, blank = True, max_length=200)
    pythonFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_LABWARE_PYTHON_DIRECTORY, null = True, blank = True ,max_length=200 )
    imageFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_LABWARE_IMAGE_DIRECTORY, null = True, blank = True ,max_length=200)
    generatedat = models.DateTimeField(auto_now_add=True)


    def __str__ (self):
        return '%s' %(self.elution_LabwareType)

    def get_elution_labware_type (self):
        return '%s' %(self.elution_LabwareType)

    def get_minimun_elution_lab_data (self):
        data = []
        data.append(self.elution_LabwareType)
        data.append(self.brand)
        data.append(self.category)
        data.append(self.num_wells)
        data.append(self.pk)
        return data

    def get_basic_labware_data(self):
        data = []
        data.append(self.elutionHW_type.get_hardware_type())
        data.append(self.brand)
        data.append(self.category)
        return data

    def get_image(self):
        return '%s' %(self.imageFile)

    def get_files(self):
        data = []
        data.append(self.jsonFile)
        data.append(self.pythonFile)
        return data

    def get_plate_data(self):
        data = []
        data.append(self.num_columns)
        data.append(self.num_rows)
        data.append(self.num_columns)
        data.append(self.x_dimension)
        data.append(self.y_dimension)
        data.append(self.z_dimension)
        return data

    def get_well_data(self):
        data = []
        data.append(self.well_volume)
        data.append(self.well_shape)
        data.append(self.well_diameter)
        data.append(self.well_depth)
        data.append(self.spacing_row)
        data.append(self.spacing_col)
        return data

    objects = Elution_LabwareManager()

class Reagent_Labware(models.Model):
    reagentLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.reagentLabwareType)

class Waste_Labware(models.Model):
    wasteLabwareType = models.CharField(max_length = 80)
    description = models.CharField(max_length = 255)

    def __str__ (self):
        return '%s' %(self.wasteLabwareType)

class RequestForStationCManager(models.Manager):

    def create_new_request (self, request_data):

        masterMixLabware = MasterMixLabware.objects.get(MasterMixLabwareType__exact = request_data['masterMixLabware'])
        masterMixTubeLabware = MasterMixTube.objects.get(MasterMixTube__exact = request_data['masterMixTubeLabware'])
        pcrPlateLabware = PCR_plateLabware.objects.get(PCR_plateLabwareType__exact = request_data['pcrPlateLabware'])
        masterMixType = MasterMixType.objects.get(MasterMixType__exact = request_data['masterMixType'])
        elutionLabware = Elution_Labware.objects.get(elution_LabwareType__exact = request_data['elutionLabware'])
        station = Stations.objects.get(stationName__exact = request_data['station'])
        usedTemplateFile = ProtocolTemplateFiles.objects.get(protocolTemplateFileName__exact = request_data['usedTemplateFile'])

        new_request = self.create(userRequestedBy = request_data['userRequestedBy'], masterMixLabware = masterMixLabware , masterMixTubeLabware = masterMixTubeLabware,
                    pcrPlateLabware = pcrPlateLabware, elutionLabware = elutionLabware, masterMixType = masterMixType, station = station,
                    usedTemplateFile = usedTemplateFile, requestedCodeID = request_data['requestedCodeID'], numberOfSamples = request_data['numberOfSamples'],
                    prepareMastermix = distutils.util.strtobool(request_data['prepareMastermix']),
                    transferMastermix = distutils.util.strtobool(request_data['transferMastermix']),
                    transferSamples = distutils.util.strtobool(request_data['transferSamples']),
                    generatedFile = request_data['generatedFile'] , userNotes = request_data['userNotes'])

        return new_request

class RequestForStationB (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    elutionLabware = models.ForeignKey (
                        Elution_Labware,
                        on_delete=models.CASCADE)
    magPlateLabware = models.ForeignKey (
                        MagPlate_Labware,
                        on_delete=models.CASCADE)
    reagentLabware = models.ForeignKey (
                        Reagent_Labware,
                        on_delete=models.CASCADE)
    wasteLabware = models.ForeignKey (
                        Waste_Labware,
                        on_delete=models.CASCADE)
    requestedCodeID = models.CharField(max_length = 50)
    numberOfSamples = models.CharField(max_length = 10)
    tipTrack = models.BooleanField()
    dispenseBeads = models.BooleanField()

    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)


class RequestForStationC (models.Model):
    userRequestedBy = models.ForeignKey (
                        User,
                        on_delete=models.CASCADE, null = True, blank = True )
    masterMixLabware = models.ForeignKey (
                        MasterMixLabware,
                        on_delete=models.CASCADE)
    masterMixTubeLabware = models.ForeignKey (
                        MasterMixTube,
                        on_delete=models.CASCADE)
    pcrPlateLabware = models.ForeignKey (
                        PCR_plateLabware,
                        on_delete=models.CASCADE)
    elutionLabware = models.ForeignKey (
                        Elution_Labware,
                        on_delete=models.CASCADE)
    masterMixType = models.ForeignKey (
                        MasterMixType,
                        on_delete=models.CASCADE)
    station = models.ForeignKey(
                        Stations,
                        on_delete=models.CASCADE)
    usedTemplateFile = models.ForeignKey(
                        ProtocolTemplateFiles,
                        on_delete=models.CASCADE)
    requestedCodeID = models.CharField(max_length = 50)
    numberOfSamples = models.CharField(max_length = 10)
    prepareMastermix = models.BooleanField()
    transferMastermix = models.BooleanField()
    transferSamples = models.BooleanField()

    generatedFile = models.FileField(upload_to = openrobots_config.OPENROBOTS_OUTPUT_DIRECTORY )
    userNotes = models.CharField(max_length = 255)
    generatedat = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return '%s' %(self.requestedCodeID)

    def get_result_data(self):
        data = []
        data.append(self.requestedCodeID)
        data.append(self.usedTemplateFile.get_protocol_type())
        data.append(self.station.get_station_name())
        data.append(self.generatedFile)
        return data

    objects = RequestForStationCManager()