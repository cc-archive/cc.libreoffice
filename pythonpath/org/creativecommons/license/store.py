#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import os
import rdflib

from rdflib.graph import Graph
from rdflib import RDF
from rdflib import Literal
from rdflib.resource import Resource
from rdflib.term import URIRef
from rdflib import Namespace

#from org.creativecommons.license.cc import CC

import threading

RDF_GRAPH = None


class RdfLoaderThread(threading.Thread):
    """Parses the rdf Graph in a Thread
    """
    def run(self, ):
        """
        """
        print "Thread started to parse!"
        #print RDF_GRAPH
        global RDF_GRAPH
        RDF_GRAPH = rdflib.Graph()

        path = os.path.join(os.path.dirname(__file__), './rdf/schema.rdf')
        RDF_GRAPH.parse(path)

        path = os.path.join(os.path.dirname(__file__), './rdf/index.rdf')
        RDF_GRAPH.parse(path)

        path = os.path.\
          join(os.path.dirname(__file__), './rdf/jurisdictions.rdf')
        RDF_GRAPH.parse(path)
        print "Thread end!"

        #RdfLoaderThread().start()
        #print "RDF_GRAPH-" + str(RDF_GRAPH)

# try:
#         RDF_GRAPH
# except NameError:
#         print "not defined"
#         RdfLoaderThread().start()
#         #RDF_GRAPH=None
#         print "calling parse graphx-exception"

#         #RDF_GRAPH = None

NS = Namespace("http://creativecommons.org/ns#")


def parseGraph():
    """Parsess the rdf graphs.
    """
    print "begin parsing"

    RDF_GRAPH = rdflib.Graph()

    path = os.path.join(os.path.dirname(__file__), './rdf/schema.rdf')
    RDF_GRAPH.parse(path)

    path = os.path.join(os.path.dirname(__file__), './rdf/index.rdf')
    RDF_GRAPH.parse(path)

    path = os.path.join(os.path.dirname(__file__), './rdf/jurisdictions.rdf')
    RDF_GRAPH.parse(path)
    print "end parsing"
    #return RDF_GRAPH


def jurisdictions():
    """Get the jurisdictions
    """
    if RDF_GRAPH is None:
        print "rdf is none"
        #RDF_GRAPH=parseGraph()
        parseGraph()

    jur = RDF_GRAPH.subjects(RDF.type, NS.Jurisdiction)

    #the empty list
    jurList = []

    for uri in jur:
        jurList.append(uri)

    jurList.sort()

    return jurList


def literal(sub, pred, lang):
    """Returns a Literal object

    Arguments:
    - `subject`:String
    - `predicate`:String
    - `lang`:String
    """

    if RDF_GRAPH is None:
        parseGraph()

    #get generator over the objects in case there's more than one
    gen = RDF_GRAPH.objects(URIRef(sub), predicate=pred)
    #gen=self.g.transitive_objects(sub,pred)
    #gen=self.g.value(subject=sub,predicate=pred)

    #print "++++++++++++++"
    #print sub
    #print pred

    for it in gen:
        # print it
        #print type(it)
        #break
        if isinstance(it, Literal):
            #if lang is set
            if lang is not None:
                if it.language == lang:
                    #this is a literal, in the language we care about
                    return it
            else:
                return it
    # ##Changed
    # gen=self.g.predicate_objects(subject)
    # print "subject:"+str(subject)
    # for it in gen:
    #     print "it"+str(it)
    #     break
    #     if isinstance(it,Literal):
    #         return it

    return None


def object(subject, predicate):
    """Get the object of the RDF triple

    Arguments:
    - `subject`: String
    - `predicate`: String
    """

    if RDF_GRAPH is None:
        parseGraph()

    #get generator over the objects in case there's more than one
    print subject
    print predicate
    gen = RDF_GRAPH.objects(URIRef(subject), predicate)
        
    for it in gen:

        print it
        # if isinstance(it, Resource):
        #     #this is a Resource
        #     return it
        return it

    return None


def exists(subject, predicate, resource):
    """Check whteher a given condition exists

    Arguments:
    - `subject`:
    - `predicate`:
    - `object`:
    """
    if RDF_GRAPH is None:
        parseGraph()

    gen = RDF_GRAPH.triples((subject, predicate, resource))

    #TODO: find a better way to do this checking

    exists = False

    #check for elements in the generator
    for dd in gen:
        #if an element exists, a triple exists
        exists = True
        #checking for one triple is enough
        break

    return exists


def query(queryString):
    """queries the graph using the given sparql
    string and returns the results.

    Arguments:
    - `queryString`: A sparql query string
    """
    return RDF_GRAPH.query(queryString,
        initNs=dict(
                cc=Namespace("http://creativecommons.org/ns#"),
                dc=Namespace("http://purl.org/dc/elements/1.1/"),
                dcq=Namespace("http://purl.org/dc/terms/"),
                rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")))


# class Store():
#     """
#     """
#     g = rdflib.Graph()

#     path = os.path.join(os.path.dirname(__file__), './rdf/schema.rdf')
#     g.parse(path)

#     path = os.path.join(os.path.dirname(__file__), './rdf/index.rdf')
#     g.parse(path)

#     path = os.path.join(os.path.dirname(__file__), './rdf/jurisdictions.rdf')
#     g.parse(path)

#     _instance = None

#     NS = Namespace("http://creativecommons.org/ns#")

#     def __new__(cls, *args, **kwargs):
#         """Create a singleton instance of the class
#         """
#         # if not cls._instance:
#         #     cls._instance = super(Store, cls).__new__(
#         #                         cls, *args, **kwargs)
#         # return cls._instance

#         if cls._instance is not None:
#             return cls._instance

#         cls._inst = object.__new__(cls, *args, **kwargs)
#         return cls._instance

#     def __init__(self, ):
#         """
#         """
#         pass

#     #model=graph=g
#         #self.g = rdflib.Graph()

#         # path=os.path.join(os.path.dirname(__file__), './rdf/schema.rdf')
#         # self.g.parse(path)

#         # path=os.path.join(os.path.dirname(__file__), './rdf/index.rdf')
#         # self.g.parse(path)

#         # path=os.path.join(os.path.dirname(__file__), './rdf/jurisdictions.rdf')
#         # self.g.parse(path)

#     def jurisdictions(self, ):
#         """Get the jurisdictions
#         """
#         jur = self.g.subjects(RDF.type, self.NS.Jurisdiction)

#         #the empty list
#         jurList = []

#         for uri in jur:
#             jurList.append(uri)

#         jurList.sort()

#         return jurList

#     def literal(self, sub, pred, lang):
#         """Returns a Literal object

#         Arguments:
#         - `subject`:String
#         - `predicate`:String
#         - `lang`:String
#         """
#         #get generator over the objects in case there's more than one
#         gen = self.g.objects(URIRef(sub), predicate=pred)
#         #gen=self.g.transitive_objects(sub,pred)
#         #gen=self.g.value(subject=sub,predicate=pred)

#         #print "++++++++++++++"
#         #print sub
#         #print pred

#         for it in gen:
#             # print it
#             #print type(it)
#             #break
#             if isinstance(it, Literal):
#                 #if lang is set
#                 if lang is not None:
#                     if it.language == lang:
#                         #this is a literal, in the language we care about
#                         return it
#                 else:
#                     return it
#         # ##Changed
#         # gen=self.g.predicate_objects(subject)
#         # print "subject:"+str(subject)
#         # for it in gen:
#         #     print "it"+str(it)
#         #     break
#         #     if isinstance(it,Literal):
#         #         return it

#         return None

#     def object(self, subject, predicate):
#         """Get the object of the RDF triple

#         Arguments:
#         - `subject`: String
#         - `predicate`: String
#         """
#         #get generator over the objects in case there's more than one
#         gen = self.g.objects(subject, predicate)

#         for it in gen:

#             if isinstance(it, Resource):
#                 #this is a Resource
#                 return it
#         return None

#     def exists(self, subject, predicate, resource):
#         """Check whteher a given condition exists

#         Arguments:
#         - `subject`:
#         - `predicate`:
#         - `object`:
#         """

#         gen = self.g.triples((subject, predicate, resource))

#         #TODO: find a better way to do this checking

#         exists = False

#         #check for elements in the generator
#         for dd in gen:
#             #if an element exists, a triple exists
#             exists = True
#             #checking for one triple is enough
#             break

#         return exists
