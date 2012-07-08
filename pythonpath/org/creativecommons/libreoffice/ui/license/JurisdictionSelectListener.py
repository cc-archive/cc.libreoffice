#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from com.sun.star.awt import XItemListener
from org.creativecommons.libreoffice.ui.license.UpdateLicenseListner \
  import UpdateLicenseListner

class JurisdictionSelectListener(XItemListener,UpdateLicenseListner):
    """Get the user selected jurisdiction.
    """
    
    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        UpdateLicenseListner.__init__(self,dialog)

    def itemStateChanged(self, event):
        """@override
        
        Arguments:
        - `event`:ItemEvent
        """
        
        self.dialog.selectedJurisdiction=self.dialog.juriList.pop(
            event.Selected)
        
    def disposing(self, event):
        """@override
        
        Arguments:
        - `event`:EventObject
        """
        pass
