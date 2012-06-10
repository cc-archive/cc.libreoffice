import os


from  org.creativecommons.libreoffice.ui.license.UpdateLicenseListner import UpdateLicenseListner
from org.creativecommons.libreoffice.ui.license.JurisdictionSelectListener import JurisdictionSelectListener
from org.creativecommons.libreoffice.ui.license.AcceptWaiveListener import AcceptWaiveListener
from org.creativecommons.libreoffice.ui.license.AcceptListener import AcceptListener
from org.creativecommons.libreoffice.ui.license.FaqClickListener import FaqClickListener
from org.creativecommons.libreoffice.ui.license.OKClickListener import OKClickListener
from org.creativecommons.libreoffice.ui.license.CancelClickListener import CancelClickListener
from org.creativecommons.libreoffice.ui.license.CCClickListener import CCClickListener
from org.creativecommons.libreoffice.ui.license.CC0ClickListener import CC0ClickListener
from org.creativecommons.libreoffice.ui.license.PDClickListener import PDClickListener


class LicenseChooserDialog():
    """Creates a new instance of LicenseChooserDialog
    """

    #TODO: add the global Constants support
    
    #Constants
    
    BTN_CC = "btnCC"
    BTN_CC0 = "btnCC0"
    BTN_PUBLICDOMAIN = "btnPublicdomain"
    BTN_FAQ = "faqbt"
    faqButtonLabel = "FAQ"
    finishButtonLabel = "OK"
    BTN_OK = "finishbt"
    BTN_CANCEL = "cancelbt"
    cancelButtonLabel = "Cancel"
    CMB_JURISDICTION = "cmbJurisdiction"

    LBL_SELECTED_LICENSE_LABEL = "lblSelectedLicense_lbl"
    LBL_SELECTED_LICENSE = "lblSelectedLicense"
    LBL_ALLOW_COMERCIAL_USE = "allowCommercialUse"
    RDO_ALLOW_COMERCIAL_YES = "rdoAllowCommercial_Yes"
    RDO_ALLOW_COMERCIAL_NO = "rdoAllowCommercial_No"
    LBL_ALLOW_MODIFICATIONS = "allowModifications"
    RDO_ALLOW_MODIFICATIONS_YES = "rdoAllowModifications_Yes"
    RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE = "rdoAllowModifications_ShareAlike"
    RDO_ALLOW_MODIFICATIONS_NO = "rdoAllowModifications_No"
    LBL_JURISDICTION_LIST = "lblJurisdictionList"
    CMB_JURISDICTION = "cmbJurisdiction"
    LBL_INSTRUCTIONS_CC = "lblInstructionsCC"

    
    LBL_INSTRUCTIONS_CC0 = "lblInstructionsCC0"
    CHK_WAIVE = "chkWaive"
    TXT_LEGAL_CODE_CC0 = "txtLegalCodeCC0"
    CHK_YES_CC0 = "chkYesCC0"
    CMB_TERRITORY = "cmbTerritory"

    cancelled=True
    
    def __init__(self, ccLoAddin, ctx):
        """
        
        Arguments:
        - `ccLoAddin`:
        - `ctx`:
        """
        self._ccLoAddin = ccLoAddin
        self.m_xContext = ctx
        
        # get the service manager from the component context
        self.xMultiComponentFactory = self.m_xContext.getServiceManager()

    # The CoreReflection object. 
    def __createUnoStruct(self, cTypeName):
        """Create a UNO struct and return it. 
        
        Arguments:
        - `cTypeName`:
        """
        
        self.xMultiComponentFactory = self.m_xContext.getServiceManager()
       
       
       
        oCoreReflection=self.xMultiComponentFactory.createInstance("com.sun.star.reflection.CoreReflection")
        
        oXIdlClass = oCoreReflection.forName( cTypeName ) 
        oReturnValue, oStruct = oXIdlClass.createObject( None ) 
        return oStruct 

    def __makeRectangle(self, nX, nY, nWidth, nHeight ): 
        """Create a com.sun.star.awt.Rectangle struct.""" 
        
        oRect = self.__createUnoStruct( "com.sun.star.awt.Rectangle" ) 
        
        oRect.X = nX 
        oRect.Y = nY 
        oRect.Width = nWidth 
        oRect.Height = nHeight 
        return oRect
    
    def __createAWTControl(self, xpsProperties, ctrlName,ctrlCaption, posSize, step):
        """Add AWT control components to the dialog.
        
        Arguments:
        - `self`:
        - `xpsProperties`:XPropertySet
        - `ctrlName`:String
        - `ctrlCaption`:String
        - `ctrlName`:String
        - `posSize`:Rectangle - https://gist.github.com/990143
        - `step`:integer
        """
    
        #throw the exceptions
        try:
            xpsProperties.setPropertyValue("PositionX",  posSize.X)
            xpsProperties.setPropertyValue("PositionY",  posSize.Y)
            xpsProperties.setPropertyValue("Width",  posSize.Width)
            xpsProperties.setPropertyValue("Height",  posSize.Height)
            xpsProperties.setPropertyValue("Name", ctrlName)
            xpsProperties.setPropertyValue("Step", step)

            if ctrlCaption is not None:
                xpsProperties.setPropertyValue("Label", ctrlCaption)

            
                
            if ( not self.dlgLicenseSelector.hasByName(ctrlName)):
                self.dlgLicenseSelector.insertByName(ctrlName,xpsProperties)
                
            return xpsProperties
            
        except Exception, ex:
            print "Exception in LicenseChooserDialog.__createAWTControl: "
            print ex
            print type(ex)
            raise ex

    def __crateCC0LicenseTab(self):
        
       
        
        try:
            
            lblWarning = self.dlgLicenseSelector.createInstance("com.sun.star.awt.UnoControlFixedTextModel")

            ##TODO: add the Java.util support to the following line
            xpsLblWarning = self.__createAWTControl(lblWarning, self.LBL_INSTRUCTIONS_CC0,"Are you certain you wish to waive all rights to your work? "
                                + "Once these rights are waived, you cannot reclaim them."+ "\n\nIn particular, if you are an artist or author who depends "
                + "upon copyright for your income, "
                + "Creative Commons does not recommend that you use this tool."
                + "\n\nIf you don't own the rights to this work, then do not use CC0. "
                + "\nIf you believe that nobody owns rights to the work, then the "
                + "Public Domain Certification may be what you're looking for.",
                self.__makeRectangle(10, 25, 195, 80), 2)

            xpsLblWarning.setPropertyValue("MultiLine", True)
            fontDes =  xpsLblWarning.getPropertyValue("FontDescriptor")
            fontDes.Weight = 150
            xpsLblWarning.setPropertyValue("FontDescriptor", fontDes)

            chkWaive = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlCheckBoxModel")

            ##TODO:Add java.util support to the following line
            xpsChkWaive = self.__createAWTControl(chkWaive, self.CHK_WAIVE,
                                "I hereby waive all copyright and related or neighboring rights "
                                + "together with all associated claims and causes of action with "
                                + "respect to this work to the extent possible under the law.",
                                self.__makeRectangle(10, 110, 190, 30), 2)
            

            xpsChkWaive.setPropertyValue("MultiLine", True)

            
            ##Legal code
            path=os.path.join(os.path.dirname(__file__), '../../../license/legalcodes/cc0')
            f=open(path,'r')
            cc0LegalCode=f.read()

            txtDeed = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlEditModel")
            xpsTxtDeed = self.__createAWTControl(txtDeed, self.TXT_LEGAL_CODE_CC0, None,
                self.__makeRectangle(10, 145, 190, 60), 2)
            xpsTxtDeed.setPropertyValue("MultiLine", True)
            xpsTxtDeed.setPropertyValue("ReadOnly", True)
            xpsTxtDeed.setPropertyValue("VScroll", True)
            xpsTxtDeed.setPropertyValue("Text", cc0LegalCode)


            chkYes = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlCheckBoxModel")
            ##TODO:Add java.util support to the following line
            xpsChkYes = self.__createAWTControl(chkYes, self.CHK_YES_CC0,
                    "I have read and understand the terms and intended legal effect of CC0, "
                    + "and hereby voluntarily elect to apply it to this work.",
                    self.__makeRectangle(10, 210, 190, 20), 2)
            xpsChkYes.setPropertyValue("MultiLine", True)

            ##Territory
            lblJurisdictionList = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsLblJurisdictionList = self.__createAWTControl(lblJurisdictionList, "lbltrritory",
                "Territory", self.__makeRectangle(10, 230, 45, 15), 2)

            #TODO: This list currently contains nothing. Add items to the list
            cmbTerritoryList = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlListBoxModel")
            xPSetList = self.__createAWTControl(cmbTerritoryList, self.CMB_TERRITORY,
                None, self.__makeRectangle(55, 230, 120, 12), 2)
            xPSetList.setPropertyValue("Dropdown", True)
            xPSetList.setPropertyValue("MultiSelection", False)
            
        except Exception,ex:
            print 'Exception in LicenseChooserDialog.__crateCC0LicenseTab'
            print type(ex)
            print ex
            raise ex


    #TODO: Method is not fully implemented.
    def __createCCLicenseTab(self, ):
        """
        """

        
        
        
        try:
            #create the current license information
            lblSelectedLicenseLabel = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            self.__createAWTControl(lblSelectedLicenseLabel, self.LBL_SELECTED_LICENSE_LABEL,
                "Selected License:", self.__makeRectangle(10, 20, 50, 15), 1)
            lblSelectedLicense = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsSelectedLicense = self.__createAWTControl(lblSelectedLicense, self.LBL_SELECTED_LICENSE,
                None, self.__makeRectangle(60, 20, 145, 30), 1)
            xpsSelectedLicense.setPropertyValue("MultiLine", True)

            #Allow commercial uses of your work?
            lblAllowCommercialUse = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            #TODO:The next line needs localization support.
            self.__createAWTControl(lblAllowCommercialUse, self.LBL_ALLOW_COMERCIAL_USE,
                "commercial", self.__makeRectangle(15, 45, 100, 12), 1)

            radioCommercialYes = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            #TODO:The next line needs localization support.
            xpsRadioCommercialYes = self.__createAWTControl(
                radioCommercialYes, self.RDO_ALLOW_COMERCIAL_YES,
                "Yes", self.__makeRectangle(20, 60, 30, 12), 1)
            #TODO: Original line was  new Short((short) 1))
            xpsRadioCommercialYes.setPropertyValue("State", 1)

            radioCommercialNo = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioCommercialNo = self.__createAWTControl(
                radioCommercialNo, self.RDO_ALLOW_COMERCIAL_NO,
                "No", self.__makeRectangle(20, 75, 30, 12), 1)
            #TODO: Original line was  new Short((short) 1))
            xpsRadioCommercialNo.setPropertyValue("State", 0)

            #Allow modifications of your work?
            lblAllowModifications = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            self.__createAWTControl(lblAllowModifications, self.LBL_ALLOW_MODIFICATIONS,
                "derivatives", self.__makeRectangle(15, 90, 100, 12), 1)
            radioModificationsYes = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioModificationYes = self.__createAWTControl(
                radioModificationsYes, self.RDO_ALLOW_MODIFICATIONS_YES,
                "Yes", self.__makeRectangle(20, 105, 30, 12), 1)
            #TODO: was new Short((short) 1)
            xpsRadioModificationYes.setPropertyValue("State", 1)

            radioModificationsShareAlike = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioModificationsShareAlike = self.__createAWTControl(
                radioModificationsShareAlike, self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE,
                "Yes, as long as others share alike", self.__makeRectangle(20, 120, 100, 12), 1)
            #TODO: was new Short((short) 1)
            xpsRadioModificationsShareAlike.setPropertyValue("State", 0)

            radioModificationsNo = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioModificationsNo = self.__createAWTControl(
                radioModificationsNo, self.RDO_ALLOW_MODIFICATIONS_NO,
                "No", self.__makeRectangle(20, 135, 30, 12), 1)
            #TODO: was new Short((short) 1)
            xpsRadioModificationsNo.setPropertyValue("State", 0)

            #Create the jurisdiction drop-down list
            lblJurisdictionList = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsLblJurisdictionList =self.__createAWTControl(lblJurisdictionList, self.LBL_JURISDICTION_LIST,
                "license.jurisdiction_question",self.__makeRectangle(15, 150, 75, 15), 1)

            cmbJurisdictionList = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlListBoxModel")
            xPSetList = self.__createAWTControl(cmbJurisdictionList, self.CMB_JURISDICTION,
                None, self.__makeRectangle(90, 150, 60, 12), 1)
            #TODO: Next two lines are different from the source- new Boolean()
            xPSetList.setPropertyValue("Dropdown", True)
            xPSetList.setPropertyValue("MultiSelection", False)

            hrLine = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedLineModel")
            xpshrLine = self.__createAWTControl(hrLine, "hrLine",
                None, self.__makeRectangle(5, 165, 200, 5), 1)
            xpshrLine.setPropertyValue("Orientation", 0)

            lblInstructions = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsLblInstructions = self.__createAWTControl(lblInstructions, self.LBL_INSTRUCTIONS_CC,
                "With a Creative Commons license, you keep your copyright but allow "
                + "people to copy and distribute your work provided they give you credit  "
                + "  and only on the conditions you specify here. "
                + "\n\nIf you want to offer your work with no conditions or you"
                + " want to certify a work as public domain, choose one of the "
                + "public domain tools.(CC0 & Public Domain)", self.__makeRectangle(10, 175, 195, 80), 1)
            
            xpsLblInstructions.setPropertyValue("MultiLine", True)
            fontDes = xpsLblInstructions.getPropertyValue("FontDescriptor")
            fontDes.Weight = 75
            xpsLblInstructions.setPropertyValue("FontDescriptor", fontDes)
            
        except Exception,ex:
            print 'Exception in LicenseChooserDialog.__createCCLicenseTab'
            print type(ex)
            print ex
            raise ex
        

    def __addListners(self,classType,controlName,listner):
        
        """Creates event listners
    
        Arguments:
        - `classType`: The type of the class
        - `controlName`: String
        - `listner`: XEventListener
        """
        if (classType == 'XButton'):
            #print "XButton"
            objectButton = self.dialog.getControl(controlName)
            objectButton.addActionListener( listner)

        elif (classType=='XRadioButton'):
            #print 'XRadioButton'
            self.dialog.getControl(controlName).addItemListener(listner)
            

        elif (classType == 'XCheckBox'):
            #print 'XCheckBox'
            self.dialog.getControl(controlName).addItemListener(listner)


    def close(self, ):
        """End the excution of the dialog
        """
        self.dialog.endExecute()

    def updateSelectedLicense(self, ):
        """
        """
        xpsSelectedLicense=self.getNameContainer().getByName(self.LBL_SELECTED_LICENSE)
        ##TODO:Complete the method
        
            
    def showDialog(self):
        """Shows the LicenseChooserDialog 
        
        Arguments:
        - `self`:
        """
       

        
       
        try:

            #set to modify the global copies of variables
            #global BTN_CC
      
            # create the dialog model and set the properties
            self.dlgLicenseSelector = self.xMultiComponentFactory.createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialogModel", self.m_xContext)


            ###
            #The following part was changed from the origianl code
            ###
            
            #rect=self.__makeRectangle(100, 80, 210, 275)
      
            self.dlgLicenseSelector.Width=210
            self.dlgLicenseSelector.Height=275
            self.dlgLicenseSelector.PositionX=100
            self.dlgLicenseSelector.PositionY=80
            self.dlgLicenseSelector.Title="Sharing & Reuse Permissions"
      

            ##--due to the following commment the following code in __createAWTControl is not run

            ##if ( not self.dlgLicenseSelector.hasByName(ctrlName)):
            ##    self.dlgLicenseSelector.insertByName(ctrlName,xpsProperties)

            
            #xPSetDialog=self.__createAWTControl(self.dlgLicenseSelector, "cc", None,rect,1)
            #xPSetDialog.setPropertyValue("Title", "Sharing & Reuse Permissions")

            #--
            ###
            ###

            #get the name container for the dialog for inserting other elements
            self.xNameCont=self.dlgLicenseSelector
            
            ###Tabs
            ##CC
            ccButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")

           
            
            
            xPSetCCButton = self.__createAWTControl(ccButton, self.BTN_CC,
                None, self.__makeRectangle(4, 3, 70, 12), 0)

            xPSetCCButton.setPropertyValue("DefaultButton", True)
            
            #TODO: The next line needs localization support. See original code
            #for more details.
           
            xPSetCCButton.setPropertyValue("Label", "Creative_Commons")
            xPSetCCButton.setPropertyValue("Toggle", True)

            fontDes = xPSetCCButton.getPropertyValue("FontDescriptor")
            fontDes.Weight = 150
            xPSetCCButton.setPropertyValue("FontDescriptor", fontDes)
            #TODO: Original code had (short)1
            xPSetCCButton.setPropertyValue("State", 1)

            ##CC0

            cc0Button = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            xPSetCC0Button = self.__createAWTControl(cc0Button, self.BTN_CC0,
                None, self.__makeRectangle(73, 3, 20, 12), 0)
            xPSetCC0Button.setPropertyValue("DefaultButton", True)
            xPSetCC0Button.setPropertyValue("Label", "CC0")
            xPSetCC0Button.setPropertyValue("Toggle", True)
            fontDes = xPSetCC0Button.getPropertyValue("FontDescriptor")
            fontDes.Weight = 75
            xPSetCC0Button.setPropertyValue("FontDescriptor", fontDes)
            #TODO: Original code had (short)0
            xPSetCC0Button.setPropertyValue("State", 0)
            
            ##PD

            pdButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            xPSetPDButton = self.__createAWTControl(pdButton, self.BTN_PUBLICDOMAIN,
                None,self.__makeRectangle(92, 3, 60, 12), 0)
            xPSetPDButton.setPropertyValue("DefaultButton", True)
            #TODO: The next line needs localization support.
            xPSetPDButton.setPropertyValue("Label","Public Domain")
            xPSetPDButton.setPropertyValue("Toggle", True)
            fontDes = xPSetPDButton.getPropertyValue("FontDescriptor")
            fontDes.Weight = 75
            xPSetPDButton.setPropertyValue("FontDescriptor", fontDes)
            #TODO: Original code had (short)0
            xPSetPDButton.setPropertyValue("State", 0)

            ##Creates the outer frame like box of the window
            oGBResults = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlGroupBoxModel")
            xpsBox =self.__createAWTControl(
                oGBResults, "box", None, self.__makeRectangle(2, 15, 206, 243), 0)

            ##Create Tabs
            self.__crateCC0LicenseTab()
            self.__createCCLicenseTab()
            print 'passed'

            ##create the button model - FAQ and set the properties
            faqButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            xPSetFaqButton = self.__createAWTControl(faqButton, self.BTN_FAQ,
                None, self.__makeRectangle(70, 260, 40, 14), 0)
            xPSetFaqButton.setPropertyValue("DefaultButton", True)
            xPSetFaqButton.setPropertyValue("Label", self.faqButtonLabel)

            ##create the button model - OK and set the properties
            finishButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            self.xPSetFinishButton = self.__createAWTControl(finishButton, self.BTN_OK,
                None, self.__makeRectangle(115, 260, 40, 14), 0)
            self.xPSetFinishButton.setPropertyValue("DefaultButton", True)
            self.xPSetFinishButton.setPropertyValue("Label", self.finishButtonLabel)

            ## create the button model - Cancel and set the properties
            cancelButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            xPSetCancelButton = self.__createAWTControl(cancelButton, self.BTN_CANCEL,
                None, self.__makeRectangle(160, 260, 40, 14), 0)
            xPSetCancelButton.setPropertyValue("Name", self.BTN_CANCEL)
            xPSetCancelButton.setPropertyValue("Label", self.cancelButtonLabel)
            
            ##create the dialog control and set the model
            self.dialog  = self.xMultiComponentFactory.createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialog", self.m_xContext)
            # xControl = dialog
            #xControlModel =  dlgLicenseSelector
            
            self.dialog .setModel(self.dlgLicenseSelector)

            ##add an action listener to the Previous button control
            #xControlCont=self.dialog 
            cmbJList=self.dialog .getControl(self.CMB_JURISDICTION)
            #TODO: Add the items to the cmbJList properly (Line 227-230)

            count=0

            ##add Unported, which isn't actually a jurisdiction'
            count+=1
            cmbJList.addItem("Unported", count)
            #TODO: add line 236-239
            
            
            ##add a bogus place-holder for Unported in the JurisdictionList to
            ##ensure indices match up when determining the item selectedJurisdiction
            #TODO: add line 243
            
            ##Pre-select Unported
            #TODO: bit different from the origianl code
            cmbJList.selectItemPos(0,True)
            cmbJList.makeVisible(0)

            

            ##listen for license selection changes
            #self.__addListners("XCheckBox", None,None)
            #self.__addListners("XRadioButton",None,None)
            #self.__addListners("XButton",None,None)

            self.__addListners("XRadioButton",self.RDO_ALLOW_COMERCIAL_YES,UpdateLicenseListner(self))
            self.__addListners("XRadioButton",self.RDO_ALLOW_COMERCIAL_NO,UpdateLicenseListner(self))
            self.__addListners("XRadioButton",self.RDO_ALLOW_MODIFICATIONS_YES,UpdateLicenseListner(self))
            self.__addListners("XRadioButton",self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE,UpdateLicenseListner(self))
            self.__addListners("XRadioButton",self.RDO_ALLOW_MODIFICATIONS_NO,UpdateLicenseListner(self))

            cmbJList.addItemListener(JurisdictionSelectListener(self))

            #self.__addListners("XCheckBox", self.CHK_WAIVE,AcceptWaiveListener(self))
            #self.__addListners("XCheckBox", self.CHK_YES_CC0,AcceptListener(self))
            #self.__addListners("XCheckBox", self.CHK_YES_PD,AcceptListener(self))

            

            
            ##add an action listeners to buttons

            ##Set the initial license

            ##create a peer

            
            ##execute the dialog
            self.dialog .setVisible(True)
            self.dialog .execute()
            

            ##dispose the dialog
            #self.dialog .dispose()
            
            
        except Exception,ex:
            print "Exception in LicenseChooserDialog.showDialog:"
            print ex

            #TODO: match the raising exception with the origianl source
            raise ex

    def setLicenseType(self, type):
        """Set license type according to the tab selected.
    
        Arguments:
        - `type`: Integer
        """

        btnArray=[BTN_CC, BTN_CC0, BTN_PUBLICDOMAIN]

        try:
            for index, entry in enumerate(btnArray):
                xPSetLicenseButton=self.xNameCont.getByName(entry)
                fontDes=xPSetLicenseButton.getPropertyValue("FontDescriptor")

                if (index+1 == type):
                    fontDes.Weight = 150
                    ##TODO: was (short)1
                    xPSetLicenseButton.setPropertyValue("State", 1)
                else:
                    fontDes.Weight = 50
                    ##TODO: was (short)0
                    xPSetLicenseButton.setPropertyValue("State", 0)
                    
                xPSetLicenseButton.setPropertyValue("FontDescriptor", fontDes)

            if (type != 1):
                self.xPSetFinishButton.setPropertyValue("Enabled", False)
            else:
                self.xPSetFinishButton.setPropertyValue("Enabled", True)

            self.xNameCont.getByName(CHK_YES_CC0).setPropertyValue("Enabled",False)
            self.xNameCont.getByName(TXT_LEGAL_CODE_CC0).setPropertyValue("Enabled",False)
            ##TODO: was (short)0
            self.xNameCont.getByName(CHK_WAIVE).setPropertyValue("State", 0)
            self.xNameCont.getByName(CHK_YES_CC0).setPropertyValue("State", 0)
            self.xNameCont.getByName(CMB_TERRITORY).setPropertyValue("Enabled",False)

            ##TODO: Implement
            #cmbTList.selectItemPos((short) 0, true);

            self.xNameCont.getByName(CHK_YES_PD).setPropertyValue("State", 0)

            ##Note: It seems like that self.dlgLicenseSelector and 
            ##xPSetDialog are equal
            self.dlgLicenseSelector.setPropertyValue("Step", type)

            
            
            
            

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.setLicenseType'
            print type(ex)
            print ex
            raise ex
        
