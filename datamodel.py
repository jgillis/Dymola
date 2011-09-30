from numpy import reshape, array, vstack, double, ndarray, nonzero, hstack, sign, append
from dymmodel import *
import re
import copy

def istime(name):
  return name=="t" or name=="time"

def makecolumn(data):
  data=array(data)
  return reshape(data,(data.size,1))

def makerow(data):
  data=array(data)
  return reshape(data,(1,data.size))


def append1(a,r):
        if a.size==0:
          return makerow(r)
        else:
          return vstack((a,makerow(r)))
          
def append2(a,r):
        if a.size==0:
          return makecolumn(r)
        else:
          return hstack((a,makecolumn(r)))
          
class AnnotatedDataModel:
  def __init__(self,data=dict()):
    if type(data)==type(""):
      self.importDymModel(DymModel(data))
    else:
      self.data=dict(data)
    
  def add(self,a):
    if isinstance(a,AnnotatedData):
      if a.annotation.name in self.data:
        raise Exception("AnnotatedDataModel: add: there allready is a variable with name '%s'" % a.annotation.name)
      self.data[a.annotation.name]=a
    elif isinstance(a,dict):
      for k,v in a.items():
        if not(isinstance(v,str)):
          self.add(AnnotatedData(v,Annotation(k)))
    else:
      raise Exception("AnnotatedDataModel: add: expecting AnnotatedData as argument")
      
  def addParams(self,a):
    for k,v in a.items():
      if not(isinstance(v,str)):
        self.add(AnnotatedData(v,Annotation(k)))

  def addSeries(self,a):
    for k,v in a.items():
      if istime(k):
        self.add(AnnotatedData(v,Annotation(k)))
      else:
        self.add(AnnotatedData(v,Annotation(k,dep='t')))

  def __str__(self):
    s="-----\n"
    for it in self.data.itervalues():
      s=s+ str(it) + "\n"
    return s+"----\n"
  
  def exportDymModel(self):
    """
    Represent the current data as DymModel.
    Returns a DymModel object
    """
    
    hasTime = False
    for key in self.data.iterkeys():
      if istime(self.data[key].annotation.name):
        hasTime = True
    
    if (not(hasTime)):
      self.add(AnnotatedData([0,1],Annotation("t")))
    
    other=copy.deepcopy(self)
    other.vectorize()
    
    mykeys = sorted(other.data.iterkeys())
    i = nonzero([istime(i) for i in mykeys])[0][0]
    t = mykeys[i] 
    del mykeys[i]
    mykeys = [t] + mykeys
    
    name=[]
    description=[]
    data=[array([]),array([])]
    dataInfo=array([])
    
    cnt1=1
    cnt2=1
    
    
    for key in mykeys:
      d=other.data[key]
      if istime(d.annotation.name):
        name.append("time")
        description.append("Time in [%s]" % d.annotation.unit)
        dataInfo=append1(dataInfo,[0,1,0,0])
        data[1]=append2(data[1],d.data)
        data[0]=append2(data[0],d.data[[0,-1]])
      elif istime(d.annotation.dep):
        name.append(d.annotation.name)
        desc=d.annotation.description
        if d.annotation.unit:
          desc=desc+" [%s]" % d.annotation.unit
        description.append(desc)
        cnt2=cnt2+1
        dataInfo=append1(dataInfo,[2,cnt2,0,0])
        data[1]=append2(data[1],d.data)
      else:
        name.append(d.annotation.name)
        desc=d.annotation.description
        if d.annotation.unit:
          desc=desc+" [%s]" % d.annotation.unit
        description.append(desc)
        cnt1=cnt1+1
        dataInfo=append1(dataInfo,[1,cnt1,0,0])
        data[0]=append2(data[0],[d.data,d.data])
        
    return DymModel(name,description,dataInfo,data)
    
  def importDymModel(self,m):
    """
    Reads a DymModel object.
    """
    self.data=dict()
    r = re.compile("^(.*?)\s*\[(.*?)\]$")
      
    for i in range(len(m.name)):
      unit=""
      mt = r.match(m.description[i])
      if mt:
        description=mt.group(1)
        unit=mt.group(2)
      else:
        unit=""
        description=m.description[i]
      name = m.name[i]
      if istime(m.name[i]):
        name= "t"
        
      if m.dataInfo[i,0] == 0:
        if len(m.data)>1:
          data=sign(m.dataInfo[i,1])*m.data[1][:,abs(m.dataInfo[i,1])-1]
        else:
          data=sign(m.dataInfo[i,1])*m.data[0][:,abs(m.dataInfo[i,1])-1]
        dep=None
      elif m.dataInfo[i,0] == 1:
        data=sign(m.dataInfo[i,1])*m.data[0][0,abs(m.dataInfo[i,1])-1]
        dep = None
      elif m.dataInfo[i,0] == 2:
        data=sign(m.dataInfo[i,1])*m.data[1][:,abs(m.dataInfo[i,1])-1]
        dep = "t"
      
      self.data[m.name[i]]=AnnotatedData(data,Annotation(name=name,unit=unit,dep=dep,description=description))
    self.unvectorize()
    
  def hasvecnames(self):
    r=re.compile("\[\d+?\]")
    for key in self.data.iterkeys():
      if r.search(key):
         return True
    return False
    
  def isvectorised(self):
    for key in list(self.data.iterkeys()):
      d=self.data[key]
      if isinstance(d.data,ndarray) and not(istime(d.annotation.name)):
        d.data=d.data.squeeze()
        if (((d.annotation.dep  is None) and (len(d.data.shape)>0)) or \
           (not(d.annotation.dep  is None) and (len(d.data.shape)>1))):
              return False
    return True
    
  def iterParam(self):
    for k,v in self.data.iteritems():
      if v.isConstant():
        yield (k,v)
        
  def iterSeries(self):
    for k,v in self.data.iteritems():
      if not(v.isConstant()):
        yield (k,v)
    
  def vectorize(self):
    """
    foo=[1,2,3]
    foo[1] = 1
    foo[2] = 2
    foo[3] = 3
    """
    while not(self.isvectorised()):
      for key in list(self.data.iterkeys()):
        d=self.data[key]
        if isinstance(d.data,ndarray) and not(istime(d.annotation.name)):
          d.data=d.data.squeeze()
          if (d.annotation.dep  is None) and (len(d.data.shape)>0):
             for i in range(d.data.shape[0]):
               self.data[key+"[%d]" % (i+1)] = AnnotatedData(
                  d.data[i,...],
                  Annotation(
                    name=d.annotation.name+"[%d]" % (i+1),
                    description=d.annotation.description,
                    unit=d.annotation.unit,
                    dep=d.annotation.dep
                    )
                 )  
             del self.data[key]
     
          if not(d.annotation.dep  is None) and (len(d.data.shape)>1):
             for i in range(d.data.shape[1]):
               self.data[key+"[%d]" % (i+1)] = AnnotatedData(
                  d.data[:,i,...],
                  Annotation(
                    name=d.annotation.name+"[%d]" % (i+1),
                    description=d.annotation.description,
                    unit=d.annotation.unit,
                    dep=d.annotation.dep
                    )
                 )

             del self.data[key]
    
  def unvectorize(self):
    while self.hasvecnames(): 
      for key in sorted(self.data.iterkeys()):
        m = re.match(r"^(.*)\[(\d+?)\]$", key)
        if m:
          reducedname=m.group(1)
          s = int(m.group(2))
          a=self.data[key].data.squeeze()
          if s  == 1:
            self.data[reducedname]=AnnotatedData(
                  reshape(a,(1,)+a.shape),
                  Annotation(
                    name=reducedname,
                    description=self.data[key].annotation.description,
                    unit=self.data[key].annotation.unit,
                    dep=self.data[key].annotation.dep
                    )
                 )
          else:
            self.data[reducedname].data=append(self.data[reducedname].data,reshape(a,(1,)+a.shape),axis=0)
          del self.data[key]
  

class Annotation:
  """
  
  name
  description
  unit
  dep : name/None (probably 't')
  
  """
  def __init__(self,name="",description="",unit="",dep=None):
    self.name=name
    self.description=description
    if unit=="" and istime(self.name):
      self.unit="s"
    else:
      self.unit=unit
    self.dep=dep

  def __str__(self):
    s=""
    if self.name:
      s=s+self.name
    if self.description:
      s=s+" (%s)" % self.description
    if self.unit:
      s=s+" [%s]" % self.unit
    if self.dep:
      s=s+" <%s>" % self.dep
    return s
   
   
     
class AnnotatedData:
  def __init__(self,data,annotation=Annotation()):
    if isinstance(data,double) or isinstance(data,float) or isinstance(data,int):
      self.data=double(data)
    else:
      self.data=array(data)
    self.annotation=annotation
    
  def __str__(self):
    return str(self.data) + ": " + str(self.annotation)
    
  def isConstant(self):
    return self.annotation.dep is None
   
