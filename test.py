import uno

import unohelper


from com.sun.star.task import XJobExecutor





class SetSharing( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx
        pass
        

    def trigger( self, args ):
        
        # retrieve the desktop object
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx )

        print 'hi from set sharing!'
        print args
     
        

class InsertSharing( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx
        pass
        

    def trigger( self, args ):
        
        # retrieve the desktop object
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx )

        print 'hi from InsertSharing!'
        print args
     
        	
       


       
            
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        InsertSharing,
        "org.creativecommons.openoffice.ccooo.Import",
        ("com.sun.star.task.Job",),)


            
#g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        SetSharing,
        "org.creativecommons.openoffice.ccooo.SetSharing",
        ("com.sun.star.task.Job",),)
