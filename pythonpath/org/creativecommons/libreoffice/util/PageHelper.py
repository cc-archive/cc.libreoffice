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
    def createUniqueName(self, _xElementContainer,_sElementName):
        """makes a String unique by appending a numerical suffix 
        
        
        Arguments:
        - `_xElementContainer`:the com.sun.star.container.XNameAccess container
        that the new Element is going to be inserted to
        - `_sElementName`: the StemName of the Element
        """
        bElementexists = True

        i = 1
        BaseName = _sElementName
        while bElementexists:
            bElementexists = _xElementContainer.hasByName(_sElementName)
            if bElementexists:
                i=i+1
                _sElementName = BaseName+str(i)

            return _sElementName
