class LicenseChooserDialog():
    """Creates a new instance of LicenseChooserDialog
    """

    #TODO: add the global Constants support
    
    #Constants
    #BTN_CC = "btnCC"
    
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


    def showDialog(self):
        """Shows the LicenseChooserDialog 
        
        Arguments:
        - `self`:
        """
       

        #Constants
        BTN_CC = "btnCC"
       
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
            
            ###Tabs
            ##CC
            ccButton = self.dlgLicenseSelector.createInstance(
                "com.sun.star.awt.UnoControlButtonModel")

           
           
            
            xPSetCCButton = self.__createAWTControl(ccButton, BTN_CC,
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
            
            ##PD

            ##Create Tabs

            ##create the button model - FAQ and set the properties

            ##create the button model - OK and set the properties

            ## create the button model - Cancel and set the properties

            ##create the dialog control and set the model
            dialog = self.xMultiComponentFactory.createInstanceWithContext(
                "com.sun.star.awt.UnoControlDialog", self.m_xContext)
            # xControl = dialog
            #xControlModel =  dlgLicenseSelector
            
            dialog.setModel(self.dlgLicenseSelector)

            ##add an action listener to the Previous button control

            ##add Unported, which isn't actually a jurisdiction'

            ##add a bogus place-holder for Unported in the JurisdictionList to
            ##ensure indices match up when determining the item selectedJurisdiction

            ##Pre-select Unported

            ##listen for license selection changes

            ##add an action listeners to buttons

            ##Set the initial license

            ##create a peer

            
            ##execute the dialog
            dialog.setVisible(True)
            dialog.execute()
            

            ##dispose the dialog
            #dialog.dispose()
            
            
        except Exception,ex:
            print "Exception in LicenseChooserDialog.showDialog:"
            print ex

            #TODO: match the raising exception with the origianl source
            raise ex
