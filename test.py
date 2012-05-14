import uno

import unohelper


from com.sun.star.task import XJobExecutor





class Import( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx
        pass
        

    def trigger( self, args ):
        
        # retrieve the desktop object
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx )
     
        

	
       


       
            
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        Import,
        "org.creativecommons.openoffice.ccooo.Import",
        ("com.sun.star.task.Job",),)


