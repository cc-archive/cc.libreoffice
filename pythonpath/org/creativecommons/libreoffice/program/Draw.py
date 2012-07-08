#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from com.sun.star.awt import Size
from com.sun.star.awt import Point
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER


from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram

class Draw(OOoProgram):
    """
    """
    
    def __init__(self,component,m_xContext):
        """
        
        Arguments:
        - `component`:XComponent
        - `m_xContext`:XComponentContext
        """
        super(Draw,self).__init__(component,m_xContext)
        
        
    def __embedGraphic(self, imgURL,xPage):
        """
        
        Arguments:
        - `imgURL`:String- URL to the license image
        - `xPage`:xDrawPage- Draw page sheet to insert the image
        """
        
        try:
            xDrawingFactory=self.component

            xBitmapContainer=xDrawingFactory.createInstance(
                "com.sun.star.drawing.BitmapTable")

            xGraphicShape=xDrawingFactory.createInstance(
                "com.sun.star.drawing.GraphicObjectShape")

            
            xGraphicShape.setSize(Size(310 * self.pageWidth / 2000, 109 * self.pageWidth / 2000))
            x=self.pageWidth - 310 * self.pageWidth / 2000- self.pageBorderRight - 200
            y=self.pageHeight - 2 * self.pageWidth / 50 - 109 * self.pageWidth / 1800 - self.pageBorderBottom - 200

            xGraphicShape.setPosition(Point(x,y))

            xProps=xGraphicShape

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            xBitmapContainer.insertByName("imgID", imgURL)
            internalURL=xBitmapContainer.getByName("imgID")

            xProps.setPropertyValue("AnchorType",AS_CHARACTER)
            xProps.setPropertyValue("GraphicURL", internalURL)
            xProps.setPropertyValue("Width", 4000) #original: 88 px
            xProps.setPropertyValue("Height", 1550) #original: 31 px
            xProps.setPropertyValue("Name", "ccoo:licenseImage")

            #inser the graphic at the cursor position
            xPage.add(xGraphicShape)

            #remove the helper-entry
            xBitmapContainer.removeByName("imgID")
            
            
        except Exception, e:
            traceback.print_exc()
            raise e

