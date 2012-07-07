#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

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
