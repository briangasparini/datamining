import requests
import urllib.request
import os
import shutil
from pandas import json_normalize
import pandas as pd
from PIL import ExifTags
from PIL import Image
import codecs
import json
from Constante import *

def saveImage(sourcePath,newPath):
    r = requests.get(sourcePath)
    if r.status_code == 200:
        with open(newPath, 'wb') as f:
            f.write(r.content)
            return True
    else:
        return False
def getExifData (imagePath):
    with open(imagePath, 'rb') as image_file:
        my_image = Image.open(image_file)
        exifProperty = {}
        for key, val in  my_image._getexif().items():
            if key in ExifTags.TAGS:
                if type(val) is bytes:
                    try:
                        temp = val.decode('utf-8')
                    except UnicodeDecodeError:
                        temp = ""
                    exifProperty[ExifTags.TAGS[key]] = temp
                elif type(val) is int or type(val) is str or type(val) is float:
                    exifProperty[ExifTags.TAGS[key]] = val
        return exifProperty
def initData(RequestURL):
    # Execute Request
    response = urllib.request.urlopen(RequestURL)
    jsonData =  json.loads(response.read().decode('utf-8'))
    return jsonData
def checkData(imagePath,imageExt,imageName,newImagePath):
    # check the extension
    if imageExt not in (".png"):
        # Download to check exif
        if saveImage(imagePath,newImagePath):
            with open(newImagePath, 'rb') as image_file:
                my_image = Image.open(image_file)
                return (not my_image._getexif() is  None)
        else:
            return False
    else: 
        return False

def getDataJsonFile(urlPath,newImagePath,imageName,imageExt,imageID):
    jsonData = {}
    jsonData["idImage"] = imageID
    jsonData["fileName"] = imageName
    jsonData["filePath"] = newImagePath
    jsonData["fileURL"] = urlPath
    jsonData["fileExtension"] = imageExt
    jsonData["exifProperty"] = getExifData(newImagePath) 
    return jsonData

def dataCollection(RequestURL,ImagePathDestination = IMAGE_CHECKED):
    jsonToCreate = False
    imageID = 0
    jsonDataFile = []
    # initData with WikiData
    jsonDataDirty = initData(RequestURL)
    for data in jsonDataDirty['results']['bindings']:
        imagePath = data['pic']['value']
        urlPath = imagePath
        urlImageName, imageExt = os.path.splitext(urlPath)
        imageName = urlImageName.split("/")[-1]
        newImagePath = IMAGE_TO_CHECK+imageName+imageExt
        # CheckData
        if checkData(urlPath,imageExt,imageName,newImagePath):
            os.remove(newImagePath)
            newImagePath = ImagePathDestination+imageName+imageExt
            # Download
            if saveImage(urlPath,newImagePath):
                jsonDataFile.append(getDataJsonFile(urlPath,newImagePath,imageName,imageExt,imageID))
                imageID = imageID +1
                jsonToCreate = True
                print("Data Valid")
            else:
                print("Data no valid")
        else:
            if os.path.isfile(newImagePath):
                os.remove(newImagePath)
            print("Data no valid")
    # Create Json
    if jsonToCreate:
        return jsonDataFile
    else:
        return []
        