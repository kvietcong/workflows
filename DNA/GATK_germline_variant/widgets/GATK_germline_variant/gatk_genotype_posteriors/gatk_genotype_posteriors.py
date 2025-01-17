import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWgatk_genotype_posteriors(OWBwBWidget):
    name = "gatk_genotype_posteriors"
    description = "Base quality recalibration using GATK"
    priority = 40
    icon = getIconName(__file__,"gatk-genotypePosteriors.png")
    want_main_area = False
    docker_image_name = "biodepot/gatk"
    docker_image_tag = "4.1.9.0__f5684bf4"
    inputs = [("inputfiles",str,"handleInputsinputfiles"),("output",str,"handleInputsoutput"),("supportTrigger",str,"handleInputssupportTrigger")]
    outputs = [("output",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    supportfiles=pset([])
    inputfile=pset(None)
    output=pset(None)
    regions=pset(None)
    pedfile=pset(None)
    skipfamily=pset(False)
    skippopulation=pset(False)
    skipindels=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"gatk_genotype_posteriors")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputfiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputfiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutput(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("output", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssupportTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("supportTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"output"):
            outputValue=getattr(self,"output")
        self.send("output", outputValue)
