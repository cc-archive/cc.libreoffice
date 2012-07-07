#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info
import traceback

from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram

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


    
