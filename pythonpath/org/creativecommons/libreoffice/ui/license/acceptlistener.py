#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import unohelper

from com.sun.star.awt import XItemListener
from com.sun.star.beans import PropertyVetoException
from com.sun.star.beans import UnknownPropertyException
from com.sun.star.container import NoSuchElementException
from com.sun.star.lang import WrappedTargetException
from com.sun.star.lang import IllegalArgumentException


class AcceptListener(XItemListener, unohelper.Base):
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
        accept = event.Source

        try:

            #enable disable dialog controls accoring to the state
            ##TODO: was (short)0
            if (accept.getState() == 0):
                self.dialog.xNameCont.getByName(
                    self.dialog.BTN_OK).setPropertyValue(
                        "Enabled", False)
            else:
                self.dialog.xNameCont.getByName(
                    self.dialog.BTN_OK).setPropertyValue(
                        "Enabled", True)
        except IllegalArgumentException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            traceback.print_exc()
            raise ex

        except WrappedTargetException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            traceback.print_exc()
            raise ex
        except PropertyVetoException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            traceback.print_exc()
            raise ex
        except UnknownPropertyException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            traceback.print_exc()
            raise ex
        except NoSuchElementException, ex:
            print "Exception in AcceptListener.itemStateChanged: "
            traceback.print_exc()
            raise ex

    def disposing(self, eObject):
        """
        Arguments:
        - `eObject`:EventObject
        """
        pass
