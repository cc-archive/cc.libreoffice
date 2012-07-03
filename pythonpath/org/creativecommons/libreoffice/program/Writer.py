#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback

#from com.sun.star.uno import AnyConverter
#from com.sun.star.uno import AnyConverter 
#import com.sun.star.uno.AnyConverter

from org.creativecommons.libreoffice.program.OOoProgram import OOoProgram
from org.creativecommons.libreoffice.util.PageHelper import PageHelper


class Writer(OOoProgram):
    """
    """
    
    def __init__(self, component,m_xContext):
        """
        
        Arguments:
        - `component`:
        - `m_xContext`:
        """
        super(Writer,self).__init__(component,m_xContext)

    
    def __getMasterField(field_name,mxTextFields,mxDocFactory):
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
            masterFieldName = "com.sun.star.text.FieldMaster.User." + field_name
            
            #see if the user field already exists
            if (mxTextFields.getTextFieldMasters().hasByName(masterFieldName)):
                xMasterPropSet=mxTextFields.getTextFieldMasters().getByName(masterFieldName)

            else:
                #Create a fieldmaster for our newly created User Text field, and
                #access it's XPropertySet interface

                xMasterPropSet=mxDocFactory.createInstance(
                "com.sun.star.text.FieldMaster.User")

                xMasterPropSet.setPropertyValue("Name", field_name)

                return xMasterPropSet
            
        except Exception, e:
            traceback.print_exc()
            raise e

        
        
    #TODO-Complete the method
    def __updateMasterField(self, field_name,field_value,mxTextFields,mxDocFactory):
        """
        
        Arguments:
        - `field_name`:String
        - `field_value`:String
        - `mxTextFields`:XTextFieldsSupplier
        - `mxDocFactory`:XMultiServiceFactory
        """
        
        try:
            #get or create the master field
            xMasterPropSet = self.__getMasterField(field_name, mxTextFields, mxDocFactory)

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

        

    #TODO: Complete the Method
    def __embedGraphic(self, mxDocFactory,xCursor,imgURL):
        """Embeds the license "button" into a Textdocument at the given cursor position
        
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

            xBitmapContainer.insertByName("imgID", imgURL)

            

        except Exception, ex:
            traceback.print_exc()
        

    #TODO: Complete the method
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
            sName = PageHelper.createUniqueName(xBitmapContainer, img.getPhotoID())
            xBitmapContainer.insertByName(sName, img.getSelectedImageURL())

            ##TODO:partially Implemented

            
            
        except Exception, ex:
                print "Exception in Writer.insertPicture: "
                print ex
                print type(ex)
                #raise ex

    
