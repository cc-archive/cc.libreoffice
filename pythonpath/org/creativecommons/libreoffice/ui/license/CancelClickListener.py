import unohelper

from com.sun.star.awt import XActionListener

class CancelClickListener(XActionListener,unohelper.Base):
    """
    """
    
    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`: LicenseChooserDialog
        """
        self.dialog = dialog

    def actionPerformed(self, aEvent):
        """
        
        Arguments:
        - `aEvent`: ActionEvent
        """
        self.dialog.close()

    def disposing(self, eObject):
        """
        
        Arguments:
        - `eObject`: EventObject
        """
        pass
