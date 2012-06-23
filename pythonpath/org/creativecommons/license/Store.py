#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import os


#import isodate
import rdflib
from rdflib import plugin
from rdflib.graph import Graph
from rdflib import RDF

from org.creativecommons.license.CC import CC

#register the plugins

plugin.register(
    'sparql', rdflib.query.Processor,
    'rdfextras.sparql.processor', 'Processor')

plugin.register(
    'sparql', rdflib.query.Result,
    'rdfextras.sparql.query', 'SPARQLQueryResult')



class Store():
    """
    """
    
    def __init__(self, ):
        """
        """
        
        #model=graph=g
        self.g = rdflib.Graph()

        path=os.path.join(os.path.dirname(__file__), './rdf/schema.rdf')
        self.g.parse(path)

        path=os.path.join(os.path.dirname(__file__), './rdf/index.rdf')
        self.g.parse(path)

        path=os.path.join(os.path.dirname(__file__), './rdf/jurisdictions.rdf')
        self.g.parse(path)



    def jurisdictions(self, ):
        """Get the jurisdictions
        """
                
        jur= self.g.subjects(RDF.type, CC.Jurisdiction)

        #the empty list
        jurList=[]
        
        for uri in jur:
            jurList.append(uri)

        jurList.sort()

        return jurList
       
        
        
        
