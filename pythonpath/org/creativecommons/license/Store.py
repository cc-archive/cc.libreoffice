#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import os


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

        path=os.path.join(os.path.dirname(__file__), './rdf/schema.rdf')
        g.parse(path)

        path=os.path.join(os.path.dirname(__file__), './rdf/index.rdf')
        g.parse(path)

        path=os.path.join(os.path.dirname(__file__), './rdf/jurisdictions.rdf')
        g.parse(path)

         
        # g = rdflib.Graph()
        # result = 
        # print("graph has %s statements." % len(g))
        
        
        
