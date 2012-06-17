#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info


#import isodate
import rdflib

class Store():
    """
    """
    
    def __init__(self, ):
        """
        """
        
        #model=graph=g
        g = rdflib.Graph()
        result = g.parse("http://www.w3.org/People/Berners-Lee/card")
        print("graph has %s statements." % len(g))
        
        
        
