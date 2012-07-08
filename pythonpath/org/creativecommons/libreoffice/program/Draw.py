#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback
import uno

from com.sun.star.awt import Size
from com.sun.star.awt import Point
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.style.LineSpacingMode import PROP
from com.sun.star.style import LineSpacing


from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram
from org.creativecommons.libreoffice.util.ShapeHelper import createShape, addPortion
from org.creativecommons.libreoffice.util.PageHelper import getDrawPageCount, getDrawPageByIndex


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
            #as a precaution
            #if xBitmapContainer is not None:
            #    xBitmapContainer.removeByName("imgID")
            traceback.print_exc()
            raise e


    def insertVisibleNotice(self, xPage=None):
        """Create and insert an auto-text containing the license for the given draw page.
        (if the draw page is given)
        
        Arguments:
        - `xPage`:XDrawPage
        """
        
        try:
            if xPage is None:
                xDocModel=self.component
                xController = xDocModel.getCurrentController()
                xPage=xController.getCurrentPage()

            docLicense=super(Draw,self).getDocumentLicense()

            #xPageProps=xPage

            #consider page margins and the page size when inserting the visible notice
            self.pageWidth=xPage.getPropertyValue("Width")
            self.pageHeight=xPage.getPropertyValue("Height")
            self.pageBorderBottom=xPage.getPropertyValue("BorderBottom")
            self.pageBorderRight=xPage.getPropertyValue("BorderRight")

            #xShapes=xPage

            aLineSpacing=LineSpacing()
            aLineSpacing.Mode=PROP

            #first shape
            x=self.pageWidth - len(docLicense.getName()) * self.pageWidth / 65 - self.pageBorderRight - 200
            y=self.pageHeight - 2 * self.pageWidth / 50 - self.pageBorderBottom - 200
            width= len(docLicense.getName()) * self.pageWidth / 65
            height= 2 * self.pageWidth / 50

            xRectangle=createShape(self.component,
                                   Point(x,y),Size(width,height),
                "com.sun.star.drawing.RectangleShape")

            xPage.add(xRectangle)

            xShapePropSet=xRectangle

            xShapePropSet.setPropertyValue("TextAutoGrowHeight", True)
            xShapePropSet.setPropertyValue("TextAutoGrowWidth", True)
            noneLineStyle=uno.getConstantByName("com.sun.star.drawing.LineStyle.NONE")
            xShapePropSet.setPropertyValue("LineStyle",noneLineStyle)
            noneFillStyle=uno.getConstantByName("com.sun.star.drawing.FillStyle.NONE")
            xShapePropSet.setPropertyValue("FillStyle", noneFillStyle)
            xShapePropSet.setPropertyValue("Name", "ccoo:licenseText")

            #first paragraph
            xTextPropSet=addPortion(xRectangle, docLicense.getName(), False)
            xTextPropSet.setPropertyValue("CharColor", int(0x000000))

            #insert the graphic
            self.__embedGraphic(docLicense.getImageUrl(),xPage)
            
        except Exception, e:
            traceback.print_exc()
            raise e

    def hasVisibleNotice(self, ):
        """
    """
        raise NotImplementedError("Draw.hasVisibleNotice")

    def insertPicture(self, img):
        """Insert pictures from the internet.
    
        Arguments:
        - `img`:Image
        """
        
        raise NotImplementedError("Draw.insertPicture")

    def updateVisibleNotice(self, ):
        """Update visible notices to current license.
        """
        
        try:
            drawPages=[]
            shapes=[]

            #search for vivible notices and remove them
            numOfPages=getDrawPageCount(self.component)

            for i in range(numOfPages):
                xPage=getDrawPageByIndex(self.component,i)
                #xShapes=xPage

                count=xPage.getCount()

                for j in range(count):
                    xShape=xPage.getByIndex(j)
                    #xShapePropSet=xShape
                    name = xShape.getPropertyValue("Name")

                    if (name.lower() == "ccoo:licenseImage".lower()):
                        shapes.append(xShape)
                        drawPages.append(xPage)
                    elif(name.lower() == "ccoo:licenseText".lower()):
                        shapes.append(xShape)

                
                for shape in shapes:
                    xPage.remove(shape)

            #add new visible notices
            for page in drawPages:
                self.insertVisibleNotice(page)
            
        except Exception, e:
            traceback.print_exc()
            raise e


    
