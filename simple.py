from dymola.datamodel import *

def saveParams(d,f):
  dm=AnnotatedDataModel()
  dm.add(d)
  dm.exportDymModel().saveText(f + ".dym")
  
  
def loadParams(f):
  dm=AnnotatedDataModel(f+ ".dym")
  return dict([(d.annotation.name,d.data) for d in dm.data.itervalues()])
