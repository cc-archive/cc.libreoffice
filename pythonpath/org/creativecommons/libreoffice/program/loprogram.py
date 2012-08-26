#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback

from com.sun.star.beans import IllegalTypeException
from com.sun.star.beans import NotRemoveableException
from com.sun.star.beans import PropertyExistException
from com.sun.star.beans import PropertyVetoException
from com.sun.star.beans import UnknownPropertyException
from com.sun.star.lang import WrappedTargetException
from com.sun.star.lang import IllegalArgumentException

#from com.sun.star.rdf.URI import URI
#import com.sun.star.rdf.URI
#import com.sun.star.rdf.Literal

from com.sun.star.beans.PropertyAttribute import MAYBEVOID, REMOVEABLE

from org.creativecommons.license.license import License


class LoProgram(object):
    """
    """

    CC_METADATA_IDENTIFIER = "http://creativecommons.org/ns#"
    LICENSE_URI = "license"
    LICENSE_NAME = "License Name"
    LANGUAGE_FILE_NAME = "language.properties"
    TERRITORY = "territory"

    def __init__(self, component, m_xContext):
        """
        Arguments:
        - `component`: XComponent
        - `m_xContext`: XComponentContext
        """
        self.component = component
        self.m_xContext = m_xContext
        self.xMultiComponentFactory = self.m_xContext.getServiceManager()

    def getDocumentLicense(self, ):
        """Return the License for the active document, if it exists
        """

        #xDocumentInfoSupplier=self.component
        docInfo = self.component.getDocumentInfo()
        #docProperties=docInfo

        if ((docInfo.getPropertySetInfo().hasPropertyByName(
                self.LICENSE_URI)) and
            (docInfo.getPropertySetInfo().hasPropertyByName(
                self.TERRITORY))):
            try:
                return License(docInfo.getPropertyValue(self.LICENSE_URI), {},
                        territory=docInfo.getPropertyValue(self.TERRITORY))

            except WrappedTargetException, ex:
                print "Exception in OOoProgram.getDocumentLicense: "
                print ex
                print type(ex)
                #raise ex
            except UnknownPropertyException, ex:
                print "Exception in OOoProgram.getDocumentLicense: "
                print ex
                print type(ex)
                #raise ex

        elif (docInfo.getPropertySetInfo().hasPropertyByName(
                self.LICENSE_URI)):
            try:
                return License(docInfo.getPropertyValue(self.LICENSE_URI), {})
            except WrappedTargetException, ex:
                print "Exception in OOoProgram.getDocumentLicense: "
                traceback.print_exc()
                #raise ex

            except UnknownPropertyException, ex:
                print "Exception in OOoProgram.getDocumentLicense: "
                traceback.print_exc()
                #raise ex

        return None

    def setDocumentLicense(self, license):
        """Set the license meta data.

        Arguments:
        - `license`:License
        """
        #xDocumentInfoSupplier=self.component
        docInfo = self.component.getDocumentInfo()
        #docProperties=docInfo
        #docPropertyContainer=docInfo
        if (not docInfo.getPropertySetInfo().hasPropertyByName(
                self.LICENSE_URI)):

            #add the necessary properties to this document
            try:
                docInfo.addProperty(self.LICENSE_URI,
                                    MAYBEVOID, "")
                docInfo.addProperty(self.LICENSE_NAME,
                                    MAYBEVOID, "")
                #iterate over metadata
                print "in LoProgram - mmm"
                for key, value in license.metadataDic.iteritems():
                    print key
                    print value
                    docInfo.addProperty(key,
                                    MAYBEVOID, value)
                    print docInfo.getPropertyValue(key)

            except IllegalArgumentException, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                traceback.print_exc()
                #raise ex

            except PropertyExistException, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                traceback.print_exc()
                #raise ex
            except IllegalTypeException, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                traceback.print_exc()
                #raise ex

        #end of if
        try:
            docInfo.setPropertyValue(self.LICENSE_URI,
                                     license.license_uri)
            docInfo.setPropertyValue(self.LICENSE_NAME, license.name)

            print
            if (license.territory is not None):
                if(not docInfo.getPropertySetInfo().hasPropertyByName(
                    self.TERRITORY)):

                    docInfo.addProperty(self.TERRITORY,
                                        REMOVEABLE, "")
                docInfo.setPropertyValue(self.TERRITORY,
                                         license.territory)

            elif(docInfo.getPropertySetInfo().hasPropertyByName(
                self.TERRITORY)):

                try:
                    docInfo.removeProperty(self.TERRITORY)
                except NotRemoveableException, ex:
                    traceback.print_exc()
                    print type(ex)
                    #raise ex

        except PropertyExistException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex
        except IllegalTypeException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex

        except IllegalArgumentException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex

        except UnknownPropertyException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex

        except PropertyVetoException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex

        except WrappedTargetException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex

        #RDF metadata
        #TODO: add territory and title to RDF
        try:
            author = None
            title = None

            try:
                author = docInfo.getPropertyValue("Author")
                title = docInfo.getPropertyValue("Title")
            except Exception, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                print ex
                print type(ex)
                #raise ex

            #xDMA=self.component
            try:
                self.component.removeMetadataFile(
                    self.__createUri(self.component.Namespace + "meta.rdf"))
            except Exception, ex:
                #TODO: remove the stack trace
                print "No graph data seems to exist"
                #raise ex

            value = self.component.StringValue
            xType = self.__createUri(value)

            xTypeRights = self.__createUri(
                "http://purl.org/dc/elements/1.1/rights")

            xGraphName = self.component.addMetadataFile(
                "meta.rdf", (xTypeRights,))

            xGraph = self.component.getRDFRepository().getGraph(xGraphName)

            nodeRights = self.__createUri(
                "http://purl.org/dc/elements/1.1/rights")
            #TODO: Line 191- Implement correctly
            valRights = self.__createLiteral("-ASCII C- " + author
                    + " licensed to the public under the " + \
                    license.name + " license")
            xGraph.addStatement(xType, nodeRights, valRights)

            nodeLicense = self.__createUri("http://purl.org/dc/terms/license")
            valLicense = self.__createLiteral(license.license_uri)
            xGraph.addStatement(xType, nodeLicense, valLicense)

            noderightsHolder = self.__createUri(
                "http://purl.org/dc/terms/rightsHolder")
            valrightsHolder = self.__createLiteral(author)
            xGraph.addStatement(xType, noderightsHolder, valrightsHolder)

        except Exception, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            traceback.print_exc()
            #raise ex

    def __createUri(self, value):
        """A helper method for rdf handling in LibreOffice.
        Creates a new uri
        """
        metaURI = self.xMultiComponentFactory.\
            createInstanceWithArgumentsAndContext(
                "com.sun.star.rdf.URI", (value,), self.m_xContext)
        return metaURI

    def __createLiteral(self, value):
        """"A helper method for rdf handling in LibreOffice.
        Creates a new Literal

        Arguments:
        - `value`:String
        """
        literal = self.xMultiComponentFactory.\
            createInstanceWithArgumentsAndContext(
                "com.sun.star.rdf.Literal", (value,), self.m_xContext)

        return literal
