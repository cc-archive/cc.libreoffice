#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper
from com.sun.star.awt import XItemListener

class UpdateLicenseListner(XItemListener,unohelper.Base):
    """Updates the selected license Label
    """
    
    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        self.dialog = dialog
        


    def disposing(self, event):
        """
        
        Arguments:
        - `event`:EventObject
        """
        pass

    def getDialog(self, ):
        """
        """
        return self.dialog

    def setDialog(self, dialog):
        """
        
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        self.dialog=dialog

    def itemStateChanged(self, event):
        """
        
        Arguments:
        - `event`:ItemEvent
        """
        self.getDialog().updateSelectedLicense()
