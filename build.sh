#!/bin/bash


rm out.oxt
echo "Deleted old generated extension"
zip -r test * -x *.*~ build.sh */*.*~ */*/*.*~ 
mv test.zip out.oxt
echo "Created new extension"

#Removes the extension if it is already installed
/usr/lib/libreoffice/program/unopkg remove org.creativecommons.libreoffice.CcLoAddin
echo "Uninstalled the old extension"

#Adds the new extension
/usr/lib/libreoffice/program/unopkg add out.oxt
echo "Installed the new extension"

#Starts LibreOffice
echo "Starting LibreOffice writer"
libreoffice --writer --nofirststartwizard
#libreoffice --draw --nofirststartwizard
#libreoffice --calc --nofirststartwizard

#Removes the extension when quitting
echo "Removing the installed extension"
/usr/lib/libreoffice/program/unopkg remove org.creativecommons.libreoffice.CcLoAddin
