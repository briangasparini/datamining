import json
import random
import pandas as pd
import numpy as np



def GetOrientationPref(tab):
    temp = np.array(tab)
    dataset = pd.DataFrame({'Liked': temp[:, 0], 'Orientation': temp[:, 1]})
    dataset = dataset.astype(dtype= {"Liked" : "int64", "Orientation" : "<U200"})
    liked = dataset.groupby("Orientation").sum().sort_values(by='Liked', ascending = False)[0:1]
    return liked.index.tolist()


def GetTagPref(tab, nb):
    temp = np.array(tab)
    dataset = pd.DataFrame(temp)
    dataset.set_index(0, inplace = True)
    dataframe = pd.DataFrame(dataset[1]).rename(columns={1: 'TAG'})
    for i in range(2, len(tab[0]) - 1):
        dataframe = pd.concat([dataframe, pd.DataFrame(dataset[i]).rename(columns={i: 'TAG'})] )
    dataframe["Liked"] = dataframe.index
    dataframe["Liked"] = dataframe["Liked"].astype("int64")
    liked = dataframe.groupby("TAG").sum().sort_values(by='Liked', ascending = False)[0:nb]
    return liked.index.tolist()

def GetTaillePref(tab):
    temp = np.array(tab)
    dataset = pd.DataFrame({'Liked': temp[:, 0], 'Longueur': temp[:, 1], 'Largeur': temp[:, 2]})
    idf = dataset['Liked'] == 1
    dataset = dataset[idf]
    return [dataset["Longueur"].mean() , dataset["Largeur"].mean()]

def GetCouleurPref(tab):
    temp = np.array(tab)
    dataset = pd.DataFrame(temp)
    dataset.set_index(0, inplace = True)
    dataframe = pd.DataFrame(dataset[1]).rename(columns={1: 'Couleur'})
    for i in range(2, len(tab[0]) - 1):
        dataframe = pd.concat([dataframe, pd.DataFrame(dataset[i]).rename(columns={i: 'Couleur'})] )
    dataframe["Liked"] = dataframe.index
    dataframe['Couleur'] = dataframe['Couleur'].str.replace('#','0x')
    dataframe["Liked"] = dataframe["Liked"].astype("int64")
    dataframe["Couleur"] = dataframe["Couleur"].apply(int, base=16)
    return dataframe["Couleur"].mean()

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
            tableau_color.append(GetCouleur(data_dict[i], liked))
            # on récupère les infos de TAG
            temp = GetTAG(data_dict[i], liked)
            if temp != -1:
                tableau_TAG.append(temp)
            # on récupère les infos de taille
            temp = GetTaille(data_dict[i], liked)
            if temp != -1:
                tableau_taille.append(temp)
                # on récupère les infos d'orientation
                tableau_orientation.append(GetOrientation(data_dict[i],liked,temp[2],temp[1]))
    allData.append({"idUser": idUser,"Liked":imageLiked,"FavoriteColor":GetCouleurPref(tableau_color),"FavoriteTag":GetTagPref(tableau_TAG,3),"Favoriteorientation":GetOrientationPref(tableau_orientation),"FavoriteTaille":GetTaillePref(tableau_taille)})
    allData.append(tableau_color)
    allData.append(tableau_TAG)
    allData.append(tableau_orientation)
    allData.append(tableau_taille)
    return allData



