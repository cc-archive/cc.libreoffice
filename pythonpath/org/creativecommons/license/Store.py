#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import os


#import isodate
import rdflib
from rdflib import plugin
from rdflib.graph import Graph
from rdflib import RDF
from rdflib import Literal
from rdflib.resource import Resource

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

    _instance=None

    def __new__(cls, *args, **kwargs):
        """
        """
        if not cls._instance:
            cls._instance = super(Store, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
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


    def literal(self, subject, predicate, lang):
        """Returns a Literal object
        
        Arguments:
        - `subject`:String
        - `predicate`:String
        - `lang`:String
        """

        print "before gen"
        #get generator over the objects in case there's more than one
        gen=self.g.objects(subject,predicate)
        print "affter"
        for it in gen:
            if isinstance(it,Literal):
                if it.language == lang:
                    #this is a literal, in the language we care about
                    return it

        return None


    def object(self, subject, predicate):
        """Get the object of the RDF triple
        
        Arguments:
        - `subject`: String
        - `predicate`: String
        """
        #get generator over the objects in case there's more than one
        gen=self.g.objects(subject,predicate)
        
        for it in gen:
            
            if isinstance(it,Resource):
                #this is a literal, in the language we care about
                return it
            
        return None

    def exists(self, subject,predicate,resource):
        """
    
        Arguments:
        - `subject`:
        - `predicate`:
        - `object`:
        """
        gen=self.g.triples((subject,predicate,resource))

        #TODO: find a better way to do this checking

        exists=False

        #check for elements in the generator
        for dd in gen:
            #if an element exists, a triple exists
            exists=True
            #checking for one triple is enough
            break

        return exists
       
        
        
        
