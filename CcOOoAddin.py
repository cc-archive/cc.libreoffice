#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

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
        self.mxRemoteServiceManager=self.ctx.getServiceManager()
        

    def updateCurrentComponent(self, ):
        """Updates the Desktop current component in case of opening, creating or swapping
        to other document
        """
        ret=None

        try:

            #TODO: original code had mxComponentContext,but it seems "Null"
            desktop = self.mxRemoteServiceManager.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", self.ctx)
            ret = desktop.getCurrentComponent()
            self.xMultiComponentFactory=self.ctx.getServiceManager()
            
            
        except Exception, ex:
            print "Exception in CcOOoAddin.updateCurrentComponent: "
            print ex
            print type(ex)
            raise ex

        self.xCurrentComponent=ret

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
                self.selectLicense()

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

        try:
            ##TODO: following part was not Implemented
            # if (mxRemoteServiceManager == null) {
            #     System.out.println("not available");
            #     return;
            # }

            self.updateCurrentComponent()

        except Exception, ex:
            print "Exception in CcOOoAddin.selectLicense: "
            print ex
            print type(ex)
            raise ex
        ###################################################################
        ###################################################################

        # # #This code fragment creates a sample window
        # # oDialogModel = self.ctx.ServiceManager.createInstanceWithContext( 
        # #     "com.sun.star.awt.UnoControlDialogModel", self.ctx )

        # # # Initialize the dialog model's properties.
        # # oDialogModel.PositionX = 200
        # # oDialogModel.PositionY = 200
        # # oDialogModel.Width = 200
        # # oDialogModel.Height = 200
        # # oDialogModel.Title = "Title"


        # # oDialogControl = self.ctx.ServiceManager.createInstanceWithContext( 
        # #     "com.sun.star.awt.UnoControlDialog", self.ctx )
        # # oDialogControl.setModel( oDialogModel )
        # # print "setModel Ok"

        # # #segfault on next line
        # # oDialogControl.setVisible( True )
        # # print "visible"
        # # oDialogControl.execute()
        # # print "execute"

        #####################################################################
        ####################################################################
        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( 
    Example, 
    IMPLE_NAME, 
    (SERVICE_NAME,),)
