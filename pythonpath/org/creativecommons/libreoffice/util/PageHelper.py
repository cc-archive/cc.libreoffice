#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback

class PageHelper():
    """
    """
    
    def __init__(self, ):
        """
        """
        
        pass
    
    @staticmethod
    def createUniqueName(_xElementContainer,elementName):
        """makes a String unique by appending a numerical suffix 
        
        
        Arguments:
        - `_xElementContainer`:the com.sun.star.container.XNameAccess container
        that the new Element is going to be inserted to
        - `_elementName`: the StemName of the Element
        """
        bElementexists = True

        i = 1
        BaseName = elementName
        while bElementexists:
            bElementexists = _xElementContainer.hasByName(elementName)
            if bElementexists:
                i=i+1
                elementName = BaseName+str(i)

        return elementName


def getDrawPageCount(xComponent):
    """get the page count for standard pages
    
    Arguments:
    - `xComponent`:XComponent
    """
    
    try:
	xDrawPages=xComponent.getDrawPages()
        return xDrawPages.getCount()
    except Exception, e:
	traceback.print_exc()
	raise e


def getDrawPageByIndex(xComponent,nIndex):
    """get draw page by index
    
    Arguments:
    - `xComponent`:XComponent
    - `nIndex`:Integer
    """

    
    try:
	#xDrawPagesSupplier=xComponent
        xDrawPages = xComponent.getDrawPages()
        return xDrawPages.getByIndex( nIndex )
    
    except Exception, e:
	traceback.print_exc()
	raise e

