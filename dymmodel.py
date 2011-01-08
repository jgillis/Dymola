from numpy import array
from dymola.dymio import ResultDymolaTextual

class DymModel:
  def __init__(self,name=[],description=[],dataInfo=array([]),data=[]):
    if type(name)==type(""):
      self.loadText(name)
    else:
      self.name=name
      self.description=description
      self.dataInfo=dataInfo
      self.data=data
    
  def __str__(self):
    return "name = %s \n description = %s \n dataInfo = %s \n data_1 = %s \n data_2 = %s" % (self.name,self.description,self.dataInfo,self.data[0],self.data[1])
 
  def loadText(self,f):
    """
    Serialize the current DymModel to a dymola text file
    
    Parameters::
            
         f --
            file object
    """
    dym=ResultDymolaTextual(f)
    self.name=dym.name
    self.dataInfo=dym.dataInfo
    self.description=dym.description
    self.data=dym.data
    
     
  def saveText(self,f):
    """
    Serialize the current DymModel to a dymola text file
    
    Parameters::
            
         f --
            file object
    """
    
    
  def saveMat(self,f):
    """
    Serialize the current DymModel to a mat file
    
    Parameters::
            
         f --
            file object
    """
    raise Exception("Not implemented yet")
