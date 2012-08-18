#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper
import traceback

from com.sun.star.awt import XActionListener


class FaqClickListener(XActionListener, unohelper.Base):
    """Go to Creative Commons FAQ site.
    """
    def __init__(self, dialog, m_xContext):
        """
        Arguments:
        - `dialog`: LicenseChooserDialog
        - `m_xContext`: XComponentContext
        """
        self.dialog = dialog
        self.m_xContext = m_xContext

    ##OnFinishClick
    def disposing(self, eObject):
        """
        Arguments:
        - `eObject`:EventObject
        """
        pass

    ##actionPerformed
    def actionPerformed(self, action):
        """
        Arguments:
        - `action`:ActionEvent
        """
        try:
            xMcFact = self.m_xContext.getServiceManager()
            xSystemShellExecute = xMcFact.createInstanceWithContext(
                    "com.sun.star.system.SystemShellExecute", self.m_xContext)
            aURLString = ("http://wiki.creativecommons.org/"
                           "Frequently_Asked_Questions")

            ##TODO: Original code used SystemShellExecuteFlags.DEFAULTS
            xSystemShellExecute.execute(
                aURLString, "", 0)

        except Exception, ex:
            print 'Exception in FaqClickListener.actionPerformed'
            traceback.print_exc()
            raise ex
