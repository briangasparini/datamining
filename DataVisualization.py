from pandas import json_normalize
import pandas as pd
import json
import matplotlib.pyplot as plot
import math
from Constante import *
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import numpy


def getDataOrientation():
    dicChiffreOrientation = {"PAYSAGE":0,"PORTRAIT":0,"CARRE":0,"INCONNUE":0}
    with open(DATA_PATH+"Data.json", "r") as read_file:
        data = json.load(read_file)
        for datajson in data:
            try:
                height = datajson["exifProperty"]["ExifImageHeight"]
                width = datajson["exifProperty"]["ExifImageWidth"]
                if height < width :
                    dicChiffreOrientation["PAYSAGE"] = dicChiffreOrientation["PAYSAGE"] + 1
                elif height > width :
                    dicChiffreOrientation["PORTRAIT"] = dicChiffreOrientation["PORTRAIT"] + 1
                else:
                    dicChiffreOrientation["CARRE"] = dicChiffreOrientation["CARRE"] + 1
            except KeyError:
                dicChiffreOrientation["INCONNUE"] = dicChiffreOrientation["INCONNUE"] + 1
    return(dicChiffreOrientation)



def getPictureByYear():
    dicImageByYear = {}
    string = ""
    with open(DATA_PATH+"Data.json", "r") as read_file:
        data = json.load(read_file)
        for datajson in data:
            try:
                year = datajson["exifProperty"]["DateTimeOriginal"][0:4]
            except KeyError:
                year = 0
            string = str(year)
            if string in dicImageByYear:
                dicImageByYear[string] = 1 + dicImageByYear[string]
            else:
                dicImageByYear[string] = 1 
    return dicImageByYear

def getPictureByCamera():
    dicData = {}
    string = ""
    with open(DATA_PATH+"Data.json", "r") as read_file:
        data = json.load(read_file)
        for datajson in data:
            try:
                year = datajson["exifProperty"]["Make"]
            except KeyError:
                year = 0
            string = str(year)
            if string in dicData:
                dicData[string] = 1 + dicData[string]
            else:
                dicData[string] = 1 
    return dicData


def getHistogram(imageLocalPath):
    imgfile = Image.open(imageLocalPath)
    histogram = imgfile.histogram()
    red = histogram[0:255]
    green = histogram[256:511]
    blue = histogram[512:767]
    x= 255
    y = []
    for i in range(x):
        y.append((red[i],green[i],blue[i]))
    return y

def plotBar(dicData,titre):
    tabCle = []
    tabVal = []
    for cle, valeur in dicData.items():
        tabCle.append(cle)
        tabVal.append(valeur)
    plot.figure(figsize=(9,3))
    plot.suptitle(titre)
    plot.bar(tabCle,tabVal)

def plotAllHistogram():
    with open(DATA_PATH+"Data.json", "r") as read_file:
        y = []
        nindice = 0
        data = json.load(read_file)
        row = int((len(data)/5))+1
        figure, axes = plot.subplots(nrows=row, ncols=5, figsize=(50,50))
        for datajson in data:
            nindice += 1
            y =  getHistogram(datajson["filePath"])
            axes[0][0] = plot.subplot(row,5,nindice)
            plot.suptitle("Histogramme de toutes les images téléchargées")
            axes[0][0].set_prop_cycle('color', ['red', 'green', 'blue'])
            plot.plot(range(255),y)
        #nX += 1

def plotMainColor(imageLocalPath,nbGrappe):
    imgfile = Image.open(imageLocalPath)
    numarray = numpy.array(imgfile.getdata(), numpy.uint8)
    clusters = MiniBatchKMeans(n_clusters = nbGrappe)
    clusters.fit(numarray)
    npbins = numpy.arange(0, nbGrappe+1)
    histogram = numpy.histogram(clusters.labels_, bins=npbins)
    labels = numpy.unique(clusters.labels_)
    histogramsorted = sorted(histogram[0], reverse=True)
    figure, axes = plot.subplots(figsize=(10,5))
    nIndice = []
    size = histogramsorted
    label = histogramsorted
    for i in range(len(histogram[0])):
        for n in range(len(histogram[0])):
            if histogram[0][i] == histogramsorted[n]:
                nIndice.append(n)
    color = []
    for i in range(len(nIndice)):
        color.append('#%02x%02x%02x' % (math.ceil(clusters.cluster_centers_[nIndice[i]][0]),math.ceil(clusters.cluster_centers_[nIndice[i]][1]),math.ceil(clusters.cluster_centers_[nIndice[i]][2])))
        plot.suptitle("Couleur principale de "+imageLocalPath)
        axes.pie(size,None,label,color)