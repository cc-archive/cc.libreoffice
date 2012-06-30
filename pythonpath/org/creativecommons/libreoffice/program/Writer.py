#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram
from org.creativecommons.libreoffice.util.PageHelper import PageHelper

class Writer(OOoProgram):
    """
    """
    
    def __init__(self, component,m_xContext):
        """
        
        Arguments:
        - `component`:
        - `m_xContext`:
        """
        super(Writer,self).__init__(component,m_xContext)

    def insertPicture(self, img):
        """Insert pictures from the internet.
        
        Arguments:
        - `img`:Image
        """
        #mxDoc=self.component

        docCursor=self.component.getCurrentController().getViewCursor()

        #mxDocFactory=self.component

        xBitmapContainer=None
        xImage=None
        internalURL=None

        try:
            xBitmapContainer=self.component.createInstance(
                    "com.sun.star.drawing.BitmapTable")
            xImage=self.component.createInstance(
                    "com.sun.star.text.TextGraphicObject")
            #xProps=xImage

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            #Static class method call
            sName = PageHelper.createUniqueName(xBitmapContainer, img.getPhotoID())
            xBitmapContainer.insertByName(sName, img.getSelectedImageURL())

            ##TODO:partially Implemented

            
            
        except Exception, ex:
                print "Exception in Writer.insertPicture: "
                print ex
                print type(ex)
                #raise ex
