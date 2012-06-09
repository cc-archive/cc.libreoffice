from com.sun.star.awt.XActionListener import XActionListener

class CCClickListener(XActionListener):
    """Show Creative Commons tab.
    """
    
    def __init__(self, dialog):
        """
        """
        self.dialog=dialog


    def actionPerformed(self, aEvent):
        """
        
        Arguments:
        - `aEvent`:ActionEvent
        """
        self.dialog.setLicenseType(1)

    #@Override
    def disposing(self, eObject):
        """
        
        Arguments:
        - `eObject`:EventObject
        """
        pass
    
        
