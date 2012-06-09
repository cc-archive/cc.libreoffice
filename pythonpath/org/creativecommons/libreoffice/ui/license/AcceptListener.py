from com.sun.star.awt.XItemListener import XItemListener
from com.sun.star.beans.PropertyVetoException import PropertyVetoException
from com.sun.star.beans.UnknownPropertyException import UnknownPropertyException
from com.sun.star.container.NoSuchElementException import NoSuchElementException
from com.sun.star.lang.WrappedTargetException import WrappedTargetException
from com.sun.star.lang.IllegalArgumentException import IllegalArgumentException

class AcceptListener(XItemListener):
    """Enable OK button after accepting the deed.
    """
    
    def __init__(self, dialog):
        """
        
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        self.dialog = dialog


    #@override
    def itemStateChanged(self, event):
        """
        
        Arguments:
        - `event`:ItemEvent
        """
        accept=event.source

        try:

            #enable disable dialog controls accoring to the state
            ##TODO: was (short)0
            if (accept.getState()==0):
                self.dialog.xNameCont.getByName(
                    LicenseChooserDialog.BTN_OK).setPropertyValue(
                        "Enabled", False)
            else:
                self.dialog.xNameCont.getByName(
                    LicenseChooserDialog.BTN_OK).setPropertyValue(
                        "Enabled", True)
            
        except IllegalArgumentException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            print ex
            print type(ex)
            raise ex

        except WrappedTargetException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            print ex
            print type(ex)
            raise ex
        except PropertyVetoException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            print ex
            print type(ex)
            raise ex
        except UnknownPropertyException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            print ex
            print type(ex)
            raise ex
        except NoSuchElementException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            print ex
            print type(ex)
            raise ex

    def disposing(self, eObject):
        """
        
        Arguments:
        - `eObject`:EventObject
        """
        pass
