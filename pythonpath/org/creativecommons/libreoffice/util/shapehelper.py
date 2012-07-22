#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback

from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER


def createShape(xDrawDoc, aPos, aSize, sShapeType):
    """create a Shape

    Arguments:
    - `xDrawDoc`:XComponent
    - `aPos`:Point
    - `aSize`:Size
    - `sShapeType`:String
    """
    try:
        #xFactory=xDrawDoc
        xShape = xDrawDoc.createInstance(sShapeType)
        xShape.setPosition(aPos)
        xShape.setSize(aSize)
        return xShape
    except Exception, e:
        traceback.print_exc()
        raise e


def addPortion(xShape, sText, bNewParagraph):
    """add text to a shape. the return value is the PropertySet
        of the text range that has been added

        Arguments:
        - `xShape`:XShape-
        - `sText`:String
        - `bNewParagraph`:Boolean
        """
    try:
        #xText=xShape
        xTextCursor = xShape.createTextCursor()
        xTextCursor.gotoEnd(False)

        if bNewParagraph:
            xShape.insertControlCharacter(xTextCursor, PARAGRAPH_BREAK, False)
            xTextCursor.gotoEnd(False)

        #xTextRange=xTextCursor
        xTextCursor.setString(sText)
        xTextCursor.gotoEnd(True)
        return xTextCursor
    except Exception, e:
        traceback.print_exc()
        #raise e
