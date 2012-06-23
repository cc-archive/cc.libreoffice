#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from rdflib import Graph
from rdflib import URIRef
from rdflib import Namespace


class CC():
    """CC vocabulary class for namespace http://creativecommons.org/ns#
    """

    NS =Namespace("http://creativecommons.org/ns#")
    g=Graph()

    
    
    
    License=NS['License']
    Work=NS['Work']
    Jurisdiction=NS['Jurisdiction']

    

    
    
    
    def __init__(self, ):
        """
        """
        
        pass

