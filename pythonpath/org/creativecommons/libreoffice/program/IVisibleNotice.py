#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

class IVisibleNotice():
    """This is an Abstract class. 
    """
    
    def __init__(self, ):
        """
        """
        pass

    def hasVisibleNotice(self, ):
        """
        """
        raise NotImplementedError( "hasVisibleNotice() method not implemented yet" )

    def insertVisibleNotice(self, ):
        """Create and insert an auto-text containing the license
        """
        raise NotImplementedError( "insertVisibleNotice() method not implemented yet" )

    def updateVisibleNotice(self, ):
        """Update visible notices to current license
        """
        raise NotImplementedError( "updateVisibleNotice() method not implemented yet" )
        
    def setDocumentLicense(self, license):
        """Set the license meta data.
        
        Arguments:
        - `license`:License
        """
        raise NotImplementedError( "setDocumentLicense() method not implemented yet" )

    def getDocumentLicense(self, ):
        """Get the licesne for the document
        """
        raise NotImplementedError( "getDocumentLicense() method not implemented yet" )

    def insertPicture(self, img):
        """Insert pictures from the internet.
        
        Arguments:
        - `img`:Image
        """
        raise NotImplementedError( "insertPicture() method not implemented yet" )

    
        
        
