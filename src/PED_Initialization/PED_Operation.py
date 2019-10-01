"""
Created on 6 jun. 2018

@author: juan.bueno
"""
from datetime import *
from OperationFrames import *
from Parse import *
import logging
from enum import Enum
from time import strftime

LongHeader = 30

def parseTrame (pedRequest):
    bErrorResponse = False
    MyRequest = CParseTrame (pedRequest)

    if MyRequest.ChipData != 'EMV#00':
        ChipTlvTree = 'EMV#8A023030'
    else:
        ChipTlvTree = ''
    # Build the response.
    # -----------------------1
    # Set the date, the time, the last NSM and the operation number.  
    if  bErrorResponse:
        TypeResponse = Trame.ERROR.value
    else:
        (Bin, post) = getfield ( '=', MyRequest.Track2 )
        if Bin[:6] == '510033':
            TypeResponse = Trame.CETELEM.value
        elif (MyRequest.OperationCode == 'PY' or MyRequest.OperationCode == 'PZ') and (int(MyRequest.LastNSM) % 2):
            TypeResponse = Trame.CEPSA_IUN_1.value
        elif (MyRequest.OperationCode == 'PY' or MyRequest.OperationCode == 'PZ') and not (int(MyRequest.LastNSM) % 2):
            TypeResponse = Trame.CEPSA_IUN_2.value
        elif MyRequest.OperationCode == 'PTA':
            TypeResponse = Trame.TOKEN_QUERY.value
        else:
            TypeResponse = Trame.CEPSA_VENTA.value
            
    #Build the trame response.
    DateStampTicket = date.today().strftime("%d/%m/%Y")
    TimeStampTicket = datetime.now().strftime("%H:%M")
    DateResponse = date.today().strftime("%d%m%Y")
    TimeResponse = datetime.now().strftime("%H%M%S")
    #TotalAmount = 0
    TotalAmountTicket = format(float(MyRequest.TotalAmount)/100, ".2f")
    QuantityLitres = 0
    if QuantityLitres:
        QuantityLitresTicket = format(float(QuantityLitres)/100, ".2f")
    else:
        QuantityLitresTicket = "00.00"
    UnitPrice = 0
    UnitPriceTicket = format(float(UnitPrice)/1000, ".3f")
    responseString = OperationTrame [TypeResponse][2].format(DateResponse, TimeResponse, MyRequest.LastNSM, MyRequest.OpNum, ChipTlvTree, DateStampTicket, TimeStampTicket, TotalAmountTicket , UnitPriceTicket, QuantityLitresTicket)
    # Calcule the length of the frame and set to the response.
    longitud = (len(responseString) - LongHeader)                
    responseString = responseString[:4] + format(longitud, "05d") + responseString[9:]
    
    # Send the response.
    # -----------------------
    # Send the response in ascii format and print it to the console. 
    responseData = responseString.encode('ascii')
    logging.info("[TX]\t{0}".format(responseString))
    print ("[TX] {0}".format(responseString))
    return responseData

def getfield (delimeter, string):
    GetField = ""
    Position = 0
    for i in string:
        Position = Position + 1
        if i == delimeter:
            return GetField, Position
        else:
            GetField = GetField + i

def NonKnownFrame (pedRequest):
    #Function to create a response to a non known frame.
        #Get the merchand Id send in the request.
    LastNSM = '000000'
    OpNum = '000000'
    DateStampTicket = date.today().strftime("%d/%m/%Y")
    TimeStampTicket = datetime.now().strftime("%H:%M")
    responseString = OperationTrame [Trame.ERROR.value][2].format( LastNSM, OpNum, DateStampTicket, TimeStampTicket )
    responseString = responseString[:4] + '00095' + responseString[9:]
    responseData = responseString.encode('ascii')
    logging.info("[TX]\t{0}".format(responseString))
    print ("[TX] {0}".format(responseString))
    return responseData
    #TODO: Implementar el encriptado de PUFDI_AesEncrypt para gestionar la respuesta encriptada.
