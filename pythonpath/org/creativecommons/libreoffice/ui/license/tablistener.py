#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper

from com.sun.star.awt import XTabListener

class TabListener(XTabListener,unohelper.Base):
    """Used to find the event of a tab gaining focus
    """
    
    def __init__(self, dialog):
        """
        """
        
        self.dialog = dialog
        
    
    def inserted(self,tabID):
        """
        """
        print "inserted :"+str(tabID)



    def removed(self, tabID):
        """
        """
        print "removed :"+str(tabID)

    def changed(self, par,par1):
        """
        
        Arguments:
        - `par`:
        - `par1`:
        """
        print "changed"
        
        
    def activated(self, tabID):
        """
        
        Arguments:
        - `tabID`:
        """
        print "activated :"+str(tabID)
        self.dialog.setLicenseType(tabID)
        #self.dialog.getSelectedLicense()

    def deactivated(self, tabID):
        """
        
        Arguments:
        - `tabID`:
        """
        print "deactivated :"+str(tabID)
