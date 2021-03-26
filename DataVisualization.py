from pandas import json_normalize
import pandas as pd
import json
import matplotlib.pyplot as plot
from Constante import *
from PIL import Image

def getDataOrientation(tabOrientation):
    dicChiffreOrientation = {"PAYSAGE":0,"PORTRAIT":0,"CARRE":0}
    for i in range (len(tabOrientation)):
        if tabOrientation[i][1] == "PAYSAGE":
            dicChiffreOrientation["PAYSAGE"] = dicChiffreOrientation["PAYSAGE"] + 1
        elif tabOrientation[i][1] == "PORTRAIT":
            dicChiffreOrientation["PORTRAIT"] = dicChiffreOrientation["PORTRAIT"] + 1
        else:
            dicChiffreOrientation["CARRE"] = dicChiffreOrientation["CARRE"] + 1
    return(dicChiffreOrientation)

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