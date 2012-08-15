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


class AcceptWaiveListener(XItemListener, unohelper.Base):
    """Enable CC0 deed and territory etc. after accepting to waive.
    """
    def __init__(self, dialog):
        """
        Arguments:
        - `dialog`:LicenseChooserDialog
        """
        self.dialog = dialog

    def disposing(self, arg0):
        """
        Arguments:
        - `arg0`: EventObject
        """
        pass

    #@override
    def itemStateChanged(self, event):
        """
        Arguments:
        - `event`:ItemEvent
        """
        waive = event.Source

        try:
            #enable disable dialog controls accoring to the state
            if (waive.getState() == 0):
                self.dialog.cc0Tab.getByName(
                    self.dialog.CHK_YES_CC0).setPropertyValue(
                        "Enabled", False)

                ##TODO: was (short)0
                self.dialog.cc0Tab.getByName(
                    LicenseChooserDialog.CHK_YES_CC0).setPropertyValue(
                        "State", 0)

                self.dialog.cc0Tab.getByName(
                    self.dialog.TXT_LEGAL_CODE_CC0).setPropertyValue(
                        "Enabled", False)

                self.dialog.cc0Tab.getByName(
                    self.dialog.CMB_TERRITORY).setPropertyValue(
                        "Enabled", False)

                self.dialog.cc0Tab.getByName(
                    self.dialog.BTN_OK).setPropertyValue(
                        "Enabled", False)

            else:
                self.dialog.cc0Tab.getByName(
                     self.dialog.CHK_YES_CC0).setPropertyValue(
                         "Enabled", True)

                self.dialog.cc0Tab.getByName(
                     self.dialog.TXT_LEGAL_CODE_CC0).setPropertyValue(
                         "Enabled", True)

                self.dialog.cc0Tab.getByName(
                     self.dialog.CMB_TERRITORY).setPropertyValue(
                         "Enabled", True)

        except IllegalArgumentException, ex:
            print "Exception in AcceptWaiveListener.itemStateChanged: "
            traceback.print_exc()
            raise ex

        except WrappedTargetException, ex:
            print "Exception in AcceptWaiveListener.itemStateChanged: "
            traceback.print_exc()
            raise ex

        except PropertyVetoException, ex:
            print "Exception in AcceptWaiveListener.itemStateChanged: "
            traceback.print_exc()
            raise ex

        except UnknownPropertyException, ex:
            print "Exception in AcceptWaiveListener.itemStateChanged: "
            traceback.print_exc()
            raise ex

        except NoSuchElementException, ex:
            print "Exception in AcceptWaiveListener.itemStateChanged: "
            traceback.print_exc()
            raise ex
