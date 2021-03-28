#%%
from Labelling import *
from DataAnalyse import *
from DataCollection import *
from Constante import *
from Recommandation import JsonRecom
from DataVisualization import *
from PIL import Image
import threading
import time


class MonThread (threading.Thread):
    jsonPath = ""
    jsonName = ""
    def __init__(self, pathJson,newJsonName):
        threading.Thread.__init__(self)
        self.jsonPath = pathJson
        self.jsonName = newJsonName
        self.etat = False       # l'état du thread est soit False (à l'arrêt)
        # soit True (en marche)

    def run(self):
        self.etat = True                        # on passe en mode marche
        createJsonFile(addMainColorToJson(self.jsonPath),self.jsonName)
        self.etat = False    




def initRepository(repositoryPath):
    if repositoryPath[-1] == "/":
        repositoryPath = repositoryPath[0:len(repositoryPath)-1]
    # Clean repository IMAGES
    if os.path.exists(repositoryPath):
        shutil.rmtree(repositoryPath)
        os.makedirs(repositoryPath)
    else:
        os.makedirs(repositoryPath)
def createJsonFile(jsonData,FileName):
    fichier = open(DATA_PATH+FileName+".json", "w")
    json.dump(jsonData,fichier)
    fichier.close()


""" Clean Repository """  
"""       
initRepository(DATA_PATH)
initRepository(IMAGE_TO_CHECK)
initRepository(IMAGE_CHECKED)
initRepository(IMAGE_CHECKED_RECOM)
"""
""" Data Collection """
"""
jsonDataFile = []
jsonDataFile = dataCollection(URL_DATA)
if len(jsonDataFile) != 0:
    createJsonFile(jsonDataFile,"Data")
"""
""" Labeling and Annotation """
"""
m = MonThread(DATA_PATH+"Data.json","DataCouleur")
m.start()
time.sleep(1)
while m.etat == True:
    # on attend que le thread démarre
    time.sleep(0.1)
#createJsonFile(addMainColorToJson(DATA_PATH+"Data.json"),"DataCouleur")
createJsonFile(addMainTagToJson(DATA_PATH+"DataCouleur.json"),"DataTAG")
"""
""" Data Analyses """

# Tableau de Data (User Like / Color / TAG / Orientation / Taille)
"""
allData = getData(5,DATA_PATH+"DataTAG.json")
createJsonFile(allData[0],"User")
"""
""" Data Visualization """ 
"""
dicData = getDataOrientation()
plotBar(dicData,'Nombre d\' images par orientation')
dicData = getPictureByYear()
plotBar(dicData,'Nombre d\' images par années')
dicData = getPictureByCamera()
plotBar(dicData,'Nombre d\' images par appareil')
plotAllHistogram()
plot.show()
boucle =  True
while boucle:
    print("Indiquer le nom de l'image dont vous voulez connaitre les couleurs principales")
    sNomImage = str(input("Nom de l'image:"))
    sNomImage = IMAGE_CHECKED+sNomImage
    nbGrappe = int(input("Combien de couleurs principales(max 5):"))
    if nbGrappe > 5 : nbGrappe = 5
    plotMainColor(sNomImage,nbGrappe)
    plot.show()
    boucle = bool(input("Continuer ? (1: Oui / 0:Non)"))
"""
""" Recomendation """
""" Creation of DataSet for the recomandation """
""" Data Collection """
"""
jsonDataFile = []
jsonDataFile = dataCollection(URL_DATA_RECOM,IMAGE_CHECKED_RECOM)
if len(jsonDataFile) != 0:
    createJsonFile(jsonDataFile,"DataRecom")
"""
""" Labeling and Annotation """
"""
m2 = MonThread(DATA_PATH+"DataRecom.json","DataCouleurRecom")
m2.start()
time.sleep(1)
while m2.etat == True:
    # on attend que le thread démarre
    time.sleep(0.1)

#createJsonFile(addMainColorToJson(DATA_PATH+"DataRecom.json"),"DataCouleurRecom")
os.remove(DATA_PATH+"DataRecom.json")
createJsonFile(addMainTagToJson(DATA_PATH+"DataCouleurRecom.json"),"DataImageRecom")
os.remove(DATA_PATH+"DataCouleurRecom.json")
"""
"""
recom = JsonRecom(DATA_PATH+"DataImageRecom.json")
createJsonFile(recom,"RecommandationByUser")
"""










# %%
