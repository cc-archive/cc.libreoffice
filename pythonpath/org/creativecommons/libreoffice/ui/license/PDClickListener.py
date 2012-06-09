from com.sun.star.awt import XActionListener

class PDClickListener(XActionListener):
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
        self.dialog.setLicenseType(3)

    #@Override
    def disposing(self, eObject):
        """
        
        Arguments:
        - `eObject`:EventObject
        """
        pass
    
