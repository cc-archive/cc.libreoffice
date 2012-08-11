#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper

from com.sun.star.awt import XTabListener


class TabListener(XTabListener, unohelper.Base):
    """Used to find the event of a tab gaining focus
    """
    def __init__(self, dialog):
        """
        """
        self.dialog = dialog

    def inserted(self, tabID):
        """
        """
        pass

    def removed(self, tabID):
        """
        """
        pass

    def changed(self, par, par1):
        """
        Arguments:
        - `par`:
        - `par1`:
        """
        pass

    def activated(self, tabID):
        """
        Arguments:
        - `tabID`:
        """
        self.dialog.setLicenseType(tabID)

    def deactivated(self, tabID):
        """
        Arguments:
        - `tabID`:
        """
        pass
