from dymola.datamodel import *

def saveParams(d,f):
  dm=AnnotatedDataModel()
  dm.addParams(d)
  dm.exportDymModel().saveText(f + ".dym")
  
def saveSeries(d,f):
  dm=AnnotatedDataModel()
  dm.addSeries(d)
  dm.exportDymModel().saveText(f + ".dym")
  
def loadParams(f):
  dm=AnnotatedDataModel(f+ ".dym")
  return dict([(d.annotation.name,d.data) for d in dm.data.itervalues()])
  
loadSeries = loadParams
