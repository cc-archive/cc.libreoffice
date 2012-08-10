#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper
from com.sun.star.awt import XFocusListener

class CC0TabFocusListener(XFocusListener, unohelper.Base):

    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`:
        """
        self.dialog = dialog

    def focusGained(self, event):
        """
        
        Arguments:
        - `event`:
        """
        print "focusGained"

    def focusLost(self, event):
        """
        
        Arguments:
        - `event`:
        """
        print "focusLost"
        
        
