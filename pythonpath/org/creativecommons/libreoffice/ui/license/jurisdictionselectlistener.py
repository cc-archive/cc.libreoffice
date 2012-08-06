#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

#from com.sun.star.awt import XItemListener
from org.creativecommons.libreoffice.ui.license.updatelicenselistner \
  import UpdateLicenseListner


class JurisdictionSelectListener(UpdateLicenseListner):
    """Get the user selected jurisdiction.
    """
    def __init__(self, dialog):
        """
        Arguments:
        - `tab`:The tab in which the jurisdiction list will be shown
        """
        UpdateLicenseListner.__init__(self, dialog)

    def itemStateChanged(self, event):
        """@override
        Arguments:
        - `event`:ItemEvent
        """
        
        self.dialog.selectedJurisdiction = self.dialog.juriList[event.Selected]
        self.dialog.updateSelectedLicense()

    def disposing(self, event):
        """@override
        Arguments:
        - `event`:EventObject
        """
        pass
