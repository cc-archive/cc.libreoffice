#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from rdflib import Namespace

from org.creativecommons.license import Store
from org.creativecommons.license import Unported

class License():
    """
    """
    
    def __init__(self, license_uri,territory=None):
        """
        
        Arguments:
        - `license_uri`:String
        - `territory`:String
        """
        self.license_uri = license_uri
        self.licenseStore=Store()

        #Creates a new instance of License with a territory (for PD).
        if territory is not None:
            self.territory=territory




    ##TODO:Implemented
    def getName(self, ):
        """Get the license for "en" locale.
        """
        #TODO: implement the Null pointer Exception handling 

        DC= Namespace("http://purl.org/dc/elements/1.1/")
        DCTerms=Namespace("http://purl.org/dc/terms/")
        
        return str(self.licenseStore.literal(self.license_uri,DC['title'],"en"))+""
        +str(self.licenseStore.literal(self.license_uri,DCTerms['hasVersion'],""))+""
        +self.getJurisdiction().getTitle()


    def getJurisdiction(self, ):
        """Get the jurisdiction.
        """
        CC=Namespace("http://creativecommons.org/ns#")
        jurisdiction=self.licenseStore.object(self.license_uri,CC['jurisdiction'])
        if jurisdiction is not None:
            return Jurisdiction(jurisdiction.identifier)

        return Unported()
        
    
