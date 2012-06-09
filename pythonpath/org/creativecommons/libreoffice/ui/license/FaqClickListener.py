from com.sun.star.awt.XActionListener import XActionListener
from com.sun.star.system.SystemShellExecuteFlags import SystemShellExecuteFlags

class FaqClickListener(XActionListener):
    """Go to Creative Commons FAQ site.
    """
    
    def __init__(self, dialog,m_xContext):
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
            xMcFact=self.m_xContext.getServiceManager()
            xSystemShellExecute = xFact.createInstanceWithContext(
                    "com.sun.star.system.SystemShellExecute", m_xContext)
            aURLString = "http://wiki.creativecommons.org/Frequently_Asked_Questions"

            xSystemShellExecute.execute(
                aURLString, "",SystemShellExecuteFlags.DEFAULTS)

        except Exception, ex:
            print 'Exception in FaqClickListener.actionPerformed'
            print type(ex)
            print ex
            raise ex
