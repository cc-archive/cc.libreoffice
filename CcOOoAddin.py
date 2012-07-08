#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback

import unohelper

from com.sun.star.frame import XDispatch, XDispatchProvider
from com.sun.star.lang import XInitialization, XServiceInfo


from org.creativecommons.license.Store import Store


#import org.creativecommons.libs.rdflib.graph #import Graph
#import org.creativecommons.libs.rdflib.term #import URIRef

#from com.sun.star.uno import AnyConverter 
#import com.sun.star.uno.AnyConverter
#from com.sun.star.rdf import URI


#from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram
from org.creativecommons.libreoffice.program.Writer import Writer
from org.creativecommons.libreoffice.program.Calc import Calc
from org.creativecommons.libreoffice.program.Draw import Draw
#import rdflib

from org.creativecommons.license.Chooser import Chooser


SERVICE_NAME = "com.sun.star.frame.ProtocolHandler"
IMPLE_NAME = "org.creativecommons.openoffice.CcOOoAddin"

def createInstance(ctx):
    import org.creativecommons.license.Store
    return org.creativecommons.license.Store.Store()


class Example(unohelper.Base, XInitialization, XServiceInfo,
              XDispatchProvider, XDispatch):

    
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.frame = None
        self.initialize(args)
        self.mxRemoteServiceManager=self.ctx.getServiceManager()


    ##A meyhod for testing purposes
    def testMethod(self,):
        """
        """
        print "in test method-CcOOoAddin"
        try:
            #chs=Chooser()
            # print "k"
            # self.xMultiComponentFactory=self.ctx.ServiceManager
            
            # URI=self.xMultiComponentFactory.createInstanceWithArguments("com.sun.star.rdf.URI",("http://purl.org/dc/elements/1.1/rights"))
            # print
            # print dir(URI)
            # print
            # print URI.ImplementationName
            # print URI.LocalName
            # print URI.Namespace
            # print URI.StringValue
            # u=URI.create("http://purl.org/dc/elements/1.1/rights")
            
            #chs.selectPDTools("United States",2)
            #chs.selectLicense(True,False,False,None)
            pass
            
        except Exception, ex:
            # print "Exception in CcOOoAddin.TestMethod: "
            # print ex
            # 
            traceback.print_exc()
            #
        
    def insertStatement(self, ):
        """
        """
        wrapper=self.getProgramWrapper()
        try:
            if (wrapper.getDocumentLicense() is not None):
                self.selectLicense()

            wrapper=self.getProgramWrapper()
            wrapper.insertVisibleNotice()

        except Exception, ex:
            traceback.print_exc()
            
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
            traceback.print_exec()
            
            

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

            self.updateCurrentComponent()

            if url.Path == "SelectLicense":
                print "SelectLicense"
                self.selectLicense()

            elif url.Path == "InsertStatement":
                print 'calling selectLicense'

                #Module.testMethod()
                #self.testMethod()
                self.insertStatement()
                

            elif url.Path == "InsertPictureFlickr":
                print "InsertPictureFlickr"
                ##Test code
                self.testMethod()

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
        print "Test"
        pass 




    def selectLicense(self):

        try:
            ##TODO: following part was not Implemented
            # if (mxRemoteServiceManager == null) {
            #     System.out.println("not available");
            #     return;
            # }

            print "Entered"
            self.updateCurrentComponent()

            #Create the dialog for license selection
            dialog=LicenseChooserDialog(self,self.ctx)
            dialog.showDialog()

            print "entering"
            if not dialog.cancelled:
                #retrieve the selected License
                selected = dialog.getSelectedLicense()
                print "1"
                document = self.getProgramWrapper()
                print "2"
                print "license :"+selected.license_uri
                #store the license information in the document
                document.setDocumentLicense(selected)
                ##TODO: Add the line 290
                print "3"
                wrapper=self.getProgramWrapper()
                wrapper.updateVisibleNotice()
                
                
            print "exiting"
        except Exception, ex:
            print "Exception in CcOOoAddin.selectLicense: "
            traceback.print_exc() 

    def getProgramWrapper(self, ):
        """
        """
        #xServiceInfo=self.xCurrentComponent

        if (self.xCurrentComponent.supportsService("com.sun.star.sheet.SpreadsheetDocument")):
            return Calc(self.xCurrentComponent,self.ctx)
            
        elif (self.xCurrentComponent.supportsService("com.sun.star.text.TextDocument")):
            return  Writer(self.xCurrentComponent,self.ctx)
            
            
        elif (self.xCurrentComponent.supportsService("com.sun.star.presentation.PresentationDocument")):
            return Draw(self.xCurrentComponent,self.ctx)

        elif (self.xCurrentComponent.supportsService("com.sun.star.drawing.DrawingDocument")):
            return Draw(self.xCurrentComponent,self.ctx)

        return None


    
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

g_ImplementationHelper.addImplementation( \
	createInstance,"org.creativecommons.license.Store",
        (SERVICE_NAME,),)

from org.creativecommons.libreoffice.ui.license.LicenseChooserDialog import LicenseChooserDialog
