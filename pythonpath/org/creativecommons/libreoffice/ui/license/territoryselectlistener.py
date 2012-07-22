#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper
from com.sun.star.awt import XItemListener


class TerritorySelectListener(XItemListener, unohelper.Base):
    """Get the user selected territory.
    """
    def __init__(self, dialog):
        """
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        self.dialog = dialog

    def itemStateChanged(self, event):
        """
        Arguments:
        - `event`:ItemEvent
        """
        self.dialog.setSelectedTerritory(event.Selected)

    def disposing(self, arg0):
        """
        Arguments:
        - `arg0`:com.sun.star.lang.EventObject
        """
        pass
