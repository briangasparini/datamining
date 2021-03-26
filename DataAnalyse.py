import json
import random

def GetTaille(Json_part, favo):
    tab = []
    tab.append(favo)
    try:
        tab.append(Json_part["exifProperty"]["ExifImageWidth"])
    except:
        print("[ERROR] il n'y a pas de largeur dans les exif de l'image n°" + str(Json_part["idImage"]))
        return -1
    try:
        tab.append(Json_part["exifProperty"]["ExifImageHeight"])
    except:
        print("[ERROR] il n'y a pas d'hauteur dans les exif de l'image n°" + str(Json_part["idImage"]))
        return -1
    return tab

def GetOrientation(Json_part, favo, height,Width):
    tab = []
    tab.append(favo)
    if height > Width:
        tab.append("PORTRAIT")
    elif height == Width:
        tab.append("CARRE")
    else:
        tab.append("PAYSAGE")
    return  tab
def GetTAG(Json_part, favo):
    tab = []
    tab.append(favo)
    try: #si l'API a bug il n'y a pas les champs "result" et "tags"
        image = Json_part["TAG"]["result"]["tags"]
        # des images ont 0 tag et dans ce cas pas possible de faire une boucle
        if len(image) > 0:
            for j in range(len(image)):
                tab.append(image[j]["tag"]["en"])
    except:
        print("[ERROR] l'API n'a pas retourné de tag pour l'image n°" + str(Json_part["idImage"]))
        return -1
    # a checker
    if len(tab) > 1:
        return tab
    else:
        return -1

def GetCouleur(Json_part, favo):
    tab = []
    tab.append(favo)
    for j in range(len(Json_part["Couleur"])):
            tab.append(Json_part["Couleur"][j]["color"])
    return tab


def getData(idUser,jsonDataPath):
    tableau_color = []
    tableau_TAG = []
    tableau_orientation = []
    tableau_taille = []
    allData = []
    imageLiked  = []
    with open(jsonDataPath, "r") as json_data:
        data_dict = json.load(json_data)
        for i in range(len(data_dict)):
            liked = random.randint(0,1)
            imageLiked.append({"idImage":data_dict[i]["idImage"],"imageLiked":liked})
            # on récupère les infos de couleur
            tableau_color.append(GetCouleur(data_dict[i], imageLiked[i]))
            # on récupère les infos de TAG
            temp = GetTAG(data_dict[i], imageLiked[i])
            if temp != -1:
                tableau_TAG.append(temp)
            # on récupère les infos de taille
            temp = GetTaille(data_dict[i], imageLiked[i])
            if temp != -1:
                tableau_taille.append(temp)
                # on récupère les infos d'orientation
                tableau_orientation.append(GetOrientation(data_dict[i], imageLiked[i],temp[2],temp[1]))
    allData.append({"idUser": idUser,"Liked":imageLiked})
    allData.append(tableau_color)
    allData.append(tableau_TAG)
    allData.append(tableau_orientation)
    allData.append(tableau_taille)
    return allData
    



