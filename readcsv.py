import csv
import pandas as pd
import datetime
import os
import environ


from . models import *


env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


def get():
    path = env("PATH_TO_CSV")
    data = pd.read_csv(path)
    return data


def copy_from_csv():
    Liste=[]
    data = get()
    for d in data.values:
        lk_name=d[0]
        city = CityModel.objects.get(name=lk_name)
        date=d[3]
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        gesamt=d[4]
        differenz_vortag=d[5]
        hospitalisiert=d[6]
        verstorben=d[7]
        genesen=d[8]
        aktuelle_faelle=d[9]
        inzidenz=d[10]
        them = RLPCovidDataModel.objects.create(landkreis=city, date=date, gesamt=gesamt, differenz_vortag=differenz_vortag, hospitalisiert=hospitalisiert, verstorben=verstorben, aktuelle_faelle=aktuelle_faelle, genesen=genesen, inzidenz=inzidenz)

    return data









