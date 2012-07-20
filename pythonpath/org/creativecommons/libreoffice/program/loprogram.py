#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from com.sun.star.beans import IllegalTypeException
from com.sun.star.beans import NotRemoveableException
from com.sun.star.beans import PropertyExistException
from com.sun.star.beans import PropertyVetoException
from com.sun.star.beans import UnknownPropertyException
from com.sun.star.lang import WrappedTargetException

#from com.sun.star.rdf.URI import URI
#import com.sun.star.rdf.URI
#import com.sun.star.rdf.Literal

from com.sun.star.beans.PropertyAttribute import MAYBEVOID,REMOVEABLE

from org.creativecommons.libreoffice.program.constants import Constants
from org.creativecommons.license.license import License

class LoProgram(object):
    """
    """
    
    def __init__(self, component, m_xContext):
        """
        
        Arguments:
        - `component`: XComponent
        - `m_xContext`: XComponentContext
        """
        
        self.component = component
        self.m_xContext = m_xContext
        self.xMultiComponentFactory=self.m_xContext.getServiceManager()

    def getDocumentLicense(self, ):
        """Return the License for the active document, if it exists 
        """

        #xDocumentInfoSupplier=self.component
        docInfo=self.component.getDocumentInfo()
        #docProperties=docInfo

        if ((docInfo.getPropertySetInfo().hasPropertyByName(
                Constants.LICENSE_URI)) and 
            (docInfo.getPropertySetInfo().hasPropertyByName(
                Constants.TERRITORY))):
            try:
                return License(docInfo.getPropertyValue(Constants.LICENSE_URI),
                        docInfo.getPropertyValue(Constants.TERRITORY))

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
                Constants.LICENSE_URI)):
            try:
                return License(docInfo.getPropertyValue(Constants.LICENSE_URI))
            
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

        return None


    def setDocumentLicense(self, license):
        """Set the license meta data.
    
        Arguments:
        - `license`:License
        """
        
        #xDocumentInfoSupplier=self.component
        docInfo=self.component.getDocumentInfo()
        #docProperties=docInfo

        
        
        #docPropertyContainer=docInfo
        if (not docInfo.getPropertySetInfo().hasPropertyByName(
                Constants.LICENSE_URI)):
            
            #add the necessary properties to this document
            try:
                docInfo.addProperty(Constants.LICENSE_URI,
                                    MAYBEVOID, "")
                docInfo.addProperty(Constants.LICENSE_NAME,
                                    MAYBEVOID, "")
                
                

            except IllegalArgumentException, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                print ex
                print type(ex)
                #raise ex

            except PropertyExistException, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                print ex
                print type(ex)
                #raise ex
            
            except IllegalTypeException, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                print ex
                print type(ex)
                #raise ex


        #end of if
        try:
            
                        
            docInfo.setPropertyValue(Constants.LICENSE_URI, 
                                     license.license_uri)
            docInfo.setPropertyValue(Constants.LICENSE_NAME, license.getName())

            
            if (license.territory is not None):
            
                if(not docInfo.getPropertySetInfo().hasPropertyByName(
                    Constants.TERRITORY)):

                    docInfo.addProperty(Constants.TERRITORY,
                                        REMOVEABLE, "")
                docInfo.setPropertyValue(Constants.TERRITORY, 
                                         license.territory)

            elif(docInfo.getPropertySetInfo().hasPropertyByName(
                Constants.TERRITORY)):

            
                try:
                    docInfo.removeProperty(Constants.TERRITORY)
                    
                except NotRemoveableException, ex:
                    print "Exception in OOoProgram.setDocumentLicense: "
                    print ex
                    print type(ex)
                    #raise ex

            
        except PropertyExistException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex
        
        except IllegalTypeException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        except IllegalArgumentException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        except UnknownPropertyException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        except PropertyVetoException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        except WrappedTargetException, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        #RDF metadata
        #TODO: add territory and title to RDF
        
        try:
            author=None
            title=None

            try:
                author=docInfo.getPropertyValue("Author")
                title=docInfo.getPropertyValue("Title")
            except Exception, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                print ex
                print type(ex)
                #raise ex

            #xDMA=self.component
            try:
                #Note: High chance of an error
                                  
                #self.component.removeMetadataFile(URI.create(self.m_xContext,self.component.getNamespace()+"meta.rdf"))
                
                self.component.removeMetadataFile(
                    self.__createUri(self.component.Namespace+"meta.rdf"))
            except Exception, ex:
                #TODO: remove the stack trace
                print "Exception in OOoProgram.setDocumentLicense:"+ \
                  "-ignored exception"
                print ex
                print type(ex)
                #raise ex
                      
            value=self.component.StringValue
            xType=self.__createUri(value)

                       
            xTypeRights = self.__createUri(
                "http://purl.org/dc/elements/1.1/rights")
            
            xGraphName = self.component.addMetadataFile(
                "meta.rdf", (xTypeRights,));
                       
            xGraph = self.component.getRDFRepository().getGraph(xGraphName)

            nodeRights = self.__createUri(
                "http://purl.org/dc/elements/1.1/rights")
            #TODO: Line 191- Implement correctly
            valRights =self.__createLiteral("-ASCII C- " + author
                    + " licensed to the public under the " + \
                    license.getName() + " license")
            xGraph.addStatement(xType, nodeRights, valRights)

            nodeLicense = self.__createUri("http://purl.org/dc/terms/license")
            valLicense = self.__createLiteral( license.license_uri)
            xGraph.addStatement(xType, nodeLicense, valLicense)

            noderightsHolder =self.__createUri(
                "http://purl.org/dc/terms/rightsHolder")
            valrightsHolder = self.__createLiteral(author)
            xGraph.addStatement(xType, noderightsHolder, valrightsHolder)
                       
                
        except Exception, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        
    def __createUri(self,value ):
        """
        """
        
        metaURI=self.xMultiComponentFactory.\
            createInstanceWithArgumentsAndContext(
                "com.sun.star.rdf.URI",(value,),self.m_xContext)
        return metaURI
            

    def __createLiteral(self, value):
        """
    
        Arguments:
        - `value`:String
        """
        literal=self.xMultiComponentFactory.\
            createInstanceWithArgumentsAndContext(
                "com.sun.star.rdf.Literal",(value,),self.m_xContext)

        return literal
        
        
