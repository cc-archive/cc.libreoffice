#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import sys

##Load our rdflib files if the user already has a
#local copy of rdflib installed
bundle_path = None
for part in sys.path:
    if part.count("uno_packages") and part.count("cache") and part.\
      count("pythonpath"):
        bundle_path = part
        break
if bundle_path:
    addTo = 1
    sys.path.append(sys.path[addTo])
    sys.path.insert(addTo, bundle_path)


import traceback

import unohelper

from com.sun.star.frame import XDispatch, XDispatchProvider
from com.sun.star.lang import XInitialization, XServiceInfo

from org.creativecommons.libreoffice.ui.license.licensechooserdialog \
   import LicenseChooserDialog

#from org.creativecommons.license.store import Store
from org.creativecommons.libreoffice.program.writer import Writer
from org.creativecommons.libreoffice.program.calc import Calc
from org.creativecommons.libreoffice.program.draw import Draw
#from org.creativecommons.license.chooser import Chooser

from com.sun.star.task import XJob


SERVICE_NAME = "com.sun.star.frame.ProtocolHandler"
IMPLE_NAME = "org.creativecommons.openoffice.CcOOoAddin"


def createInstance(ctx):
    """Used to load the 3rd party libraries to the extension
    """
    #import org.creativecommons.license.store
    #return org.creativecommons.license.store.Store()
    pass


class CcLoAddin(unohelper.Base, XInitialization, XServiceInfo,
              XDispatchProvider, XDispatch, XJob):

    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.frame = None
        self.initialize(args)
        self.mxRemoteServiceManager = self.ctx.getServiceManager()

    ##A meyhod for testing purposes
    def testMethod(self,):
        """
        """
        print "in test method-CcOOoAddin"
        try:
            #chs=Chooser()
            # print "k"
            # self.xMultiComponentFactory=self.ctx.ServiceManager
            # URI=self.xMultiComponentFactory.createInstanceWithArguments(
            #"com.sun.star.rdf.URI",("http://purl.org/dc/elements/1.1/rights"))
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
        """Inserts the relevant license statement to the document
           on menu item click
        """
        wrapper = self.getProgramWrapper()
        try:
            if (wrapper.getDocumentLicense() is None):
                self.selectLicense()

            wrapper = self.getProgramWrapper()
            wrapper.insertVisibleNotice()

        except Exception, ex:
            traceback.print_exc()

    def updateCurrentComponent(self, ):
        """Updates the Desktop current component in case of opening, creating
           or swapping to other document
        """
        ret = None

        try:

            #TODO: original code had mxComponentContext,but it seems "Null"
            desktop = self.mxRemoteServiceManager.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", self.ctx)
            ret = desktop.getCurrentComponent()
            self.xMultiComponentFactory = self.ctx.getServiceManager()

        except Exception, ex:
            print "Exception in CcOOoAddin.updateCurrentComponent: "
            traceback.print_exc()

        self.xCurrentComponent = ret

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

    def selectLicense(self):
        """Shows the license chooser dialog for the user to select a
           license
        """

        try:
            ##TODO: following part was not Implemented
            # if (mxRemoteServiceManager == null) {
            #     System.out.println("not available");
            #     return;
            # }

            self.updateCurrentComponent()

            #Create the dialog for license selection
            dialog = LicenseChooserDialog(self, self.ctx)
            dialog.showDialog()

            if not dialog.cancelled:
                #retrieve the selected License
                selected = dialog.getSelectedLicense()
                document = self.getProgramWrapper()

                #store the license information in the document
                document.setDocumentLicense(selected)
                ##TODO: Add the line 290
                wrapper = self.getProgramWrapper()
                wrapper.updateVisibleNotice()

        except Exception, ex:
            print "Exception in CcOOoAddin.selectLicense: "
            traceback.print_exc()

    def getProgramWrapper(self, ):
        """Returns a class corresponding to the currently
        selected document
        """
        #xServiceInfo=self.xCurrentComponent

        if (self.xCurrentComponent.supportsService(
                "com.sun.star.sheet.SpreadsheetDocument")):
            return Calc(self.xCurrentComponent, self.ctx)

        elif (self.xCurrentComponent.supportsService(
                "com.sun.star.text.TextDocument")):
            return  Writer(self.xCurrentComponent, self.ctx)

        elif (self.xCurrentComponent.supportsService(
                "com.sun.star.presentation.PresentationDocument")):
            return Draw(self.xCurrentComponent, self.ctx)

        elif (self.xCurrentComponent.supportsService(
                "com.sun.star.drawing.DrawingDocument")):
            return Draw(self.xCurrentComponent, self.ctx)

        return None

    def execute(self, args):
        """
    Arguments:
    - `args`:
    """
        from org.creativecommons.license.store import RdfLoaderThread
        RdfLoaderThread().start()

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    CcLoAddin,
    IMPLE_NAME,
    (SERVICE_NAME,),)

# g_ImplementationHelper.addImplementation( \
#         createInstance, "org.creativecommons.license.store",
#         (SERVICE_NAME,),)
