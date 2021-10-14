import requests
import os
import environ


from . models import *


env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Kopieren der RLP-Data-Models von Raspberry auf Desktop
# zuletzt: 25.09.2021

def copy_cities():
    url = env("URL_COVID_CITY")
    data = requests.get(url)
    data = data.json()
    for d in data:
        name = d["name"]
        population = d["population"]
        population_is_manual_updated = d["population_is_manual_updated"]
        cityModel = CityModel(
            name=name,
            population=population,
            population_is_manual_updated=population_is_manual_updated
        )
        cityModel.save()

def copy_rlp_data():
    url = env("URL_COVID_RLPDATA")
    data = requests.get(url)
    data = data.json()
    data.sort(key=lambda x: x["landkreis"])
    letzter_landkreis = ""
    lk = ""
 
    for d in data: 
        landkreis = d["landkreis"]
        if letzter_landkreis != landkreis:
            letzter_landkreis = landkreis
            landkreis = requests.get(landkreis)
            landkreis = landkreis.json()
            landkreis = CityModel.objects.get(name=str(landkreis["name"]))
            lk=landkreis
        date = d["date"]
        gesamt = d["gesamt"]
        differenz_vortag = d["differenz_vortag"]
        hospitalisiert = d["hospitalisiert"]
        verstorben = d["verstorben"]
        genesen = d["genesen"]
        aktuelle_faelle = d["aktuelle_faelle"]
        inzidenz = d["inzidenz"]
        rlpModel = RLPCovidDataModel.objects.create(
            landkreis=lk,
            date=date,
            gesamt=gesamt,
            differenz_vortag=differenz_vortag,
            hospitalisiert=hospitalisiert,
            verstorben=verstorben,
            genesen=genesen,
            aktuelle_faelle=aktuelle_faelle,
            inzidenz=inzidenz
        )
        rlpModel.save()

def check_double_dates():
    cities=CityModel.objects.all()
    rlpdatamodels=RLPCovidDataModel.objects.all()
    vorher = len(rlpdatamodels)

    Liste = []
    Doubles = []
    for m in rlpdatamodels:
        co = [m.landkreis, m.date]
        if co not in Liste:
            Liste.append(co)
        else:
            Doubles.append(m)
    for d in Doubles:
        RLPCovidDataModel.objects.get(pk=d.id).delete()
    return [vorher, RLPCovidDataModel.objects.all()]