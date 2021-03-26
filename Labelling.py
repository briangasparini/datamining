from sklearn.cluster import MiniBatchKMeans
import math
import matplotlib.pyplot as plot
import numpy
from PIL import Image
import json
import requests

API_KEY = 'acc_41a418a90eb4f18'
API_SECRET = '61a357112a731f5df0ccad405433c57f'

def getColor(nb, path):
    # on ouvre l'image
    imgfile = Image.open(path)
    # on transforme l'image comme un tableau de données
    numarray = numpy.array(imgfile.getdata(), numpy.uint8)
    # on trouve les couleurs prédominantes par l'algorithme de regroupement KMeans
    # fit permet de calculer le cluster kmeans pour nb points
    clusters = MiniBatchKMeans(n_clusters = nb).fit(numarray)
    #initialise un tableau de [0 à nb]
    npbins = numpy.arange(0, nb+1)
    #cluster.labels_ renvoie un tableau du cluster de type : array([1, 1, 1, 0, 0, 0], dtype=int32)
    # calcul l'historgramme d'un set de data pour npbins point
    histogram = numpy.histogram(clusters.labels_, bins=npbins)
    # Trouve les éléments uniques du tableaux
    labels = numpy.unique(clusters.labels_)
    # passage par un tableau (répétition dans le code)
    labelTab = [labels, sorted(histogram[0], reverse=True)]
    # comme on modifie l'ordre d'histogramme on va enregistrer l'ordre des indices dans un autre tableau
    # Il sert lorsque l'on récupère les propriétées du cluster non trié
    indice = numpy.argsort(histogram[0])[::-1]
    tab = []
    for i in range(nb):
        temp = {}
        temp["cluster"] = i
        temp["quantity"] = int(labelTab[1][i])
        temp["color"] = ('#%02x%02x%02x' % (
           math.ceil(clusters.cluster_centers_[indice[i]][0]), 
           math.ceil(clusters.cluster_centers_[indice[i]][1]),
           math.ceil(clusters.cluster_centers_[indice[i]][2])))
        tab.append(temp)
    return tab

def getTag(image_url,confidence,limit):
    response = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % (image_url), auth=(API_KEY, API_SECRET),params={"threshold":confidence,"limit":limit})
    return response.json()
def addMainColorToJson(dataJsonPath):
    with open(dataJsonPath, "r") as read_file:
        data = json.load(read_file)
        for datajson in data:
            datajson["Couleur"] = (getColor(4,datajson["filePath"]))
    return data
def addMainTagToJson(dataJsonPath):
    with open(dataJsonPath, "r") as read_file:
        data = json.load(read_file)
        for datajson in data:
            datajson["TAG"] = (getTag(datajson["fileURL"],10.0,3))
    return data