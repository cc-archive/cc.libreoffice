#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import os
import traceback
import uno


from com.sun.star.beans import PropertyValue

from  org.creativecommons.libreoffice.ui.license.updatelicenselistner \
  import UpdateLicenseListner
from org.creativecommons.libreoffice.ui.license.jurisdictionselectlistener \
  import JurisdictionSelectListener
from org.creativecommons.libreoffice.ui.license.acceptwaivelistener \
  import AcceptWaiveListener
from org.creativecommons.libreoffice.ui.license.acceptlistener \
  import AcceptListener
from org.creativecommons.libreoffice.ui.license.faqclicklistener \
  import FaqClickListener
from org.creativecommons.libreoffice.ui.license.okclicklistener \
  import OKClickListener
from org.creativecommons.libreoffice.ui.license.cancelclicklistener \
  import CancelClickListener
from org.creativecommons.libreoffice.ui.license.territoryselectlistener \
  import TerritorySelectListener
from org.creativecommons.libreoffice.ui.license.tablistener \
  import TabListener

from org.creativecommons.license.store import jurisdictions
from org.creativecommons.license.chooser import Chooser
from org.creativecommons.license.license import License
from org.creativecommons.license.jurisdiction import Jurisdiction


class LicenseChooserDialog():
    """Creates a new instance of LicenseChooserDialog
    """
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
    LBL_INFO_METADATA = "lblInstructionsMetadata"
    CHK_WAIVE = "chkWaive"
    TXT_LEGAL_CODE_CC0 = "txtLegalCodeCC0"
    TXT_LEGAL_CODE_PD = "txtLegalCodePD"
    CHK_YES_CC0 = "chkYesCC0"
    CHK_YES_PD = "chkYesPD"
    CHK_YES_METADATA = "chkYesMetadata"
    CMB_TERRITORY = "cmbTerritory"

    CC_TAB_NAME = "ccPage"
    CC0_TAB_NAME = "cc0Page"
    PD_TAB_NAME = "pdPage"
    METADATA_TAB_NAME = "metadataPage"

    ATTRIBUTE_WORK_TO_URL = "attributeWorkToUrl"
    LBL_ATTRIBUTE_WORK_TO_URL = "attributeWorkToUrlLabel"

    cancelled = True

    def __init__(self, ccLoAddin, ctx):
        """
        Arguments:
        - `ccLoAddin`:
        - `ctx`:
        """
        self._ccLoAddin = ccLoAddin
        self.m_xContext = ctx
        self.xNameCont = None

        # get the service manager from the component context
        self.xMultiComponentFactory = self.m_xContext.getServiceManager()

        #get the current component
        self.xCurrentComponent = \
          self.xMultiComponentFactory.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", ctx).getCurrentComponent()

        #initialize selectedTerritory, useful when a territory is not selected
        self.selectedTerritory = None

        #TODO-how about uno.createUnoStruct ?
    # The CoreReflection object.
    def __createUnoStruct(self, cTypeName):
        """Create a UNO struct and return it.

        Arguments:
        - `cTypeName`:
        """

        self.xMultiComponentFactory = self.m_xContext.getServiceManager()

        oCoreReflection = self.xMultiComponentFactory.createInstance(
            "com.sun.star.reflection.CoreReflection")

        oXIdlClass = oCoreReflection.forName(cTypeName)
        oReturnValue, oStruct = oXIdlClass.createObject(None)
        return oStruct

    def __makeRectangle(self, nX, nY, nWidth, nHeight):
        """Create a com.sun.star.awt.Rectangle struct."""

        oRect = self.__createUnoStruct("com.sun.star.awt.Rectangle")

        oRect.X = nX
        oRect.Y = nY
        oRect.Width = nWidth
        oRect.Height = nHeight
        return oRect

    def __createAWTControl(self, xpsProperties, ctrlName, ctrlCaption,
                           posSize, step, targetModel):
        """Add AWT control components to the dialog.

        Arguments:
        - `self`:
        - `xpsProperties`:XPropertySet
        - `ctrlName`:String
        - `ctrlCaption`:String
        - `ctrlName`:String
        - `posSize`:Rectangle - https://gist.github.com/990143
        - `step`:integer
        - `targetModel`:The model in which the element should be created .
        """

        #throw the exceptions
        try:
            xpsProperties.setPropertyValue("PositionX",  posSize.X)
            xpsProperties.setPropertyValue("PositionY",  posSize.Y)
            xpsProperties.setPropertyValue("Width",  posSize.Width)
            xpsProperties.setPropertyValue("Height",  posSize.Height)
            xpsProperties.setPropertyValue("Name", ctrlName)
            #xpsProperties.setPropertyValue("Step", step)

            if ctrlCaption is not None:
                xpsProperties.setPropertyValue("Label", ctrlCaption)

            if (not targetModel.hasByName(ctrlName)):
                targetModel.insertByName(ctrlName, xpsProperties)

            return xpsProperties

        except Exception, ex:
            print "Exception in LicenseChooserDialog.__createAWTControl: "
            traceback.print_exc()
            raise ex

    def __crateCC0LicenseTab(self):
        """Creates the CC0 license tab
        """
        try:
            lblWarning = self.cc0Tab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")

            ##TODO: add the Java.util support to the following line
            xpsLblWarning = self.__createAWTControl(lblWarning,
                                                    self.LBL_INSTRUCTIONS_CC0,
                                                    ("Are you certain "
            "you wish to waive all "
            "rights to your work? "
            "Once these rights are waived, you cannot reclaim them."
            "\n\nIn particular, if you are an artist or author who depends "
            "upon copyright for your income, "
            "Creative Commons does not recommend that you use this tool."
            "\n\nIf you don't own the rights to this work, then do not use "
            "CC0. "
            "\nIf you believe that nobody owns rights to the work, then the "
            "Public Domain Certification may be what you're looking for."),
            self.__makeRectangle(10, 25, 195, 80), 2, self.cc0Tab)

            xpsLblWarning.setPropertyValue("MultiLine", True)
            fontDes = xpsLblWarning.getPropertyValue("FontDescriptor")
            fontDes.Weight = 150
            xpsLblWarning.setPropertyValue("FontDescriptor", fontDes)

            chkWaive = self.cc0Tab.createInstance(
                "com.sun.star.awt.UnoControlCheckBoxModel")

            ##TODO:Add java.util support to the following line
            xpsChkWaive = self.\
              __createAWTControl(chkWaive, self.CHK_WAIVE,
                                ("I hereby waive all copyright and related"
                                 " or neighboring rights together with all"
                                 "associated claims and causes of action with "
                                 "respect to this work to the extent possible"
                                 " under the law."),
                                self.__makeRectangle(10, 110, 190, 30), 2,
                                self.cc0Tab)

            xpsChkWaive.setPropertyValue("MultiLine", True)

            ##Legal code

            #relative path to file
            rPath = \
              ".." + os.path.sep + ".." + os.path.sep + ".." + os.path.sep +\
               "license" + os.path.sep + "legalcodes" + os.path.sep + "cc0"
            path = os.path.join(os.path.dirname(__file__),
                              rPath)
            f = open(path, 'r')
            cc0LegalCode = f.read()

            xpsTxtDeed = self.cc0Tab.createInstance(
                "com.sun.star.awt.UnoControlEditModel")

            xpsTxtDeed.setPropertyValue("MultiLine", True)
            xpsTxtDeed.setPropertyValue("ReadOnly", True)
            xpsTxtDeed.setPropertyValue("VScroll", True)
            xpsTxtDeed.setPropertyValue("Text", cc0LegalCode)
            self.__createAWTControl(xpsTxtDeed,
                                                 self.TXT_LEGAL_CODE_CC0, None,
                self.__makeRectangle(10, 145, 190, 60), 2, self.cc0Tab)

            chkYes = self.cc0Tab.createInstance(
                "com.sun.star.awt.UnoControlCheckBoxModel")
            ##TODO:Add java.util support to the following line
            xpsChkYes = self.\
              __createAWTControl(chkYes, self.CHK_YES_CC0,
                    ("I have read and understand the terms and intended"
                     "legal effect of CC0, "
                     "and hereby voluntarily elect to apply it to this work."),
                    self.__makeRectangle(10, 210, 190, 20), 2, self.cc0Tab)
            xpsChkYes.setPropertyValue("MultiLine", True)

            ##Territory
            lblJurisdictionList = self.cc0Tab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsLblJurisdictionList = self.__createAWTControl(
                lblJurisdictionList, "lbltrritory",
                "Territory", self.__makeRectangle(10, 230, 45, 15), 2,
                self.cc0Tab)

            #TODO: This list currently contains nothing. Add items to the list
            cmbTerritoryList = self.cc0Tab.createInstance(
                "com.sun.star.awt.UnoControlListBoxModel")

            cmbTerritoryList.setPropertyValue("Dropdown", True)
            cmbTerritoryList.setPropertyValue("MultiSelection", False)

            self.__createAWTControl(cmbTerritoryList,
                                                self.CMB_TERRITORY,
                None, self.__makeRectangle(55, 230, 120, 12), 2, self.cc0Tab)

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__crateCC0LicenseTab'
            traceback.print_exc()
            raise ex

    def __createCCLicenseTab(self, ):
        """Creates the CC license tab
        """
        try:
            #create the current license information
            lblSelectedLicenseLabel = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            self.__createAWTControl(lblSelectedLicenseLabel,
                                    self.LBL_SELECTED_LICENSE_LABEL,
                "Selected License:", self.__makeRectangle(10, 20, 50, 15), 1,
                self.ccTab)
            lblSelectedLicense = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsSelectedLicense = self.__createAWTControl(
                lblSelectedLicense, self.LBL_SELECTED_LICENSE,
                None, self.__makeRectangle(60, 20, 145, 30), 1, self.ccTab)
            xpsSelectedLicense.setPropertyValue("MultiLine", True)

            #Allow commercial uses of your work?
            lblAllowCommercialUse = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            #TODO:The next line needs localization support.
            self.__createAWTControl(lblAllowCommercialUse,
                                    self.LBL_ALLOW_COMERCIAL_USE,
                "Commercial", self.__makeRectangle(15, 45, 100, 12), 1,
                self.ccTab)

            radioCommercialYes = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            #TODO:The next line needs localization support.
            xpsRadioCommercialYes = self.__createAWTControl(
                radioCommercialYes, self.RDO_ALLOW_COMERCIAL_YES,
                "Yes", self.__makeRectangle(20, 60, 30, 12), 1, self.ccTab)
            #TODO: Original line was  new Short((short) 1))
            xpsRadioCommercialYes.setPropertyValue("State", 1)

            radioCommercialNo = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioCommercialNo = self.__createAWTControl(
                radioCommercialNo, self.RDO_ALLOW_COMERCIAL_NO,
                "No", self.__makeRectangle(20, 75, 30, 12), 1, self.ccTab)
            #TODO: Original line was  new Short((short) 0))
            xpsRadioCommercialNo.setPropertyValue("State", 0)

            #Allow modifications of your work?
            lblAllowModifications = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            self.__createAWTControl(lblAllowModifications,
                                    self.LBL_ALLOW_MODIFICATIONS,
                "Derivatives", self.__makeRectangle(15, 90, 100, 12), 1,
                self.ccTab)
            radioModificationsYes = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioModificationYes = self.__createAWTControl(
                radioModificationsYes, self.RDO_ALLOW_MODIFICATIONS_YES,
                "Yes", self.__makeRectangle(20, 105, 30, 12), 1, self.ccTab)
            #TODO: was new Short((short) 1)
            xpsRadioModificationYes.setPropertyValue("State", 1)

            radioModificationsShareAlike = self.ccTab.\
              createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioModificationsShareAlike = self.__createAWTControl(
                radioModificationsShareAlike,
                self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE,
                "Yes, as long as others share alike", self.__makeRectangle(
                    20, 120, 100, 12), 1, self.ccTab)
            #TODO: was new Short((short) 1)
            xpsRadioModificationsShareAlike.setPropertyValue("State", 0)

            radioModificationsNo = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlRadioButtonModel")
            xpsRadioModificationsNo = self.__createAWTControl(
                radioModificationsNo, self.RDO_ALLOW_MODIFICATIONS_NO,
                "No", self.__makeRectangle(20, 135, 30, 12), 1, self.ccTab)
            #TODO: was new Short((short) 1)
            xpsRadioModificationsNo.setPropertyValue("State", 0)

            #Create the jurisdiction drop-down list
            lblJurisdictionList = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsLblJurisdictionList = self.__createAWTControl(
                lblJurisdictionList, self.LBL_JURISDICTION_LIST,
                "Jurisdiction", self.__makeRectangle(
                    15, 150, 75, 15), 1, self.ccTab)

            cmbJurisdictionList = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlListBoxModel")

            cmbJurisdictionList.setPropertyValue("Dropdown", True)
            cmbJurisdictionList.setPropertyValue("MultiSelection", False)
            self.__createAWTControl(cmbJurisdictionList,
                                                self.CMB_JURISDICTION,
                None, self.__makeRectangle(90, 150, 60, 12), 1, self.ccTab)

            hrLine = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedLineModel")
            xpshrLine = self.__createAWTControl(hrLine, "hrLine",
                None, self.__makeRectangle(5, 165, 200, 5), 1, self.ccTab)
            xpshrLine.setPropertyValue("Orientation", 0)

            lblInstructions = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")
            xpsLblInstructions = self.__createAWTControl(
                lblInstructions, self.LBL_INSTRUCTIONS_CC,
                ("With a Creative Commons license, you keep your copyright but"
                 " allow "
                 "people to copy and distribute your work provided they give"
                 " you credit  "
                 "  and only on the conditions you specify here. "
                 "\n\nIf you want to offer your work with no conditions or you"
                 " want to certify a work as public domain, choose one of the "
                 "public domain tools.(CC0 & Public Domain)"),
                 self.__makeRectangle(10, 175, 195, 80), 1, self.ccTab)

            xpsLblInstructions.setPropertyValue("MultiLine", True)
            fontDes = xpsLblInstructions.getPropertyValue("FontDescriptor")
            fontDes.Weight = 75
            xpsLblInstructions.setPropertyValue("FontDescriptor", fontDes)

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__createCCLicenseTab'
            traceback.print_exc()
            raise ex

    def __cratePDLicenseTab(self, ):
        """Creates the PD license tab
        """
        try:
            lblWarning = self.pdTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")

            xpsLblWarning = self.\
              __createAWTControl(lblWarning, "pdwarning",
                ("You have selected the Public Domain Certification. "
                 "The Public Domain Certification should only be used "
                 "to certify "
                 "a work that is already in the public domain. "
                 "\n\nCreative Commons does not recommend you use the "
                 "Public Domain Certification for dedicating a work still "
                 "protected by copyright to the public domain. "
                 "To dedicate a work to the public domain, consider using "
                 "CC0. "
                 "\n\nPlease note that if you use the Public Domain "
                 "Certification to "
                 "dedicate a work to the public domain, it may not be valid "
                 "outside "
                 "of the United States."),
                self.__makeRectangle(10, 25, 190, 100), 3, self.pdTab)

            xpsLblWarning.setPropertyValue("MultiLine", True)

            fontDes = xpsLblWarning.getPropertyValue("FontDescriptor")
            fontDes.Weight = 150
            xpsLblWarning.setPropertyValue("FontDescriptor", fontDes)

            #relative path to file
            rPath =\
               ".." + os.path.sep + ".." + os.path.sep + ".." + os.path.sep +\
                "license" + os.path.sep + "legalcodes" + os.path.sep + "pd"
            path = os.path.join(
                os.path.dirname(__file__), rPath)
            f = open(path, 'r')
            pdLegalCode = f.read()

            #Legal code
            xpsTxtDeed = self.pdTab.createInstance(
                "com.sun.star.awt.UnoControlEditModel")
            xpsTxtDeed.setPropertyValue("MultiLine", True)
            xpsTxtDeed.setPropertyValue("ReadOnly", True)
            xpsTxtDeed.setPropertyValue("VScroll", True)
            xpsTxtDeed.setPropertyValue("Text", pdLegalCode)
            xpsTxtDeed = self.__createAWTControl(xpsTxtDeed,
                                               self.TXT_LEGAL_CODE_PD, None,
                                               self.__makeRectangle(
                                                   10, 130, 190, 75), 3,
                                                   self.pdTab)

            chkYes = self.pdTab.createInstance(
                "com.sun.star.awt.UnoControlCheckBoxModel")

            ##TODO: add internationalization support
            xpsChkYes = self.__createAWTControl(chkYes, self.CHK_YES_PD,
                                ("I have read and understand the terms"
                                 " and intended legal effect of "
                                 "this tool, and hereby voluntarily"
                                 " elect to apply it to this work."),
                                self.__makeRectangle(10, 210, 190, 30), 3,
                                self.pdTab)
            xpsChkYes.setPropertyValue("MultiLine", True)

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__cratePDLicenseTab'
            traceback.print_exc()
            raise ex

    def __createMetadataTab(self, ):
        """Creates the Metadata tab
    """
        
        try:
            infoLabelModel = self.metadataTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")

            infoLabel = self.\
              __createAWTControl(infoLabelModel, self.LBL_INFO_METADATA ,
                ("This part is optional, but filling it out"
                 " will add machine-readable metadata to the"
                 " document and it will help others attribiute you!"),
                self.__makeRectangle(10, 25, 190, 20), 3, self.metadataTab)

            infoLabel.MultiLine = True
            fontDes = infoLabel.FontDescriptor
            fontDes.Weight = 150
            infoLabel.FontDescriptor = fontDes


            chkYesModel = self.metadataTab.createInstance(
                "com.sun.star.awt.UnoControlCheckBoxModel")
            chkYesModel.Enabled = True

            ##TODO: add internationalization support
            chkYes = self.__createAWTControl(chkYesModel, self.CHK_YES_METADATA,
                                ("I want to add metadata"),
                                self.__makeRectangle(10, 45, 100, 30), 3,
                                self.metadataTab)

            xpsTxtDeed = self.metadataTab.createInstance(
                "com.sun.star.awt.UnoControlEditModel")
            xpsTxtDeed.setPropertyValue("MultiLine", False)
            xpsTxtDeed.setPropertyValue("ReadOnly", True)
            xpsTxtDeed = self.__createAWTControl(xpsTxtDeed,
                                               self.ATTRIBUTE_WORK_TO_URL, None,
                                               self.__makeRectangle(
                                                   80, 55, 100, 10), 3,
                                                   self.metadataTab)

            attWorktoUrlLblModel = self.metadataTab.createInstance(
                "com.sun.star.awt.UnoControlFixedTextModel")

            attWorktoUrlLbl = self.\
              __createAWTControl(attWorktoUrlLblModel, self.LBL_ATTRIBUTE_WORK_TO_URL ,
                ("Attribute work to URL"),
                self.__makeRectangle(10, 55, 50, 20), 3, self.metadataTab)
            
        except Exception, e:
            traceback.print_exc()
            #raise e


    def __addListners(self, classType, controlName, listner, page=None):
        """Creates event listners

        Arguments:
        - `classType`: The type of the class
        - `controlName`: String
        - `listner`: XEventListener
        - `page`: The tab page that the controlName is in.If page is None,
        it'll be assumed that the controlName is in the dialog(not in a tab)
        """
        if (classType == 'XButton'):
            #print "XButton"
            objectButton = self.dialog.getControl(controlName)
            objectButton.addActionListener(listner)

        elif (classType == 'XRadioButton'):
            #get the CC tab page by default since xRadioButtons are
            #only available in that tab.
            ccTabPage = self.tab.getControl(self.CC_TAB_NAME)
            ccTabPage.getControl(controlName).addItemListener(listner)

        elif (classType == 'XCheckBox'):
            #get the tab page

            tabPage = self.tab.getControl(page)

            tabPage.getControl(controlName).addItemListener(listner)

        elif (classType == 'XTabPage'):

            #tabPage = self.tab.getControl(page)
            #print dir(tabPage)
            self.tab.addTabListener(listner)

    def close(self, ):
        """End the excution of the dialog
        """
        self.dialog.endExecute()

    def __getRadioButtonValue(self, rdoName):
        """
        Returns the value of the given radio button

        Arguments:
        - `rdoName`:String
        """
        try:

            xPSetList = self.ccTab.getByName(rdoName)
            if (xPSetList.getPropertyValue("State") == 1):
                return True
            else:
                return False

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__getRadioButtonValue'
            traceback.print_exc()
            return None
            #raise ex

    def updateSelectedLicense(self, ):
        """Updates the current selected license
        label value.
        """
        try:
            ccTabPage = self.tab.getControl(self.CC_TAB_NAME)
            xpsSelectedLicense = self.ccTab.getByName(
                self.LBL_SELECTED_LICENSE)

            xpsSelectedLicense.setPropertyValue("Label",
                                                self.getSelectedLicense().name)

        except Exception, ex:
            traceback.print_exc()

    def __getGraphic(self, sImageUrl):
        """Returns the xGraphic object from the
            given image location

        Arguments:
        - `sImageUrl`:String
        """
        xGraphic = None

        try:

            #create a GraphicProvider at the global service manager...
            oGraphicProvider = self.xMultiComponentFactory.\
              createInstanceWithContext(
                    "com.sun.star.graphic.GraphicProvider", self.m_xContext)
            aPropertyValue = PropertyValue()
            aPropertyValue.Name = "URL"
            aPropertyValue.Value = sImageUrl
            #Create an array
            #aPropertyValues=()
            aPropertyValues = (aPropertyValue,)

            xGraphic = oGraphicProvider.queryGraphic(aPropertyValues)

            return xGraphic

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__getGraphic'
            traceback.print_exc()
            raise ex

    def __setInfoImage(self, rect, item, title, step):
        """Set "i" image for tips on each license option.

        Arguments:
        - `rect`:Rectangle
        - `item`:String
        - `title`:String
        - `step`:Integer
        """
        try:

            oICModel = None
            ##print 'ss'
            #print dir(self.xN)

            ##xNameCont=dialog

            ccTabPage = self.tab.getControl(self.CC_TAB_NAME)
            ##TODO: original was "ImageControl" + item
            if (self.xNameCont.hasByName("ImageControl" + item)):
                try:
                    xImageControl = self.dialog.\
                      getControl("ImageControl" + item)

                    if (xImageControl != None):
                        xImageControl.dispose()

                        #TODO: original was "ImageControl" +item
                    self.xNameCont.removeByName(item)

                except Exception, ex:
                    print "Exception in LicenseChooserDialog." + \
                      "__setInfoImage- Inside the If statement"
                    print type(ex)
                    print ex
                    raise ex

            oICModel = self.ccTab.createInstance(
                "com.sun.star.awt.UnoControlImageControlModel")
            xGraphic = None

            path = "vnd.sun.star.extension://org.creativecommons." + \
              "libreoffice.CcLoAddin/images/information.png"
            xGraphic = self.__getGraphic(path)
            #print "xGraphic: "+xGraphic

            ##TODO: was (short)0
            oICModel.setPropertyValue("Border",  0)
            oICModel.setPropertyValue("Height", rect.Height)
            oICModel.setPropertyValue("Name", "ImageControl" + item)
            oICModel.setPropertyValue("PositionX", rect.X)
            oICModel.setPropertyValue("PositionY", rect.Y)
            oICModel.setPropertyValue("Width", rect.Width)
            oICModel.setPropertyValue("Step", step)

            self.ccTab.insertByName("ImageControl" + item, oICModel)
            oICModel.setPropertyValue("HelpText", title)
            oICModel.setPropertyValue("Graphic", xGraphic)

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__setInfoImage'
            traceback.print_exc()
            #raise ex

    # def __getSelectedLicense(self, ):
    #     """
    #     """
    #     try:
    #         pass
    #     except Exception, ex:
    #         print 'Exception in LicenseChooserDialog.__getSelectedLicense'
    #         print type(ex)
    #         print ex

    #     return None

    def __setCRadioButtonValue(self, controlName, bValue):
        """ Set the value of the given radio button

        Arguments:
        - `controlName`: String
        - `bValue`: Boolean
        """
        try:
            xPSetList = self.ccTab.getByName(controlName)
            if bValue:
                xPSetList.setPropertyValue("State", 1)
            else:
                xPSetList.setPropertyValue("State", 0)

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.__setCRadioButtonValue'
            traceback.print_exc()
            #raise ex

    def __setSelectedLicense(self, selected):
        """ update the user interface to match this selection

        Arguments:
        - `selected`:
        """

        self.__setCRadioButtonValue(self.RDO_ALLOW_COMERCIAL_YES,
                                    not selected.prohibitCommercial)

        self.__setCRadioButtonValue(self.RDO_ALLOW_COMERCIAL_NO,
                                    selected.prohibitCommercial)

        self.__setCRadioButtonValue(self.RDO_ALLOW_MODIFICATIONS_YES,
                                    (selected.allowRemix and
                                     not selected.requireShareAlike))

        self.__setCRadioButtonValue(self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE,
                                    selected.requireShareAlike)

        self.__setCRadioButtonValue(self.RDO_ALLOW_MODIFICATIONS_NO,
                                    not selected.allowRemix)

        self.selectedJurisdiction = selected.jurisdiction

        self.updateSelectedLicense()

    def __Array(self, *args):
        """This is just sugar coating so that code from OOoBasic which
        contains the Array() function can work perfectly in python."""

        tArray = ()
        for arg in args:
            tArray += (arg,)

        return tArray

    def __AddTabPage(self, tab, name, title):
        """
        Arguments:
        - `tab`:
        - `name`:
        - `title`:
        """

        args = uno.createUnoStruct("com.sun.star.beans.NamedValue")
        args.Name = "Title"
        args.Value = title
        tab_model = tab.getModel()

        page_model = tab_model.createInstance("com.sun.star.awt.UnoPageModel")
        tab_model.insertByName(name, page_model)
        n = len(tab_model.getElementNames())
        tab.setTabProps(n, self.__Array(args))
        return page_model

    def showDialog(self):
        """Shows the LicenseChooserDialog

        Arguments:
        - `self`:
        """
        try:
            #create the dialog model and set the properties
            self.dlgLicenseSelector = self.xMultiComponentFactory.\
              createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialogModel", self.m_xContext)

            ###
            #The following part was changed from the origianl code
            ###
            #rect=self.__makeRectangle(100, 80, 210, 275)

            self.dlgLicenseSelector.Width = 210
            self.dlgLicenseSelector.Height = 275
            self.dlgLicenseSelector.PositionX = 100
            self.dlgLicenseSelector.PositionY = 80

            self.dlgLicenseSelector.Title = "Sharing & Reuse Permissions"
            self.dlgLicenseSelector.Step = 1

            #create the dialog control and set the model
            self.dialog = self.xMultiComponentFactory.\
              createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialog", self.m_xContext)
            # xControl = dialog
            #xControlModel =  dlgLicenseSelector

            self.dialog.setModel(self.dlgLicenseSelector)

            ##--due to the following commment the following code in
            ##__createAWTControl is not run

            ##if ( not self.dlgLicenseSelector.hasByName(ctrlName)):
            ##    self.dlgLicenseSelector.insertByName(ctrlName,xpsProperties)

            #xPSetDialog=self.__createAWTControl(self.dlgLicenseSelector, "cc",
            # None,rect,1)
            #xPSetDialog.setPropertyValue("Title",
            #"Sharing & Reuse Permissions")

            #--
            ###
            ###

            #get the name container for the dialog for inserting other elements
            self.xNameCont = self.dlgLicenseSelector

            ######
            #Tab code
            ######
            self.tab_model = \
              self.dlgLicenseSelector.\
              createInstance("com.sun.star.awt.UnoMultiPageModel")

            self.tab_model.PositionX = 0
            self.tab_model.PositionY = 0
            self.tab_model.Width = 210  # 206
            self.tab_model.Height = 260  # 243

            self.dlgLicenseSelector.insertByName("tab", self.tab_model)
            toolkit = self.m_xContext.\
              getServiceManager().createInstanceWithContext(
            "com.sun.star.awt.Toolkit", self.m_xContext)
            self.dialog.createPeer(toolkit, None)

            self.tab = self.dialog.getControl("tab")
            self.ccTab = self.\
              __AddTabPage(self.tab, self.CC_TAB_NAME, "Creative Commons")
            self.cc0Tab = self.__AddTabPage(self.tab, self.CC0_TAB_NAME, "CC0")
            self.pdTab = self.\
              __AddTabPage(self.tab, self.PD_TAB_NAME, "Public Domain")
            self.metadataTab = self.\
              __AddTabPage(self.tab, self.METADATA_TAB_NAME, "Metadata")

            # # ##Create Tabs
            self.__crateCC0LicenseTab()
            self.__createCCLicenseTab()
            self.__cratePDLicenseTab()
            self.__createMetadataTab()

            ##create the button model - FAQ and set the properties
            faqButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            xPSetFaqButton = self.__createAWTControl(faqButton, self.BTN_FAQ,
                None, self.__makeRectangle(70, 260, 40, 14), 0,
                self.dlgLicenseSelector)
            xPSetFaqButton.setPropertyValue("DefaultButton", True)
            xPSetFaqButton.setPropertyValue("Label", self.faqButtonLabel)
            #self.dlgLicenseSelector.insertByName("ss",faqButton)
            ##create the button model - OK and set the properties
            finishButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            self.xPSetFinishButton = self.__createAWTControl(finishButton,
                                                             self.BTN_OK,
                None, self.__makeRectangle(115, 260, 40, 14), 0,
                self.dlgLicenseSelector)
            self.xPSetFinishButton.setPropertyValue("DefaultButton", True)
            self.xPSetFinishButton.setPropertyValue("Label",
                                                    self.finishButtonLabel)

            ## create the button model - Cancel and set the properties
            cancelButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")
            xPSetCancelButton = self.__createAWTControl(cancelButton,
                                                        self.BTN_CANCEL,
                None, self.__makeRectangle(160, 260, 40, 14), 0,
                self.dlgLicenseSelector)
            xPSetCancelButton.setPropertyValue("Name", self.BTN_CANCEL)
            xPSetCancelButton.setPropertyValue("Label", self.cancelButtonLabel)

            ##add an action listener to the Previous button control
            #xControlCont=self.dialog
            cmbJList = self.tab.\
              getControl(self.CC_TAB_NAME).getControl(self.CMB_JURISDICTION)
            #TODO:Done- Add the items to the cmbJList properly (Line 227-230)
            self.jurisdictionList = jurisdictions()
            #TODO-seems like lines 229-230 are unnecessary

            self.juriList = jurisdictions()

            count = 0

            ##add Unported, which isn't actually a jurisdiction'
            cmbJList.addItem("Unported", count)
            count += 1

            #TODO:Done- add line 236-239
            for uri in self.juriList:

                title = Jurisdiction(uri).getTitle()
                cmbJList.addItem(title, count)
                count += 1

            ##add a bogus place-holder for Unported in the JurisdictionList to
            ##ensure indices match up when determining the item
            ##selectedJurisdiction

            self.juriList.insert(0, None)

            ##Pre-select Unported
            #TODO: bit different from the origianl code
            cmbJList.selectItemPos(0, True)
            cmbJList.makeVisible(0)

            # ##listen for license selection changes
            # #self.__addListners("XCheckBox", None,None)
            # #self.__addListners("XRadioButton",None,None)
            # #self.__addListners("XButton",None,None)

            self.__addListners("XRadioButton", self.RDO_ALLOW_COMERCIAL_YES,
                             UpdateLicenseListner(self))
            self.__addListners("XRadioButton", self.RDO_ALLOW_COMERCIAL_NO,
                               UpdateLicenseListner(self))
            self.__addListners("XRadioButton",
                               self.RDO_ALLOW_MODIFICATIONS_YES,
                               UpdateLicenseListner(self))
            self.__addListners("XRadioButton",
                               self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE,
                               UpdateLicenseListner(self))
            self.__addListners("XRadioButton", self.RDO_ALLOW_MODIFICATIONS_NO,
                               UpdateLicenseListner(self))

            cmbJList.addItemListener(JurisdictionSelectListener(self))

            self.__addListners("XCheckBox",
                               self.CHK_WAIVE, AcceptWaiveListener(self),
                               self.CC0_TAB_NAME)
            self.__addListners("XCheckBox",
                               self.CHK_YES_CC0, AcceptListener(self),
                               self.CC0_TAB_NAME)
            self.__addListners("XCheckBox",
                               self.CHK_YES_PD, AcceptListener(self),
                               self.PD_TAB_NAME)

            ##add an action listeners to buttons

            self.__addListners("XButton",
                               self.BTN_FAQ, FaqClickListener(self,
                                                             self.m_xContext))
            self.__addListners("XButton", self.BTN_OK, OKClickListener(self))
            self.__addListners("XButton",
                               self.BTN_CANCEL, CancelClickListener(self))

            #add listners to tabs
            self.__addListners("XTabPage", None, TabListener(self),
                               self.CC0_TAB_NAME)

            ##Set the initial license
            docProperties = self.xCurrentComponent.getDocumentInfo()
            if (docProperties.getPropertySetInfo().\
                hasPropertyByName("license")):
                self.__setSelectedLicense(
                    License(str(docProperties.getPropertyValue("license"))))
            else:
                self.__setSelectedLicense(
                    License("http://creativecommons.org/licenses/by/3.0/"))

            ##create a peer
            toolkit = self.xMultiComponentFactory.createInstanceWithContext(
                "com.sun.star.awt.Toolkit", self.m_xContext)
            self.dialog.setVisible(False)
            self.dialog.createPeer(toolkit, None)

            ##TODO: all the following info images needs
            ##internationalization support

            self.__setInfoImage(
                self.__makeRectangle(55, 58, 9, 10),
                self.RDO_ALLOW_COMERCIAL_YES,
                                ("The licensor permits others to copy,"
                                 "distribute, display, and perform the work,"
                                 "including for commercial purposes."), 1)

            self.__setInfoImage(self.__makeRectangle(55, 73, 9, 10),
                                self.RDO_ALLOW_COMERCIAL_NO,
                                ("The licensor permits others to copy,"
                                 "distribute, display, and perform the work"
                                 " for non-commercial purposes only"), 1)

            self.__setInfoImage(self.__makeRectangle(55, 103, 9, 10),
                                self.RDO_ALLOW_MODIFICATIONS_YES,
                                ("The licensor permits others to copy, "
                                 "\ndistribute, display and perform the work, "
                                 "\nas well as make derivative works based"
                                 " on it."), 1)

            self.__setInfoImage(self.__makeRectangle(125, 118, 9, 10),
                                self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE,
                                ("The licensor permits others to distribute"
                                 " derivative works "
                                 "\nonly under the same license or one "
                                 "compatible "
                                 "\nwith the one that governs the "
                                 "licensor's work."), 1)

            self.__setInfoImage(self.__makeRectangle(55, 133, 9, 10),
                                self.RDO_ALLOW_MODIFICATIONS_NO,
                                ("The licensor permits others to copy, "
                                 "\ndistribute and transmit only unaltered"
                                 " copies of the "
                                 "\nwork - not derivative works based"
                                 " on it."), 1)

            self.__setInfoImage(self.__makeRectangle(155, 148, 9, 10),
                                self.CMB_JURISDICTION,
                                ("Use the option \"Unported\" if you "
                                 "desire a license using "
                                 "\nlanguage and terminology from "
                                 "international treaties. "), 1)

            ##TODO: Implement the Territories correctly- Line 314
            #relative path to file
            rPath =\
               ".." + os.path.sep + ".." + os.path.sep + ".." + os.path.sep +\
                "license" + os.path.sep + "rdf" + os.path.sep + "territory"
            path = os.path.join(
                os.path.dirname(__file__), rPath)
            f = open(path)

            territoryList = f.read().rstrip().split('\n')
            self.trritories = ()
            #add the terrotories to the data structure
            for trr in territoryList:
                self.trritories += (trr,)
            #trritories+=('1',)
            #trritories+=('2',)
            cc0TabPage = self.tab.getControl(self.CC0_TAB_NAME)
            self.cmbTList = cc0TabPage.getControl(self.CMB_TERRITORY)
            ##TODO: was (short)
            self.cmbTList.addItem("",  0)
            ##TODO: was (short)
            self.cmbTList.addItems(self.trritories,  1)
            ##TODO: was (short)
            self.cmbTList.selectItemPos(0, True)
            ##TODO: was (short)
            self.cmbTList.makeVisible(0)

            self.cmbTList.addItemListener(TerritorySelectListener(self))
            ##execute the dialog
            self.dialog .setVisible(True)
            self.dialog .execute()

            ##dispose the dialog
            self.dialog .dispose()

        except Exception, ex:
            print "Exception in LicenseChooserDialog.showDialog:"
            traceback.print_exc()

    def setLicenseType(self, type):
        """Set license type according to the tab selected.

        Arguments:
        - `type`: Integer
        """

        btnArray = [self.BTN_CC, self.BTN_CC0, self.BTN_PUBLICDOMAIN]

        try:
            if (type != 1):
                self.xPSetFinishButton.setPropertyValue("Enabled", False)
            else:
                self.xPSetFinishButton.setPropertyValue("Enabled", True)

            self.cc0Tab.getByName(self.CHK_YES_CC0).\
              setPropertyValue("Enabled", False)
            self.cc0Tab.getByName(self.TXT_LEGAL_CODE_CC0).setPropertyValue(
                "Enabled", False)
            ##TODO: was (short)0
            self.cc0Tab.getByName(self.CHK_WAIVE).setPropertyValue(
                "State", 0)
            self.cc0Tab.getByName(self.CHK_YES_CC0).\
              setPropertyValue("State", 0)
            self.cc0Tab.getByName(self.CMB_TERRITORY).\
              setPropertyValue("Enabled", False)

            ##TODO: was (short)
            self.cmbTList.selectItemPos(0, True)

            self.pdTab.getByName(self.CHK_YES_PD).setPropertyValue(
                "State", 0)

            ##Note: It seems like that self.dlgLicenseSelector and
            ##xPSetDialog are equal
            self.dlgLicenseSelector.setPropertyValue("Step", type)

        except Exception, ex:
            print 'Exception in LicenseChooserDialog.setLicenseType'
            traceback.print_exc()
            raise ex

    def setSelectedTerritory(self, selection):
        """Sets the selected territory

        Arguments:
        - `selection`:Integer
        """
        if (selection > 0):
            self.selectedTerritory = self.trritories[selection - 1]

        else:
            self.selectedTerritory = None

    def getSelectedLicense(self, ):
        """Returns the selected license
        """
        try:
            #retrieve the Document for the issued license
            licenseChooser = Chooser()

            type = self.dlgLicenseSelector.getPropertyValue("Step")

            if (type == 2):
                #TODO:From where self.selectedTerritory set??
                return licenseChooser.selectPDTools(self.selectedTerritory, 2)
            elif (type == 3):
                return licenseChooser.selectPDTools(None, 3)
            else:
                return licenseChooser.selectLicense(
                    self.__getRadioButtonValue(
                        self.RDO_ALLOW_MODIFICATIONS_YES)
                    or self.__getRadioButtonValue(
                        self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE),
                    self.__getRadioButtonValue(self.RDO_ALLOW_COMERCIAL_NO),
                    self.__getRadioButtonValue(
                        self.RDO_ALLOW_MODIFICATIONS_SHARE_ALIKE),
                    self.selectedJurisdiction)

        except Exception, ex:
            traceback.print_exc()

        return None
