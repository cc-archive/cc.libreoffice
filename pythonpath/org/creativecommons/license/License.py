#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

from rdflib import Namespace
import traceback

from org.creativecommons.license.Store import Store
from org.creativecommons.license.Unported import Unported
from org.creativecommons.license.Jurisdiction import Jurisdiction

class License():
    """
    """
    CC=Namespace("http://creativecommons.org/ns#")
    DCTerms=Namespace("http://purl.org/dc/terms/")
    
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
        
        
        return str(self.licenseStore.literal(self.license_uri,DC['title'],"en"))+""
        +str(self.licenseStore.literal(self.license_uri,self.DCTerms['hasVersion'],""))+""
        +self.getJurisdiction().getTitle()


    def getJurisdiction(self, ):
        """Get the jurisdiction.
        """
        
        jurisdiction=self.licenseStore.object(self.license_uri,self.CC['jurisdiction'])
        if jurisdiction is not None:
            return Jurisdiction(jurisdiction.identifier)

        return Unported()
        
    def requireShareAlike(self, ):
        """
        """
        return self.licenseStore.exists(self.license_uri,self.CC['requires'],self.CC['ShareAlike'])

    def prohibitCommercial(self, ):
        """
        """
        
        
        return self.licenseStore.exists(self.license_uri,self.CC['prohibits'],self.CC['CommercialUse'])

    def allowRemix(self, ):
        """
        """
        return self.licenseStore.exists(self.license_uri,self.CC['permits'],self.CC['DerivativeWorks'])

    def getCode(self, ):
        """Return the license code for this License.  For example, the code for the
        Attribution 3.0 license (http://creativecommons.org/licenses/by/3.0/) is
        "by".  Note this is based on a Creative Commons-specific standard.
        """
        try:
            return self.license_uri.split('/')[4]
        except Exception, ex:
            traceback.print_exc()

    def getVersion(self, ):
        """License version
        """

        version=self.licenseStore.literal(self.license_uri,
                                             self.DCTerms['hasVersion'],"")
        if version is None:
            return None
        
        return str(version)

    def getImageUrl(self, ):
        """
        """
        version=self.getVersion()

        if version is not None:
            return ("http://i.creativecommons.org/l/" + self.getCode() + "/"
                    + version + "/88x31.png")

        else:
            return ("http://i.creativecommons.org/l/" + self.getCode() + "/88x31.png")

    
