from Labelling import *
from DataAnalyse import *
from DataCollection import *
from Constante import *


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
#initRepository(DATA_PATH)
#initRepository(IMAGE_TO_CHECK)
#initRepository(IMAGE_CHECKED)
""" Data Collection """
#jsonDataFile = []
#jsonDataFile = dataCollection()
#if len(jsonDataFile) != 0:
    #createJsonFile(dataCollection(),"Data")
#else:
#    return False
""" Labeling and Annotation """
#createJsonFile(addMainColorToJson(DATA_PATH+"Data.json"),"DataCouleur")
#createJsonFile(addMainColorToJson(DATA_PATH+"DataCouleur.json"),"DataCouleur")
""" Data Analyses """
# Tableau de Data (User Like / Color / TAG / Orientation / Taille)
allData = []
allData = getData(0,DATA_PATH+"DataTAG.json")
print("Tableau Données User")
print(allData[0])
print("Tableau Couleurs")
print(allData[1])
print("Tableau Tag")
print(allData[2])
print("Tableau Orientation")
print(allData[3])
print("Tableau Taille")
print(allData[4])
""" Data Visualization """



