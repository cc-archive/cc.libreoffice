#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from org.creativecommons.license.store import Store
from rdflib import Namespace

class Jurisdiction():
    """
    """

    
    
    def __init__(self, uri):
        """
        
        Arguments:
        - `uri`:
        """
        self.uri = uri

    @staticmethod
    def byId(id):
        """
        
        Arguments:
        - `id`:String
        """
        #TODO:This was a class wide variable
        JURIS_BASE = "http://creativecommons.org/international/"
        return Jurisdiction(JURIS_BASE + id + "/")

    def __repr__(self):
        return self.uri

    # def getTitle(self, ):
    #     """
    #     """
    #     return self.getTitle("en")
        
    def getTitle(self, lang=None):
        """
        
        Arguments:
        - `lang`:String
        """

        if lang is None:
            lang="en"
            
        DC= Namespace("http://purl.org/dc/elements/1.1/")
        
        dcTitle=DC['title']

        title=Store().literal(self.uri,dcTitle,lang)


        if title:
            return str(title)

        return ""

    def compareTo(self, other):
        """
        
        Arguments:
        - `other`:Jurisdiction
        """
        
        return cmp(self.getTitle(),other.getTitle())

