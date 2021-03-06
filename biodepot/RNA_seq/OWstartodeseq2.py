import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from orangebiodepot.util.DockerClient import DockerClient
from orangebiodepot.util.BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements
from PyQt5 import QtWidgets, QtGui

class OWStartoDESeq2(OWBwBWidget):
    name = "Star to DESeq2"
    description = "Convert Star quantMode counts file to DESeq2 style counts file"
    category = "RNA-seq"
    priority = 10
    icon = "/biodepot/RNA_seq/icons/startodeseq2.png"
    want_main_area = False
    docker_image_name = "biodepot/star2deseq"
    docker_image_tag = "1.0-alpine-3.7"
    inputs = [("outputDirs",str,"handleInputsoutputDirs"),("inputDirs",str,"handleInputsinputDirs"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("outputFile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    outputFile=pset("DESeqCounts.tsv")
    inputFile=pset("ReadsPerGene.out.tab")
    column=pset(4)
    inputDirs=pset([])
    outputDirs=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open("/biodepot/RNA_seq/json/startodeseq2.json") as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsoutputDirs(self, value, sourceId=None):
        self.handleInputs(value, "outputDirs", sourceId=None)
    def handleInputsinputDirs(self, value, sourceId=None):
        self.handleInputs(value, "inputDirs", sourceId=None)
    def handleInputsTrigger(self, value, sourceId=None):
        self.handleInputs(value, "Trigger", sourceId=None)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
