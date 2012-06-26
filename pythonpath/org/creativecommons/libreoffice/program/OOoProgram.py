#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from com.sun.star.beans import IllegalTypeException
from com.sun.star.beans import NotRemoveableException
from com.sun.star.beans import PropertyExistException
from com.sun.star.beans import PropertyVetoException
from com.sun.star.beans import UnknownPropertyException
from com.sun.star.lang import WrappedTargetException

from com.sun.star.rdf import URI

#from com.sun.star.beans import PropertyAttribute

from org.creativecommons.libreoffice.program.IVisibleNotice import IVisibleNotice
from org.creativecommons.libreoffice.program.Constants import Constants
from org.creativecommons.license.License import License

class OOoProgram(IVisibleNotice):
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

    def getDocumentLicense(self, ):
        """Return the License for the active document, if it exists 
        """

        #xDocumentInfoSupplier=self.component
        docInfo=self.component.getDocumentInfo()
        #docProperties=docInfo

        if ((docInfo.getPropertySetInfo().hasPropertyByName(Constants.LICENSE_URI)) and (docInfo.getPropertySetInfo().hasPropertyByName(Constants.TERRITORY))):
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

        elif (docInfo.getPropertySetInfo().hasPropertyByName(Constants.LICENSE_URI)):
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
        if (not docInfo.getPropertySetInfo().hasPropertyByName(Constants.LICENSE_URI)):
            #add the necessary properties to this document
            try:
                docInfo.addProperty(Constants.LICENSE_URI,
                                    PropertyAttribute.MAYBEVOID, "")
                docInfo.addProperty(Constants.LICENSE_NAME,
                                    PropertyAttribute.MAYBEVOID, "")
                

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
            docInfo.setPropertyValue(Constants.LICENSE_URI, license.getLicenseUri())
            docInfo.setPropertyValue(Constants.LICENSE_NAME, license.getName())

            if (license.getTerritory() is not None):
                if(not docInfo.getPropertySetInfo().hasPropertyByName(Constants.TERRITORY)):

                    docInfo.addProperty(Constants.TERRITORY,
                                    PropertyAttribute.REMOVEABLE, "")
                docInfo.setPropertyValue(Constants.TERRITORY, license.getTerritory())

            elif(docInfo.getPropertySetInfo().hasPropertyByName(Constants.TERRITORY)):
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
                self.component.removeMetadataFile(URI.create(self.m_xContext,self.component.getNamespace()+"meta.rdf"))
            except Exception, ex:
                print "Exception in OOoProgram.setDocumentLicense: "
                print ex
                print type(ex)
                #raise ex
                
        except Exception, ex:
            print "Exception in OOoProgram.setDocumentLicense: "
            print ex
            print type(ex)
            #raise ex

        
        
        
            
