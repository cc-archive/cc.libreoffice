#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info
import traceback

from com.sun.star.awt import Size
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.style.LineSpacingMode import PROP
from com.sun.star.style import LineSpacing

from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram
from org.creativecommons.libreoffice.util.PageHelper import PageHelper
from org.creativecommons.libreoffice.util.ShapeHelper import ShapeHelper

class Calc(OOoProgram):
    """
    """
    
    def __init__(self, component,m_xContext):
        """
        
        Arguments:
        - `component`:XComponent
        - `m_xContext`:XComponentContext
        """
        super(Calc,self).__init__(component,m_xContext)
        
        
    def __getAbsoluteCellPosition(self, spreadsheet,x,y):
        """
        
        Arguments:
        - `spreadsheet`:XSpreadsheet
        - `x`:Integer
        - `y`:Integer
        """
        
        try:
            xCell = spreadsheet.getCellByPosition(x, y)
            #xPropSet=xCell
            p=xCell.getPropertyValue("Position")
            return p
        except Exception, e:
            traceback.print_exc()
            raise e


    def __getActiveCellsRange(self, xComponent):
        """
        
        Arguments:
        - `xComponent`:xComponent
        """
        #xDocModel=xComponent
        xSheetCellAddressable=xComponent.getCurrentSelection()
        return xSheetCellAddressable.getRangeAddress()

    #TODO-complete the method
    def insertPicture(self, img):
        """Insert pictures from the internet.
        
        Arguments:
        - `img`:Image
        """
                
        try:
            xSheetDoc=self.component
            #xDocModel=xSheetDoc
            xController = xSheetDoc.getCurrentController()
            #view=xController
            xSpreadsheet = xController.getActiveSheet()
            
            #xSpreadsheetFactory=xSheetDoc
            #xDrawPageSupplier=xSpreadsheet

            xPage = xDrawPageSupplier.getDrawPage()

            xBitmapContainer=xSheetDoc.createInstance(
                "com.sun.star.drawing.BitmapTable")
            xGraphicShape = xSheetDoc.createInstance(
                    "com.sun.star.drawing.GraphicObjectShape")

            xGraphicShape.setSize(Size(3104, 1093))

            acrSc=self.__getActiveCellsRange(self.component).StartColumn
            acrSr=self.__getActiveCellsRange(self.component).StartRow
            xGraphicShape.setPosition(self.__getAbsoluteCellPosition(xSpreadsheet,acrSc,acrSr))

            xProps=xGraphicShape

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            sName = PageHelper.createUniqueName(xBitmapContainer, img.getPhotoID())
            xBitmapContainer.insertByName(sName, img.getSelectedImageURL())

            internalURL=xBitmapContainer.getByName(sName)

            xProps.setPropertyValue("AnchorType",AS_CHARACTER)
            xProps.setPropertyValue("GraphicURL", internalURL)
            xProps.setPropertyValue("Name", "ccoo:picture")

            #insert the graphic at the cursor position
            xPage.add(xGraphicShape)

            xGraphicPropsGOSX=xProps.getPropertyValue( "Graphic" )
            actualSize=xGraphicPropsGOSX.getPropertyValue( "Size100thMM" )

            if ((actualSize.Width != 0) or (actualSize.Height != 0)):
                xGraphicShape.setSize(actualSize)
            else:
                actualSize=xGraphicPropsGOSX.getPropertyValue("SizePixel")
                #convert pixels to 100th of mm
                xGraphicShape.setSize(Size(actualSize.Width * 26.4,actualSize.Height * 26.4))
                
            #remove the helper-entry
            xBitmapContainer.removeByName(sName)

            aLineSpacing=LineSpacing()
            aLineSpacing.Mode =PROP

            byCaption = ""
            if (img.getLicenseCode()== "by"):
                byCaption = "CC BY "
            else:
                byCaption = img.getLicenseCode().upper()+" "

            #first shape
            caption = byCaption + img.getLicenseNumber() + " ( " + img.getLicenseURL() + " )"
            
            #resume @ 151

            
            
        except Exception, e:
            traceback.print_exc()
            raise e


    def __embedGraphic(self, imgURL,xSpreadsheet):
        """Insert the license image.
    
    Arguments:
    - `imgURL`:String-URL to the license image
    - `xSpreadsheet`:xSpreadsheet-Spread sheet to insert the image
    """
        
        try:
            xSheetDoc=self.component
            #xSpreadsheetFactory=xSheetDoc
            #xDrawPageSupplier=xSpreadsheet
            xPage=xSpreadsheet.getDrawPage()

            xBitmapContainer=xSheetDoc.createInstance(
                "com.sun.star.drawing.BitmapTable")

            xGraphicShape=xSheetDoc.createInstance(
                    "com.sun.star.drawing.GraphicObjectShape")
            xGraphicShape.setSize(Size(3104, 1093))

            acrSc=self.__getActiveCellsRange(self.component).StartColumn
            acrSr=self.__getActiveCellsRange(self.component).StartRow

            #add to current cell
            xGraphicShape.setPosition(self.__getAbsoluteCellPosition(xSpreadsheet,acrSc,acrSr))

            xProps=xGraphicShape

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            internalURL=xBitmapContainer.getByName("imgID")

            xProps.setPropertyValue("AnchorType",AS_CHARACTER)
            xProps.setPropertyValue("GraphicURL", internalURL)
            xProps.setPropertyValue("Width", 4000) # original: 88 px
            xProps.setPropertyValue("Height", 1550) # original: 31 px
            xProps.setPropertyValue("Name", "ccoo:licenseImage")

            #inser the graphic at the cursor position
            xPage.add(xGraphicShape)
            #remove the helper-entry
            xBitmapContainer.removeByName("imgID")
            
        except Exception, e:
            traceback.print_exc()
            raise e

