import unittest
from numpy import *
from dymola.datamodel import *
from dymola.simple import *

class Unittests(unittest.TestCase):

  def setUp(self):
    pass  
    
  def test_annotatedConstructor(self):
    d=AnnotatedDataModel()
    d.add(AnnotatedData(5,Annotation("foo")))
    d.add(AnnotatedData([5,12],Annotation("bar",unit="kg")))
    d.add(AnnotatedData(array([[1,2,3],[4,5,6]]),Annotation("baz",unit="kg")))
    d.add(AnnotatedData(array([[[1,2,3],[4,5,6]],[[1,0,0],[5,9,3]]]),Annotation("bak",unit="kg")))
    d.add(AnnotatedData(linspace(0,3,10),Annotation("t")))
    d.add(AnnotatedData(linspace(0,3,10)*2,Annotation("x",unit="m",dep="t")))

    d.add(AnnotatedData(zeros((10,2)),Annotation("yz",unit="m",dep="t")))
   
  def test_dictConstructor(self):
    mydict = {'foo':123,'bar':456,'baz':1.0}
    d=AnnotatedDataModel()
    d.add(mydict)
    d.exportDymModel().saveText("foo.dym")
    dm=AnnotatedDataModel("foo.dym")
    
    
  def test_simple(self):
    mydict = {'foo':123,'bar':456,'baz':1.0}
    saveParams(mydict,"foo")
    mydict2 = loadParams("foo")
    self.comparedicts(mydict,mydict2)

  def test_arrays(self):
    mydict = {'q':array([1.2,3.4]),'w': array([[1.2,3.4],[4,5],[6,7]])}
    saveParams(mydict,"foo")
    mydict2 = loadParams("foo")
    self.comparedicts(mydict,mydict2)
    
  def comparedicts(self,original,other):
    if not('t' in original):
      self.assertTrue('t' in other,"Time should be added automatically")
      del other['t']
    self.assertTrue(set(original.keys())==set(other.keys()),"All dict keys should be preserved in the operation. %s <-> %s" % (str(original.keys()),str(other.keys())))
    for k in original.iterkeys():
      a = original[k]
      b = other[k]
      if isinstance(a,ndarray):
        self.assertEqual(a.shape,b.shape,"Array lengths should be preserved")
        for i in range(a.size):
          self.assertEqual(a.ravel()[i],b.ravel()[i],"Numerics should be preserved")
      else:
        self.assertEqual(a,b,"Numerics should be preserved")
        
if __name__ == '__main__':
    unittest.main()

