#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info
import traceback
import uno

from com.sun.star.awt import Size
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.style.LineSpacingMode import PROP
from com.sun.star.style import LineSpacing

from org.creativecommons.libreoffice.program.loprogram import LoProgram
from org.creativecommons.libreoffice.util.pagehelper import createUniqueName
from org.creativecommons.libreoffice.util.shapehelper \
  import createShape, addPortion

class Calc(LoProgram):
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
            
            # print "X- "+p.X
            #print "Y- "+p.Y
            return p
        except Exception, e:
            traceback.print_exc()
            raise e


    ##TODO-The following method throws an exception if a cell
    ##is not selected whenthis method is called. Fix it
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

            xPage = xSpreadsheet.getDrawPage()

            xBitmapContainer=xSheetDoc.createInstance(
                "com.sun.star.drawing.BitmapTable")
            xGraphicShape = xSheetDoc.createInstance(
                    "com.sun.star.drawing.GraphicObjectShape")

            xGraphicShape.setSize(Size(3104, 1093))

            acrSc=self.__getActiveCellsRange(self.component).StartColumn
            acrSr=self.__getActiveCellsRange(self.component).StartRow
            xGraphicShape.setPosition(self.__getAbsoluteCellPosition(
                xSpreadsheet,acrSc,acrSr))

            xProps=xGraphicShape

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            sName = createUniqueName(xBitmapContainer, img.getPhotoID())
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
                xGraphicShape.setSize(
                    Size(actualSize.Width * 26.4,actualSize.Height * 26.4))
                
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
            caption = (byCaption + img.getLicenseNumber() + " ( " 
                + img.getLicenseURL() + " )")
            
            #resume @ 151
            raise NotImplementedError("Calc.insertPicture")

            
            
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
            xGraphicShape.setPosition(self.__getAbsoluteCellPosition(
                xSpreadsheet,acrSc,acrSr))

            xProps=xGraphicShape

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)
            xBitmapContainer.insertByName("imgID", imgURL)

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

    
    def insertVisibleNotice(self, xSpreadsheet=None):
        """Create and insert an auto-text containing the license(
        if spreadsheet is given,to it)
    
        Arguments:
        - `xSpreadsheet`:xSpreadsheet- Spread sheet to insert the text
        """
        
        try:
            if xSpreadsheet is None:
                xDocModel=self.component
                xController = xDocModel.getCurrentController()
                xSpreadsheet=xController.getActiveSheet()
            
            docLicense=super(Calc,self).getDocumentLicense()

            #xDrawPageSupplier=xSpreadsheet
            xPage=xSpreadsheet.getDrawPage()

            #xShapes=xPage

            aLineSpacing=LineSpacing()
            aLineSpacing.Mode=PROP

            #first shape
            acrSc=self.__getActiveCellsRange(self.component).StartColumn
            acrSr=self.__getActiveCellsRange(self.component).StartRow+3

            absCellPos=self.__getAbsoluteCellPosition(xSpreadsheet,acrSc,acrSr)

            xRectangle=createShape(
                self.component,absCellPos,Size( 15000, 1500 ),
                                   "com.sun.star.drawing.RectangleShape" )
            xPage.add( xRectangle )

            xShapePropSet=xRectangle

            xRectangle.setPropertyValue("TextAutoGrowHeight", True)
            xShapePropSet.setPropertyValue("TextAutoGrowWidth", True)
            noneLineStyle=uno.getConstantByName(
                "com.sun.star.drawing.LineStyle.NONE")
            xShapePropSet.setPropertyValue("LineStyle", noneLineStyle)
            noneFillStyle=uno.getConstantByName(
                "com.sun.star.drawing.FillStyle.NONE")
            xShapePropSet.setPropertyValue("FillStyle", noneFillStyle)
            xShapePropSet.setPropertyValue("Name", "ccoo:licenseText")

            #first paragraph
            xTextPropSet=addPortion( xRectangle, docLicense.getName(), False )
            #TODO-has this been done correctly??
            xTextPropSet.setPropertyValue( "CharColor",int(0x000000))

            #insert the graphic
            self.__embedGraphic(docLicense.getImageUrl(),xSpreadsheet)
            
        except Exception, e:
            traceback.print_exc()
            #raise e

    #TODO-complete the method
    def updateVisibleNotice(self, ):
        """Update visible notices to current license.
        """
        shapes=[]
        drawPages=[]
        
        try:
            xSheetDoc=self.component

            sheetNames = xSheetDoc.getSheets().getElementNames()

            #search for visible notices and remove them
            for sheet in sheetNames:
                xSpreadsheet=xSheetDoc.getSheets().getByName(sheet)

                #xDrawPageSupplier=xSpreadsheet
                xShapes = xSpreadsheet.getDrawPage()

                #TODO-resume from 381
                numOfShapes=xShapes.getCount()
                for i in range(numOfShapes):
                    xShape=xShapes.getByIndex(i)
                    #xShapePropSet=xShape
                    
                    name= xShape.getPropertyValue("Name")

                    if (name.lower() == "ccoo:licenseImage".lower()):
                        shapes.append(xShape)
                        drawPages.append(xSpreadsheet)
                    elif(name.lower() == "ccoo:licenseText".lower()):
                        shapes.append(xShape)

                for shape in shapes:
                    xShapes.remove(shape)

            #add new visible notices
            for page in drawPages:
                self.insertVisibleNotice(page)
            
        except Exception, e:
            traceback.print_exc()
            raise e

    def hasVisibleNotice(self, ):
        """
    """
        raise NotImplementedError("Calc.hasVisibleNotice")
