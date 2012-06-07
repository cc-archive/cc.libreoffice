from com.sun.star.awt.XItemListener import XItemListener
from org.creativecommons.libreoffice.ui.license.UpdateLicenseListener import UpdateLicenseListener

class JurisdictionSelectListener(XItemListener,UpdateLicenseListener):
    """Get the user selected jurisdiction.
    """
    
    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        super(JurisdictionSelectListener,self).__init__(dialog)

    def itemStateChanged(self, event):
        """@override
        
        Arguments:
        - `event`:ItemEvent
        """
        #TODO: Complete the method
        pass
        
    def disposing(self, event):
        """@override
        
        Arguments:
        - `event`:EventObject
        """
        pass
