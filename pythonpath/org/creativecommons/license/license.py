#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from rdflib import Namespace
import traceback

#from org.creativecommons.license.store import Store
from org.creativecommons.license.store import object, literal, exists
from org.creativecommons.license.unported import Unported
from org.creativecommons.license.jurisdiction import Jurisdiction


class License():
    """
    """
    CC = Namespace("http://creativecommons.org/ns#")
    DCTerms = Namespace("http://purl.org/dc/terms/")
    DC = Namespace("http://purl.org/dc/elements/1.1/")

    def __init__(self, license_uri, territory=None):
        """
        Arguments:
        - `license_uri`:String
        - `territory`:String
        """
        self.license_uri = license_uri
        #self.licenseStore = store

        #Creates a new instance of License with a territory (for PD).
        if territory is not None:
            self.territory = territory

        else:
            self.territory = None

        ####Jurisdiction####
        jurisdiction = object(self.license_uri, self.CC['jurisdiction'])
        if jurisdiction is not None:
            self.jurisdiction = Jurisdiction(str(jurisdiction))

        else:
            self.jurisdiction = Unported()

        ####name####

        title = literal(self.license_uri, self.DC['title'], "en")
        version = literal(self.license_uri, self.DCTerms['hasVersion'], None)
        juri = str(self.jurisdiction.getTitle())

        if not title:
            #CC0 license
            self.name = "CC0" + " " + str(version) + " " + "Universal"
        elif not version:
            #PD license
            self.name = str(title)
        else:
            #CC license
            self.name = str(title) + " " + str(version) + " " + juri

        ####requireShareAlike####
        self.requireShareAlike = exists(
              self.license_uri, self.CC['requires'], self.CC['ShareAlike'])

        ####prohibitCommercial####
        self.prohibitCommercial = exists(
              self.license_uri, self.CC['prohibits'], self.CC['CommercialUse'])

        ####allowRemix####
        self.allowRemix = exists(
              self.license_uri, self.CC['permits'], self.CC['DerivativeWorks'])

        ####code####
        #Return the license code for this License.
        #For example, the code for the
        #Attribution 3.0 license
        #(http://creativecommons.org/licenses/by/3.0/) is
        #"by".  Note this is based on a
        #Creative Commons-specific standard.
        try:
            self.code = self.license_uri.split('/')[4]
        except Exception, ex:
            traceback.print_exc()

        ####version####
        self.version = str(literal(self.license_uri,
                                             self.DCTerms['hasVersion'], None))

        ####Image URL####
        if self.version is not None:
            self.imageUrl =\
               ("http://i.creativecommons.org/l/" + self.code + "/"
                    + self.version + "/88x31.png")
        else:
            self.imageUrl =\
               ("http://i.creativecommons.org/l/" +\
                self.getCode() + "/88x31.png")
