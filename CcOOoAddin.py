import unohelper

from com.sun.star.frame import XDispatch, XDispatchProvider
from com.sun.star.lang import XInitialization, XServiceInfo

from org.creativecommons.libreoffice.ui.license.LicenseChooserDialog import LicenseChooserDialog
import module.module1 as Module


SERVICE_NAME = "com.sun.star.frame.ProtocolHandler"
IMPLE_NAME = "org.creativecommons.openoffice.CcOOoAddin"


class Example(unohelper.Base, XInitialization, XServiceInfo,
              XDispatchProvider, XDispatch):

    
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.frame = None
        self.initialize(args)

    def supportsService(self, name):
        return (name == SERVICE_NAME)

    def getImplementationName(self):
        return IMPLE_NAME

    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)

    # XInitialization
    def initialize(self, args): 
        if args: 
            self.frame = args[0] 
        
    # XDispatchProvider 
    def queryDispatch(self, url, name, flags):
         
        if url.Protocol == "org.creativecommons.openoffice.ccooo:": 
            return self 
        return None 
    
    def queryDispatches(self, req): 
        pass 
    
    # XDispatch 
    def dispatch(self, url, args):

        if url.Protocol == "org.creativecommons.openoffice.ccooo:":

            #this.updateComponent()

            if url.Path == "SelectLicense":
                print "SelectLicense"

            elif url.Path == "InsertStatement":
                print 'calling selectLicense'

                Module.testMethod()
                lcd=LicenseChooserDialog(self, self.ctx)
                #print type(lcd)
                #print dir(lcd)
                lcd.showDialog()
                

            elif url.Path == "InsertPictureFlickr":
                print "InsertPictureFlickr"

            elif url.Path == "InsertOpenClipArt":
                print "InsertOpenClipArt"

            elif url.Path == "InsertWikimediaCommons":
                print "InsertWikimediaCommons"

            elif url.Path == "InsertPicasa":
                print "InsertPicasa"
    
    def addStatusListener(self, control, url): 
        pass 
    
    def removeStatusListener(self, control, url): 
        pass 
    
    def do(self): 
        pass 

    def selectLicense(self):

        #This code fragment creates a sample window
        oDialogModel = self.ctx.ServiceManager.createInstanceWithContext( 
            "com.sun.star.awt.UnoControlDialogModel", self.ctx )

        # Initialize the dialog model's properties.
        oDialogModel.PositionX = 200
        oDialogModel.PositionY = 200
        oDialogModel.Width = 200
        oDialogModel.Height = 200
        oDialogModel.Title = "Title"


        oDialogControl = self.ctx.ServiceManager.createInstanceWithContext( 
            "com.sun.star.awt.UnoControlDialog", self.ctx )
        oDialogControl.setModel( oDialogModel )
        print "setModel Ok"

        #segfault on next line
        oDialogControl.setVisible( True )
        print "visible"
        oDialogControl.execute()
        print "execute"
        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( 
    Example, 
    IMPLE_NAME, 
    (SERVICE_NAME,),)
