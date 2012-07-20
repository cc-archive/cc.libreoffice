#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback


from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER

from org.creativecommons.libreoffice.program.loprogram import LoProgram
from org.creativecommons.libreoffice.util.pagehelper import createUniqueName


class Writer(LoProgram):
    """
    """
    
    def __init__(self, component,m_xContext):
        """
        
        Arguments:
        - `component`:
        - `m_xContext`:
        """
        super(Writer,self).__init__(component,m_xContext)

    
    def __getMasterField(self,field_name,mxTextFields,mxDocFactory):
        """
        Arguments:
        - `field_name`:String
        - `mxTextFields`:XTextFieldsSupplier
        - `mxDocFactory`:XMultiServiceFactory
        """

        
        try:
            #property set for the user text field
            xMasterPropSet=None
            
            #determine the name for the master field
            masterFieldName = "com.sun.star.text.FieldMaster.User." + \
              field_name
            
            #see if the user field already exists
            if (mxTextFields.getTextFieldMasters().hasByName(masterFieldName)):
                xMasterPropSet=mxTextFields.getTextFieldMasters().getByName(
                    masterFieldName)

            else:
                #Create a fieldmaster for our newly created User Text field, 
                #and access it's XPropertySet interface

                xMasterPropSet=mxDocFactory.createInstance(
                "com.sun.star.text.FieldMaster.User")

                xMasterPropSet.setPropertyValue("Name", field_name)

            return xMasterPropSet
            
        except Exception, e:
            traceback.print_exc()
            raise e

        
        
    
    def __updateMasterField(self, 
                            field_name,field_value,mxTextFields,mxDocFactory):
        """
        
        Arguments:
        - `field_name`:String
        - `field_value`:String
        - `mxTextFields`:XTextFieldsSupplier
        - `mxDocFactory`:XMultiServiceFactory
        """
        
        try:
            #get or create the master field
            xMasterPropSet = self.__getMasterField(field_name, 
                                                   mxTextFields, mxDocFactory)

            #Set the value of the FieldMaster
            xMasterPropSet.setPropertyValue("Content", field_value)

            #update any dependent text fields in the document
            fields=xMasterPropSet.getPropertyValue("DependentTextFields")

            for field in fields:
                field.update()

            return xMasterPropSet
            
        except Exception, e:
            traceback.print_exc()
            raise e

    def __createUserTextField(self, mxDocFactory,
                              mxTextFields,field_name,field_value):
        """
    
        Arguments:
        - `mxDocFactory`:XMultiServiceFactory
        - `mxTextFields`:XTextFieldsSupplier
        - `field_name`:String
        - `field_value`:String
        """

        
        try:
            xMasterPropSet=self.__updateMasterField(field_name, field_value,
                                                    mxTextFields, mxDocFactory)

            #Use the text document's factory to create a user text field,
            #and access it's XDependentTextField interface

            xUserField=mxDocFactory.createInstance(
                "com.sun.star.text.TextField.User")

            #Attach the field master to the user field
            xUserField.attachTextFieldMaster(xMasterPropSet)

            return xUserField

                    
        except Exception, e:
            traceback.print_exc()
            raise e

        

    
    def __embedGraphic(self, mxDocFactory,xCursor,imgURL):
        """Embeds the license "button" into a Textdocument at 
        the given cursor position
        
        Arguments:
        - `mxDocFactory`:XMultiServiceFactory-the factory to create services from
        - `xCursor`:XTextCursor-the cursor where to insert the graphic
        - `imgURL`:String- URL of the license button
        """

        try:
            xBitmapContainer=mxDocFactory.createInstance(
                "com.sun.star.drawing.BitmapTable")

            xImage=mxDocFactory.createInstance(
                    "com.sun.star.text.TextGraphicObject")
            #xProps=xImage

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            #TODO:use this link
            #http://www.oooforum.org/forum/viewtopic.phtml?t=87225

            
            try:
                xBitmapContainer.insertByName("imgID", imgURL)
            except Exception, e:
                print "Image imgID already exists"
                traceback.print_exc()                
                xBitmapContainer.removeByName("imgID")
                xBitmapContainer.insertByName("imgID", imgURL)
                #raise e

                
            
            internalURL=xBitmapContainer.getByName("imgID")

            xImage.setPropertyValue("AnchorType",AS_CHARACTER)
            xImage.setPropertyValue("GraphicURL", internalURL)
            xImage.setPropertyValue("Width", 3104)
            xImage.setPropertyValue("Height", 1093)

            #insert the graphic at the cursor position
            xCursor.getText().insertTextContent(xCursor, xImage, False)

            #remove the helper-entry
            xBitmapContainer.removeByName("imgID")
            
            
            

        except Exception, ex:
            traceback.print_exc()

    def insertVisibleNotice(self, ):
        """
    """
        docLicense=super(Writer,self).getDocumentLicense()

        if docLicense is None:
            return

        
        try:
            mxDoc=self.component
            mxDocText = mxDoc.getText()

            docCursor=mxDoc.getCurrentController().getViewCursor()

            #mxDocFactory=mxDoc

            #mxTextFields=mxDoc

            licenseNameField=self.__createUserTextField(mxDoc,
                    mxDoc, "License Name", docLicense.getName())

            licenseURLField=self.__createUserTextField(mxDoc,
                    mxDoc, "License URL", docLicense.license_uri)

            #insert the license graphic if available
            if (docLicense.getImageUrl() is not None):
                self.__embedGraphic(mxDoc, docCursor, docLicense.getImageUrl())
            #insert the licensing statement
            if (docLicense.getName()=="CC0 1.0 Universal"):
                mxDocText.insertControlCharacter(docCursor, 
                                                 PARAGRAPH_BREAK, False)
                mxDocText.insertString(
                    docCursor, 
                    "To the extent possible under law, the person who"
                    + "associated ", 
                    False)
                mxDocText.insertTextContent(docCursor, licenseNameField, False)
                mxDocText.insertString(docCursor, 
                                       " with this work has waived all "
                        + "copyright and related or neighboring rights to this"
                        + " work. The summary of the Legal Code is" 
                        + "available at ", False)
                mxDocText.insertTextContent(docCursor, licenseURLField, False)
                mxDocText.insertString(docCursor, ".", False)

                if (docLicense.territory is not None):
                    territory=self.__createUserTextField(mxDoc,mxDoc,
                                                         "Territory",
                                                         docLicense.territory)
                    mxDocText.insertString(docCursor, "This work is published"
                                           + "from ", False)
                    mxDocText.insertTextContent(docCursor, territory, False)

                mxDocText.insertControlCharacter(docCursor, PARAGRAPH_BREAK, 
                                                 False)

            elif (docLicense.getName() == "Public Domain"):
                mxDocText.insertControlCharacter(docCursor, PARAGRAPH_BREAK, 
                                                 False)
                mxDocText.insertString(docCursor, "This document is in the ", 
                                       False)
                mxDocText.insertTextContent(docCursor, licenseNameField, False)
                mxDocText.insertString(docCursor, ". The summary of the Legal" 
                                       + "Code is available at ", False)
                mxDocText.insertTextContent(docCursor, licenseURLField, False)
                mxDocText.insertString(docCursor, ".", False)
                mxDocText.insertControlCharacter(docCursor, PARAGRAPH_BREAK, 
                                                 False)

            else:
                mxDocText.insertControlCharacter(docCursor, PARAGRAPH_BREAK, 
                                                 False)
                mxDocText.insertString(docCursor, "This document is licensed"
                                       + "under the ", False)
                mxDocText.insertTextContent(docCursor, licenseNameField, False)
                mxDocText.insertString(docCursor, " license, available at ", 
                                       False)
                mxDocText.insertTextContent(docCursor, licenseURLField, False)
                mxDocText.insertString(docCursor, ".", False)
                mxDocText.insertControlCharacter(docCursor, PARAGRAPH_BREAK, 
                                                 False)

            mxDoc.refresh()

                        
        except Exception, e:
            traceback.print_exc()
            #raise e


    
    def insertPicture(self, img):
        """Insert pictures from the internet.
        
        Arguments:
        - `img`:Image
        """
        #mxDoc=self.component

        docCursor=self.component.getCurrentController().getViewCursor()

        #mxDocFactory=self.component

        xBitmapContainer=None
        xImage=None
        internalURL=None

        try:
            xBitmapContainer=self.component.createInstance(
                    "com.sun.star.drawing.BitmapTable")
            xImage=self.component.createInstance(
                    "com.sun.star.text.TextGraphicObject")
            #xProps=xImage

            #helper-stuff to let OOo create an internal name of the graphic
            #that can be used later (internal name consists of various checksums)

            #Static class method call
            imgId=img.getPhotoID()
            sName = createUniqueName(xBitmapContainer,imgId )
            xBitmapContainer.insertByName(sName, img.getSelectedImageURL())

            internalURL=xBitmapContainer.getByName(sName)

            xImage.setPropertyValue("AnchorType",AS_CHARACTER)
            xImage.setPropertyValue("GraphicURL", internalURL)

            #insert the graphic at the cursor position
            size=xImage.getPropertyValue("ActualSize")

            if (size.Width != 0):
                xImage.setPropertyValue("Width", size.Width)
            else:
                xImage.setPropertyValue("Width", img.getSelectedImageWidth())

            if (size.Height != 0):
                xImage.setPropertyValue("Height", size.Height)
            else:
                xImage.setPropertyValue("Height", img.getSelectedImageHeigth())

            #remove the helper-entry
            xBitmapContainer.removeByName(sName)

            byCaption = ""
            if (img.getLicenseCode() =="by"):
                byCaption = "CC BY "
            else:
                byCaption = img.getLicenseCode().upper()+" "

            docCursor.getText().insertControlCharacter(docCursor,
                                    PARAGRAPH_BREAK, False)
            
            caption = img.getTitle() + " ( " + \
              img.getImgUrlMainPage()+ " ) / " + byCaption + \
              img.getLicenseNumber()+ " ( " + img.getLicenseURL() + " )"
                
            docCursor.getText().insertString(docCursor, caption, False)    
            
            
            
        except Exception, ex:
                print "Exception in Writer.insertPicture: "
                print ex
                print type(ex)
                #raise ex

    def updateVisibleNotice(self, ):
        """
        """
        #TODO-method to change the visible notice
        pass

    def hasVisibleNotice(self, ):
        """
        """
        #TODO-Should this be implemented?
        raise NotImplementedError("Writer.hasVisibleNotice")
