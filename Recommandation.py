from DataAnalyse import GetOrientation,GetTAG,GetTaille,GetCouleur
from Constante import *
import json

def checkTaille(taille, pref):
    compt = 0
    if taille != -1:
        #          pref-250    < Longueur <   pref+250            
        if (taille[1]>pref[0] - 250 and taille[1]<pref[0] + 250) :
            compt = 15
        #         pref-250      < Largeur <    pref+250
        if (taille[2]>pref[1] - 250 and taille[2]<pref[1] + 250):
            compt = compt + 15
        if GetOrientation(False, taille[1], taille[2]) != GetOrientation(False, pref[0], pref[1]):
            compt = compt - 20
    return compt


def checkTAG(tags, pref):
    compt = 0
    for tag in tags[1:]:
        if tag in pref:
            compt = compt + 1
    return 15 * compt


def checkColor(colors, pref):
    compt = 0
    for color in colors[1:]:
        color = int(color.replace("#", "0x"), 16)
        # écart-relatif entre la théorie(pref) et la pratique(color)
        #Plus c'est petit mieux c'est
        compt = compt + (2/abs((pref-color)/color))
    return compt/(len(colors)-1)


def GetRecom(data_img, userPref):
    array = []
    for img in data_img:
        confidence = 0
        confidence += checkTaille (GetTaille(img, False) , userPref[3])
        confidence += checkTAG  (GetTAG(img, False), userPref[1])
        confidence += checkColor(GetCouleur(img, False), userPref[0])
        if confidence > 50 :
            array.append([img['idImage'], img['filePath']])
    return array


def GetUserPref(user):
    array = [user['FavoriteColor'], user['FavoriteTag'], user['Favoriteorientation'], user['FavoriteTaille']]
    return array


def JsonRecom(dataImgReco_path):
    jsonRecommandation = json.load(open(dataImgReco_path))
    jsondata = json.load(open(DATA_PATH+"User.json"))
    recommandation = []
    for data in jsondata:
        Pref = GetUserPref(data)
        recommandation.append({'idUser': data['idUser'] , 'Recomandation' : GetRecom(jsonRecommandation, Pref)})
    return recommandation
