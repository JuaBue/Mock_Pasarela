"""
Created on 28 ago. 2018

@author: juan.bueno
"""
import logging

LongHeader = 30

class CParseTrame:

    def __init__(self, request ):
        self.bErrorResponse = False
        self.TrameToParse = request
        self.ParsePos = LongHeader
        self.LastNSM = 0
        self.OpNum = 0
        # Start the proccesing to parse.
        (self.HeaderTrame, self.bErrorResponse ) = self.pt_parseheader()
        # Parse the field �Type of Request�
        (self.TypeRequest, self.bErrorResponse ) = self.pt_typerequest()
        # Parse the field �Business ID�
        (self.Merchant, self.bErrorResponse ) = self.pt_businessID()
        # Parse the field �Type of machine�
        (self.TypeMachine, self.bErrorResponse ) = self.pt_typemachine()
        # Parse the ID of the Terminal
        (self.IdTerminal, self.bErrorResponse ) = self.pt_idterminal()
        # Parse the version of the tables stored in the PED.
        (self.TableVersion, self.bErrorResponse ) = self.pt_tableversion()
        # Parse the Last NSM.
        (self.LastNSM, self.bErrorResponse ) = self.pt_lastNSM()
        # Parse the Operation number.
        (self.OpNum, self.bErrorResponse ) = self.pt_operationNum()
        # Parse the Offline Transaction numbrer.
        (self.OffTrans, self.bErrorResponse ) = self.pt_offlinetrans()
        # Parse the Operation mode.
        (self.OpMode, self.bErrorResponse ) = self.pt_operationmode()
        # Parse the Currency of the transaction (ISO 4217).
        (self.Currency, self.bErrorResponse ) = self.pt_currency()
        # Parse the Language of the terminal.
        (self.Languaje, self.bErrorResponse ) = self.pt_lenguaje()
        # Parse the type of card, 1-Swiped 2-EMV
        (self.TypeCard, self.bErrorResponse ) = self.pt_typecard()
        # Parse the trak 1 of the card.
        (self.Track1, self.bErrorResponse ) = self.pt_track1()
        # Parse the trak 2 of the card.
        (self.Track2, self.bErrorResponse ) = self.pt_track2()
        # Parse the fiels related with the card info.
        (self.ExtraDataTarjet, self.bErrorResponse ) = self.pt_extradatacard()
        # Parse the data ralated with the chip.
        (self.ChipData, self.bErrorResponse ) = self.pt_chipdata()
        # Parse the type of card, 1-Cash 2-Card
        (self.TypePayment, self.bErrorResponse ) = self.pt_typepayment()
        # Parse the field indicates to us which operation is
        (self.OperationCode, self.bErrorResponse ) = self.pt_operationcode()
        # Parse the number of products of the transaction.
        (self.NumberProducts, self.bErrorResponse ) = self.pt_numberproducts()
        # Parse the Net Total Amount (including discounts).
        (self.TotalAmount, self.bErrorResponse ) = self.pt_totalamount()
        # Parse the field with 4 whole numbers and 2 decimals.
        (self.EuroLPoint, self.bErrorResponse ) = self.pt_eurolpoint()
        # Parse the product code which is acquired in the transaction
        (self.GiftProCode, self.bErrorResponse ) = self.pt_giftprocode()
        # Parse the Unit price for this product, 7 whole numbers 3 decimals
        (self.UnitPrice, self.bErrorResponse ) = self.pt_unitprice()
        # Parse the Quantity of litres, 4 whole numbers 2 decimals
        (self.QuantityLitres, self.bErrorResponse ) = self.pt_quantitylitres()
        # Parse the total amount per product, 10 whole number characters and 2 decimals.
        (self.Amount, self.bErrorResponse ) = self.pt_amount()
        # Parse field discount with 10 whole numbers 2 decimals
        (self.DiscountProduct, self.bErrorResponse ) = self.pt_discountproduct()
        # Parse the extra data block.
        (self.ExtraDataBlock, self.bErrorResponse ) = self.pt_extradatablock()
        # Parse the encryption key (field not used)
        (self.EncryptionKey, self.bErrorResponse ) = self.pt_encryptionkey()
        # Parse the Communication type.
        (self.CommmunicationType, self.bErrorResponse ) = self.pt_communicationtype()
        # Parse the Operation mode.
        (self.CommissionsBlock, self.bErrorResponse ) = self.pt_commissionsblock()
        # Parse the end delimeter <EM>
        self.bErrorResponse = self.pt_endtrame()

    # Method for parse the Header of the PUFDI request.
    def pt_parseheader (self):
        HeaderTrameParsed = ""
        # Parse the field "PH24"
        HProVer = self.TrameToParse[0:4]
        if HProVer == 'PH24':
            HeaderTrameParsed = HeaderTrameParsed + HProVer
        else:
            self.bErrorResponse = True
        # Parse the field �length�
        HLength = self.TrameToParse[4:9]
        try:
            if HLength.isdigit() and (int(HLength) > 0) and (self.TrameToParse[(int(HLength) + 29)] == ""):
                HeaderTrameParsed = HeaderTrameParsed + HLength
            else:
                self.bErrorResponse = True
        except IndexError:
            self.bErrorResponse = True
        # Parse the field �Type of message id�
        HTypeId = self.TrameToParse[9:12]
        if HTypeId == "PDI" or HTypeId == "PPL" or HTypeId == "PTD":
            HeaderTrameParsed = HeaderTrameParsed + HTypeId
        else:
            self.bErrorResponse = True
        # Parse the field �Protocol Version�
        ProtoVersion = self.TrameToParse[12:16]
        if ProtoVersion.isdigit() and (int(ProtoVersion) > 0) and ( (ProtoVersion == "0400") or (ProtoVersion == "0300") or (ProtoVersion == "0200")):
            HeaderTrameParsed = HeaderTrameParsed + ProtoVersion
        else:
            self.bErrorResponse = True
        # Parse the field �Message id�
        IdMessage = self.TrameToParse[16:27]
        if ProtoVersion.isdigit():
            HeaderTrameParsed = HeaderTrameParsed + IdMessage
        else:
            self.bErrorResponse = True
        # Parse the field �Error code�
        ErrorCode = self.TrameToParse[27:30]
        if ErrorCode == "000":
            HeaderTrameParsed = HeaderTrameParsed + ErrorCode
        else:
            self.bErrorResponse = True

        logging.info("Header of frame\t{0}".format(HeaderTrameParsed))
        if self.bErrorResponse:
            return "PH2400000PDI040000000009260000", self.bErrorResponse
        else:
            return HeaderTrameParsed, self.bErrorResponse

    # Method for parse the field "Type of Request"
    def pt_typerequest (self):
        (TypeRequest, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        logging.info("Type of Request\t{0}".format(TypeRequest))
        if (TypeRequest != "M") and (TypeRequest != "R") and (TypeRequest != "D"):
            self.bErrorResponse = True
            logging.error("Type of Request bad format")
        else:
            self.ParsePos = self.ParsePos + post
        return TypeRequest, self.bErrorResponse

    # Method for parse the field "Business ID"
    def pt_businessID (self):
        (Merchant, post) = self.__pt_getfield ( '#', self.TrameToParse[self.ParsePos:] )
        logging.info("Business ID\t{0}".format(Merchant))
        if ( not Merchant.isdigit()) or Merchant == "0000000" :
            self.bErrorResponse = True
            logging.error("Business ID bad format")
        else:
            self.ParsePos = self.ParsePos + post
        return Merchant , self.bErrorResponse

    # Method for parse the field "Type machine"
    def pt_typemachine (self):
        (TypeMachine, post) = self.__pt_getfield ( '#', self.TrameToParse[self.ParsePos:] )
        logging.info("Type of machine\t{0}".format(TypeMachine))
        if TypeMachine not in ['3', '8', '6', 'T', 't']:
            self.bErrorResponse = True
            logging.error("Type of machine bad format")
        else:
            self.ParsePos = self.ParsePos + post
        return TypeMachine, self.bErrorResponse

    # Method for parse the ID of the Terminal.
    def pt_idterminal (self):
        (IdTerminal, post) = self.__pt_getfield ( '#', self.TrameToParse[self.ParsePos:] )
        logging.info("ID of the Terminal\t{0}".format(IdTerminal))
        if IdTerminal == '':
            self.bErrorResponse = True
            logging.error("ID Terminal with bad format")
        else:
            self.ParsePos = self.ParsePos + post
        return IdTerminal, self.bErrorResponse

    # Method for parse the version of the tables stored in the PED.
    def pt_tableversion (self):
        (TableVersion, post) = self.__pt_getfield ( '#',  self.TrameToParse[self.ParsePos:] )
        logging.info("Tables version\t{0}".format(TableVersion))
        if TableVersion == '':
            self.bErrorResponse = True
            logging.error("Trable version are not include")
        else:
            self.ParsePos = self.ParsePos + post
        return TableVersion, self.bErrorResponse

    # Method for parse the Last NSM.
    def pt_lastNSM (self):
        (LastNSM, post) = self.__pt_getfield  ( '#', self.TrameToParse[self.ParsePos:] )
        logging.info("Last NSM\t{0}".format(LastNSM))
        LastNSM = format(int(LastNSM) + 1, "06d")
        if int(LastNSM) <= 0 :
            self.bErrorResponse = True
            logging.error("Last NSM bad format")
        else:
            self.ParsePos = self.ParsePos + post
            self.LastNSM = LastNSM
        return LastNSM, self.bErrorResponse

    # Method for parse the Operation number.
    def pt_operationNum (self):
        (OpNum, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        logging.info("Operation number\t{0}".format(OpNum))
        OpNum = format(int(OpNum), "06d")
        if int(OpNum) < 0 :
            self.bErrorResponse = True
            logging.error("Operation number bad format")
        else:
            self.ParsePos = self.ParsePos + post
            self.OpNum = OpNum
        return OpNum, self.bErrorResponse

    # Method for parse the Offline Transaction numbrer.
    def pt_offlinetrans (self):
        (OffTrans, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        logging.info("Offline Transaction\t{0}".format(OffTrans))
        if ( OffTrans == '' ) or ( len(OffTrans) is not 3 ) :
            self.bErrorResponse = True
            logging.error("Operation number bad format")
        else:
            self.ParsePos = self.ParsePos + post
        return OffTrans, self.bErrorResponse

    # Method for parse the Operation mode.
    def pt_operationmode (self):
        OpModeKey = {'0':'Autonomous', '1':'Unattended', '2':'Polling Attended', '3':'Polling Unattended' }
        (OpMode, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if ( OpMode == '' ) or ( len(OpMode) > 2 ) or ( OpMode not in ['0', '1', '2', '3']):
            self.bErrorResponse = True
            logging.error("Operation mode bad format:\t{0}".format(OpMode))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Operation mode\t{0} - {1}".format(OpMode, OpModeKey[OpMode]))
        return OpMode, self.bErrorResponse

    # Method fot parse the Currency of the transaction (ISO 4217).
    def pt_currency (self):
        CurrencyKey = {'978':'EUR', '840':'USD', '826':'GBP', '756':'CHF' }
        (Currency, post) = self.__pt_getfield ( '#', self.TrameToParse[self.ParsePos:])
        if Currency not in CurrencyKey:
            self.bErrorResponse = True
            logging.error("Currency bad format:\t{0}".format(Currency))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Currency\t{0} - {1}".format(Currency, CurrencyKey[Currency]))
        return Currency, self.bErrorResponse

    # Method for parse the Language of the terminal.
    def pt_lenguaje (self):
        LenguajeKey = {'DA':'Danish', 'DE':'German', 'EL':'Greek', 'EN':'English', 'ES':'Spanish', 'FI':'Finnish', 'FR':'French', 'NL':'Dutch', 'PT':'Portuguese', 'SW':'Swedish' }
        (Languaje, post) = self.__pt_getfield ( '', self.TrameToParse[self.ParsePos:])
        if Languaje not in LenguajeKey:
            self.bErrorResponse = True
            logging.error("Languaje bad format:\t{0}".format(Languaje))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Languaje\t{0} - {1}".format(Languaje, LenguajeKey[Languaje]))
        return Languaje, self.bErrorResponse

    # Method for parse the type of card, 1-Swiped 2-EMV
    def pt_typecard (self):
        TypeCardKey = { '1':'Swiped', '2':'EMV' }
        (TypeCard, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if TypeCard not in TypeCardKey:
            self.bErrorResponse = True
            logging.error("TypeCard bad format\t{0}".format(TypeCard))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("TypeCard\t{0} - {1}".format(TypeCard, TypeCardKey[TypeCard]))
        return TypeCard, self.bErrorResponse

    # Method for parse the trak 1 of the card.
    def pt_track1 (self):
        (Track1, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        logging.info("Track1\t{0}".format(Track1))
        self.ParsePos = self.ParsePos + post
        return Track1, self.bErrorResponse

    # Method for parse the trak 2 of the card.
    def pt_track2 (self):
        (Track2, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        if Track2 == '':
            logging.error("Track2 is empty\t{0}".format(Track2))
        else:
            logging.info("Track2\t{0}".format(Track2))
        self.ParsePos = self.ParsePos + post
        return Track2, self.bErrorResponse

    # Method for parse the fiels related with the card info.
    def pt_extradatacard (self):
        (ExtraDataTarjet, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        logging.info("Card info\t{0}".format(ExtraDataTarjet))
        # TODO: Crear funcion para parsear estos campos.
        self.ParsePos = self.ParsePos + post
        return ExtraDataTarjet, self.bErrorResponse

    # Method for parse the data ralated with the chip.
    def pt_chipdata (self):
        (ChipData, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        logging.info("Chip Data\t{0}".format(ChipData))
        # TODO: Crear funcion para parsear estos campos.
        self.ParsePos = self.ParsePos + post
        return ChipData, self.bErrorResponse

    #  Method to parse the type of card, 1-Cash 2-Card
    def pt_typepayment (self):
        (TypePayment, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if ( TypePayment and TypePayment != '1') and (TypePayment and TypePayment != '2'):
            self.bErrorResponse = True
            logging.error("Type of Payment bad format:\t{0}".format(TypePayment))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Type of Payment\t{0}".format(TypePayment))
        return TypePayment, self.bErrorResponse

    # Method to parse the field indicates to us which operation is
    def pt_operationcode (self):
        OperationCodeKey = { 'V ':'Venta', 'A ':"Anulacion Generica", 'CP':'Consulta Puntos', 'AV':'Anulacion Venta',
                             'BF':'Bonus sale', 'AF':'Bonus redemption', 'RF':'Bonus balance sale',
                             'CF':'Bonus query - CEPSA', 'PAP':'Unattended Preauthorization',
                             'PAC':'Preauthorization confirmation', 'PAN':'Preauthorization cancellation',
                             'AT':'Partial Refund operation', 'APP':'Explicit transaction reversal', 'AP':'Automatic cancellation',
                             'VY':'DCC query'}
        (OperationCode, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if ( OperationCode not in OperationCodeKey ) and ( len(OperationCode) != 3 ):
            self.bErrorResponse = True
            logging.error("Operation Code bad format:\t{0}".format(OperationCode))
        elif OperationCode not in OperationCodeKey:
            self.ParsePos = self.ParsePos + post
            logging.info("Operation Code\t{0}".format(OperationCode))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Operation Code\t{0} - {1}".format(OperationCode, OperationCodeKey[OperationCode]))
        return OperationCode, self.bErrorResponse
        # TODO: Processing the AP and APP operations wiht an annulation code process.

    # Method to parse the number of products of the transaction.
    def pt_numberproducts (self):
        (NumberProducts, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if not NumberProducts.isdigit() and ( len(NumberProducts) != 2):
            self.bErrorResponse = True
            logging.error("Number of products bad format")
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Number of products\t{0}".format(NumberProducts))
        return NumberProducts, self.bErrorResponse

    # Method to parse the Net Total Amount (including discounts).
    def pt_totalamount (self):
        (TotalAmount, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if not TotalAmount.isdigit() or ( int(TotalAmount) < 0 ):
            self.bErrorResponse = True
            logging.error("Total Amount bad format:\t{0}".format(TotalAmount))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Total Amount\t{0}".format(TotalAmount))
        return TotalAmount, self.bErrorResponse

    # Method to parse the field with 4 whole numbers and 2 decimals.
    def pt_eurolpoint (self):
        (EuroLPoint, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        if EuroLPoint and ( not EuroLPoint.isdigit() or ( int(EuroLPoint) < 0 ) ):
            self.bErrorResponse = True
            logging.error("Euro Litres/Point bad format\t{0}".format(EuroLPoint))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Euro Litres/Point\t{0}".format(EuroLPoint))
        return EuroLPoint, self.bErrorResponse

    # Method to parse the product code which is acquired in the transaction.
    def pt_giftprocode (self):
        (GiftProCode, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if GiftProCode and (GiftProCode and not GiftProCode.isdigit() or (int(GiftProCode) < 0)) and (len(GiftProCode) != 6):
            logging.error("Gift Product code bad format:\t{0}".format(GiftProCode))
            self.bErrorResponse = True
        else:
            logging.info("Gift Product code\t{0}".format(GiftProCode))
            self.ParsePos = self.ParsePos + post
        return GiftProCode, self.bErrorResponse

    # Method for parse the Unit price for this product, 7 whole numbers 3 decimals
    def pt_unitprice(self):
        (UnitPrice, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if UnitPrice and ( not UnitPrice.isdigit()):
            self.bErrorResponse = True
            logging.error("Unit Price bad format\t{0}".format(UnitPrice))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Unit Price\t{0}".format(UnitPrice))
        return UnitPrice, self.bErrorResponse

    # Method to parse the Quantity of litres, 4 whole numbers 2 decimals
    def pt_quantitylitres(self):
        (QuantityLitres, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        if QuantityLitres and (not QuantityLitres.isdigit() or (int(QuantityLitres) < 0)):
            self.bErrorResponse = True
            logging.error("Quantity Litres bad format:\t{0}".format(QuantityLitres))
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Quantity Litres\t{0}".format(QuantityLitres))
        return QuantityLitres, self.bErrorResponse

    # Method to parse the total amount per product, 10 whole number characters and 2 decimals.
    def pt_amount(self):
        (Amount, post) = self.__pt_getfield('#', self.TrameToParse[self.ParsePos:])
        self.ParsePos = self.ParsePos + post
        logging.info("Amount\t{0}".format(Amount))
        return Amount, self.bErrorResponse

    # Method to parse field discount with 10 whole numbers 2 decimals
    def pt_discountproduct(self):
        (DiscountProduct, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        if DiscountProduct and (not DiscountProduct.isdigit() and ( int(DiscountProduct) < 0 ) ):
            self.bErrorResponse = True
            logging.error("Discount Product bad format")
        else:
            self.ParsePos = self.ParsePos + post
            logging.info("Discount Product\t{0}".format(DiscountProduct))
        return DiscountProduct, self.bErrorResponse

    # Method to parse the extra data block.
    def pt_extradatablock(self):
        (ExtraDataBlock, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        logging.info("Extra Data Block\t{0}".format(ExtraDataBlock))
        self.ParsePos = self.ParsePos + post
        return ExtraDataBlock, self.bErrorResponse
        # TODO: Crear funcion para parsear los campos extra de la trama.

    # Method to parse the encryption key (field not used)
    def pt_encryptionkey(self):
        (EncryptionKey, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        logging.info("Encryption key\t{0}".format(EncryptionKey))
        self.ParsePos = self.ParsePos + post
        return EncryptionKey, self.bErrorResponse

    # Method to parse the Operation mode.
    def pt_communicationtype(self):
        (CommmunicationType, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        if CommmunicationType != 'IP':
            self.bErrorResponse = True
            logging.error("Commmunication Type bad format\t{0}".format(CommmunicationType))
        else:
            logging.info("Commmunication Type\t{0}".format(CommmunicationType))
            self.ParsePos = self.ParsePos + post
        return CommmunicationType, self.bErrorResponse

    # Method to parse the Operation mode.
    def pt_commissionsblock(self):
        (CommissionsBlock, post) = self.__pt_getfield('', self.TrameToParse[self.ParsePos:])
        logging.info("Commissions Block\t{0}".format(CommissionsBlock))
        self.ParsePos = self.ParsePos + post
        return CommissionsBlock, self.bErrorResponse

    # Parse the end delimeter <EM>
    def pt_endtrame(self):
        if self.__pt_checkdelimeter('', self.TrameToParse[self.ParsePos - 1] ):
            self.bErrorResponse = True
            logging.error("The EM delimeter has not been found")
        return self.bErrorResponse

    # Method to parse delimeters.
    @staticmethod
    def __pt_getfield (delimeter, string):
        GetField = ""
        Position = 0
        for i in string:
            Position = Position + 1
            if i == delimeter:
                return GetField, Position
            else:
                GetField = GetField + i

    # Method to look for a delimeter.
    @staticmethod
    def __pt_checkdelimeter(delimeter, character):
        ErrorRetorno = True
        if character == delimeter:
            ErrorRetorno = False
        return ErrorRetorno