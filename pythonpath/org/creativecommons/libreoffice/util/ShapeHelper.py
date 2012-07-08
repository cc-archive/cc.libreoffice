#Author: Ishan Thilina Somasiri
#E-mail: ishan@ishans.info
#Blog: www.blog.ishans.info

import traceback

def createShape(xDrawDoc,aPos,aSize,sShapeType):
    """create a Shape
    
    Arguments:
    - `xDrawDoc`:XComponent
    - `aPos`:Point
    - `aSize`:Size
    - `sShapeType`:String
    """
    
    try:
	#xFactory=xDrawDoc
        xShape=xDrawDoc.createInstance( sShapeType )
        xShape.setPosition( aPos )
        xShape.setSize( aSize )
        return xShape
    except Exception, e:
	traceback.print_exc()
	raise e

