#!/bin/bash

rm out.oxt
zip -r test * -x *.*~ build.sh */*.*~ */*/*.*~ 
mv test.zip out.oxt

#Removes the extension if it is already installed
/usr/lib/libreoffice/program/unopkg remove org.creativecommons.openoffice.CcOOoAddin

#Adds the new extension
/usr/lib/libreoffice/program/unopkg add out.oxt

#Starts LibreOffice
libreoffice --writer --nofirststartwizard

#Removes the extension when quitting
/usr/lib/libreoffice/program/unopkg remove org.creativecommons.openoffice.CcOOoAddin
