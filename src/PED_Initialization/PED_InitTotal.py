'''
Created on 27 mar. 2018

@author: jomartin

Standalone Python script to simulate CSACT side during H24 PED initialization.

This script will supply all tables to the PED regardless version number, total or partial download.

@version 0.1 (first implementation) 
'''

import re
import os
from PED_Telecharge import *
from PED_Operation import *
from Socket import *
from enum import Enum
from time import strftime
import logging

#Constant to run the mockup as Testmode.
TESTMODE = 0

def loginit():
	logfolder = r'.\LOGS'
	if not os.path.exists(logfolder): 
		os.makedirs(logfolder)
	logfile = '.\\LOGS\\{0}{1}.LOG'.format(date.today().strftime("%Y%m%d"), datetime.now().strftime("%H%M"))
	logging.basicConfig(filename=logfile, format='%(asctime)s\t%(funcName)s\t%(lineno)d\t[%(levelname)s]\t%(message)s', datefmt='%Y-%m-%d\t%I:%M:%S', level=logging.INFO)
	logpath = os.getcwd()
	logging.info("The path of the log\t{0}".format(logpath))
	logging.info("The name of the file\t{0}".format(logfile))
	return logpath + logfolder[1:]

def initscript(mylogpath):
	mylocalhost = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
	mylocalport = "4445"
	logoinit = '--------------------------------------------------------------------------------\n  oooooooo8  oooooooo8      o       oooooooo8 ooooooooooo \no888     88 888            888    o888     88 88  888  88 \n888          888oooooo    8  88   888             888                      _   \n888o     oo         888  8oooo88  888o     oo     888 _ __ ___   ___   ___| | __\n 888oooo88  o88oooo888 o88o  o888o 888oooo88     o888o  ''_ ` _ \ / _ \ / __| |/ /\n                                                     | | | | | | (_) | (__|   < \n                                                     |_| |_| |_|\___/ \___|_|\_\\\n--------------------------------------------------------------------------------\n INGENICO Technical Software Department\n--------------------------------------------------------------------------------\n Copyright (c) 2011-2014, INGENICO.\n Av. Partenon num 10, 4ta planta, 28042 Madrid, Espana\n All rights reserved.\n This source program is the property of the INGENICO Company mentioned above\n and may not be copied in any form or by any means, whether in part or in whole,\n except under license expressly granted by such INGENICO company.\n All copies of this source program, whether in part or in whole, and\n whether modified or not, must display this and all other\n embedded copyright and ownership notices in full.\n--------------------------------------------------------------------------------\n Project : \tCSACT Mock for H24 app\n Feature : \tOperations & Tables Initialization \n Date : \t12 Jun 2018 14:08:26\n Author : \tJuan Ignacio Bueno Gallego\n--------------------------------------------------------------------------------\n LocalHost : \t{0}\n Port : \t{1}\n--------------------------------------------------------------------------------\n Log folder : \t{2}\n--------------------------------------------------------------------------------\n Select the project Configuration:\n\t[1] GENERAL.\n\t[2] CEPSA Otorgacion.\n\t[3] CEPSA Tarjetizacion.\n\t[4] Telecarga de SW.\n\t[5] Telecarga tabla Estacion.\n\t[6] Offline Telecharge.\n\t'
	print(logoinit.format(mylocalhost, mylocalport, mylogpath))
	if TESTMODE:
		# Include the test mode text.
		print ("\n\t\t\t ----------------------\n\t\t\t| RUNNING ON TEST MODE |\n\t\t\t ----------------------\n")
	logging.info("The IP address\t{0}".format(mylocalhost))
	logging.info("The PORT\t{0}".format(mylocalport))
	
	
def listen():
	while True:
		try:
			frameSequence = input(" ->Project:")
			int(frameSequence)
		except ValueError:
			print("The input is not valid!, try again:")
			continue
		if int(frameSequence) > 6:
			print("The input is not a valid configuration!, try again:")
			continue
		else:
			if TESTMODE:
				# Run the test configuration tables.
				frameSequence = 6
			frameSequence = Definesecuence(frameSequence)
			frameCount = len(frameSequence)
			break
	framePos = 0
	lSocketExit = 1
	merchantId = ''
	# 1.  Configuracion del Socket.
	connection = SocketHandler()
	if not connection.start(False):
		logging.error("Socket configuration error")
		connection.close()
		exit(ERROR_SOCKET_CONFIGURATION)
	
	connection.server_start()
	print("Starting...")
	while True:
		current_connection, address = connection.accept_socket()
		
		print (" The system is waiting...\n")
		logging.info("The socket has been opened successfully")
		lSocketExit = 0
			
		while not lSocketExit:
			
			data = current_connection.recv(2048)	
			if data:
				# Convert bytes object into string.
				try:
					pedRequest = data.decode('ascii')
				except:
					print(" The trame is ENCRIPTED!!!\n")
					pedRequest = 'PH2400578PDI040099777998220000X0000000#'
				isRequestFrame = re.search(requestTemplate, pedRequest, re.DOTALL)
				isAckFrame = re.search(ackTemplate, pedRequest, re.DOTALL)
				isNackFrame = re.search(nackTemplate, pedRequest, re.DOTALL)
				isOpeRFrame = re.search(OperationTemplate, pedRequest, re.DOTALL)
				print ("[RX] {0}".format(pedRequest))
				logging.info("[RX]\t{0}".format(pedRequest))
				print ("\n") 
				if isRequestFrame:
					# Get Merchant ID from request frame.
					merchantId = pedRequest[33:40]
					# Reset frame position.
					framePos = 0
					# Send response with customized merchantId.
					responseString = frameSequence[framePos].format(merchantId)
					responseData = responseString.encode('ascii')
					current_connection.send( responseData )
					print ("[TX] {0}".format(responseString))
				elif isAckFrame or isNackFrame:
					# Jump to next frame position and send it (if not yet finished)
					if isAckFrame:
						framePos += 1
					if framePos < frameCount:
						responseData = SendTableLine ( frameSequence, framePos, merchantId )
						current_connection.send( responseData )
					elif framePos == frameCount:
						lSocketExit = 1
						print (" Siguiente trama\n")
					else:
						lSocketExit = 0
				elif isOpeRFrame:
					# Response to a normal operation frame. 
					responseData = parseTrame (pedRequest)
					current_connection.send( responseData )
					lSocketExit = 1
				else:
					# Response to a no known petition.
					responseData = NonKnownFrame (pedRequest)
					current_connection.send( responseData )
					# All done, close se socket
					lSocketExit = 1  
				
			print ("\n\n--------------------------------------------------------------------------------\n")
			logging.info("Waiting for a new comunication")

				
if __name__ == "__main__":
	try:
		initscript(loginit())
		listen()
	except KeyboardInterrupt:
		pass


