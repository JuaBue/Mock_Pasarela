'''
Created on 4 jun. 2018

@author: juan.bueno
'''

from TelechargeTables import *
from enum import Enum
import logging

class Config(Enum):
    GENERICO = 0
    CEPSA = 1
    TARJETIZACION = 2 
    TELECARGASW = 3
    TELECARGASTATION = 4
    OFFLINE = 5
    TELECARGATEST = 6  # This line has to be the last one.

    

ProjectTable = [ ( Config.GENERICO, frameSequenceGeneric, "Generic configuration has been loaded") 
               , ( Config.CEPSA, frameSequenceCEPSA, "CEPSA configuration has been loaded")
               , ( Config.TARJETIZACION, frameSequenceTARJETIZACION, "CEPSA Tarjetizacion configuration has been loaded")
               , ( Config.TELECARGASW, frameSequenceTelecargaSW, "SW Telecharge config has been loaded")
               , ( Config.TELECARGASTATION, frameSequenceStationTable, "Station's table with language and currency change config has been loaded.")
               , ( Config.OFFLINE, frameSequenceOffline, "Offline configuration has been loaded." )
               , ( Config.TELECARGATEST, frameSequenceTEST, "Ejecucion en Modo Test....")  # This line has to be the last one.
               ]


def Definesecuence (TypeConfig):
    frameSequence = ProjectTable [int(TypeConfig) - 1][1]
    if ( Config.TELECARGASW.value == (int(TypeConfig)-1)):
        ConfigTelecargaSW()
    print ("\n" + ProjectTable [ int(TypeConfig) - 1][2]) 
    logging.info("{0}".format(ProjectTable [ int(TypeConfig) - 1][2]))
    return frameSequence


def SendTableLine ( frameSequence, framePos, merchantId ):
    responseString = frameSequence[framePos].format(merchantId)
    responseData = responseString.encode('ascii')
    logging.info("[TX]\t{0}".format(responseString))  
    print ("[TX] {0}".format(responseString))
    return responseData    
 
        
def ConfigTelecargaSW ():
    print ("\n\n ------------------------------\n CONFIGURATION MENU [Telecharge]\n ------------------------------\n")
                            

