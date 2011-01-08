from numpy import *
from dymola.datamodel import *

d=AnnotatedDataModel()
d.add(AnnotatedData(5,Annotation("foo")))
d.add(AnnotatedData([5,12],Annotation("bar",unit="kg")))
d.add(AnnotatedData(array([[1,2,3],[4,5,6]]),Annotation("baz",unit="kg")))
d.add(AnnotatedData(array([[[1,2,3],[4,5,6]],[[1,0,0],[5,9,3]]]),Annotation("bak",unit="kg")))
d.add(AnnotatedData(linspace(0,3,10),Annotation("t")))
d.add(AnnotatedData(linspace(0,3,10)*2,Annotation("x",unit="m",dep="t")))

d.add(AnnotatedData(zeros((10,2)),Annotation("yz",unit="m",dep="t")))
print d

print d.exportDymModel()

#print d.exportDymModel()
