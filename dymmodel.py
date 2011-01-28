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
    if not(isinstance(f,file)):
      f=open(f,"write")
    f.write('#1\n')
    f.write('char Aclass(3,11)\n')
    f.write('Atrajectory\n')
    f.write('1.1\n')
    f.write('\n')
    
    # Find the maximum name and description length
    max_name_length = len('Time')
    max_desc_length = len('Time in [s]')
    
    for i in range(len(self.name)):
        name = self.name[i]
        desc = self.description[i]
        
        if (len(name)>max_name_length):
            max_name_length = len(name)
            
        if (len(desc)>max_desc_length):
            max_desc_length = len(desc)

    N = len(self.name)
    f.write('char name(%d,%d)\n' % (N, max_name_length))

    # write names
    for name in self.name:
        f.write(name +'\n')

    f.write('\n')

    f.write('char description(%d,%d)\n' % (N, max_desc_length))

    # write descriptions
    for desc in self.description:
        f.write(desc+'\n')
        
    f.write('\n')

    f.write('int dataInfo(%d,%d)\n' % (len(self.name), 4))

    for i in range(len(self.name)):
      f.write('%d %d %d %d # %s\n' % (self.dataInfo[i,0],self.dataInfo[i,1],self.dataInfo[i,2],self.dataInfo[i,3],self.name[i]))
            
    f.write('\n')

    f.write('float data_1(%d,%d)\n' % (self.data[0].shape))
    for i in range(self.data[0].shape[0]):
      s=''
      for j in range(self.data[0].shape[1]):
        s += "%12.12f " % (self.data[0][i,j])
      f.write(s)
      f.write('\n')
    
    f.write('float data_1(%d,%d)\n' % (self.data[1].shape))
    for i in range(self.data[1].shape[0]):
      s=''
      for j in range(self.data[1].shape[1]):
        s += "%12.12f " % (self.data[1][i,j])
      f.write(s)
      f.write('\n')
      
    f.close()
    
  def saveMat(self,f):
    """
    Serialize the current DymModel to a mat file
    
    Parameters::
            
         f --
            file object
    """
    raise Exception("Not implemented yet")
