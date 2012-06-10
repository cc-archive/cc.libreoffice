#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from com.sun.star.beans import IllegalTypeException
from com.sun.star.beans import NotRemoveableException
from com.sun.star.beans import PropertyExistException
from com.sun.star.beans import PropertyVetoException
from com.sun.star.beans import UnknownPropertyException
from com.sun.star.lang import WrappedTargetException

from org.creativecommons.libreoffice.program.IVisibleNotice import IVisibleNotice
from org.creativecommons.libreoffice.program.Constants import Constants

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

        
        
