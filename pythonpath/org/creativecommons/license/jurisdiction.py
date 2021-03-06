#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

#from org.creativecommons.license.store import Store
from org.creativecommons.license.store import literal
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

    def __repr__(self):
        return self.uri

    def getTitle(self, lang=None):
        """
        Arguments:
        - `lang`:String
        """

        if lang is None:
            lang = "en"

        DC = Namespace("http://purl.org/dc/elements/1.1/")

        dcTitle = DC['title']

        title = literal(self.uri, dcTitle, lang)

        if title:
            return str(title)

        return ""

    def compareTo(self, other):
        """
        Arguments:
        - `other`:Jurisdiction
        """
        return cmp(self.getTitle(), other.getTitle())
