#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper
import traceback

from com.sun.star.awt import XActionListener

class OKClickListener(XActionListener,unohelper.Base):
    """
    """
    
    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        self.dialog = dialog


    def actionPerformed(self, aEvent):
        """
        
        Arguments:
        - `aEvent`:ActionEvent
        """
        
        try:
            self.dialog.cancelled=False
            self.dialog.close()
        except Exception, e:
            traceback.print_exc()
            raise e



    def disposing(self, eObject):
        """
        
        Arguments:
        - `eObject`:EventObject
        """
        pass

        
