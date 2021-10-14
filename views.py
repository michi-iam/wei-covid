import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from io import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib as plt

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


from . models import CityModel, RLPCovidDataModel, LastUpdateTry
import logging
logger = logging.getLogger('herokulogger')

TEMPLATES = {
    "index": "covid/startseite.html",
    "impressum": "impressum/impressum.html",
    "datenschutz": "impressum/datenschutz.html",
    "plot": "covid/plots.html",
    }
CovidKeys = {
    "gesamt": "Gesamt",
    "differenz_vortag": "Differenz zum Vortag",
    "hospitalisiert": "Hospitalisiert",
    "verstorben": "Verstorben",
    "genesen": "Genesen",
    "aktuelle_faelle": "Aktuelle Fälle",
    "inzidenz": "Inzidenz",
    }


def update_on_visit():
    from covid import cron
    if can_update():
        try:
            data_updated = cron.cron_create_daily_rlp_ab_september()
            lastUpdateTry = LastUpdateTry.objects.last()
            lastUpdateTry.data_updated = data_updated
            lastUpdateTry.save()
            logger.info('RLP Daten geupdated = ' + str(data_updated))
        except:
            LastUpdateTry.objects.last().save()
            logger.warning("Trouble! RLP-Daten konnten nicht geupdated werden. Check die Webseite")


def can_update():
    if LastUpdateTry.objects.all():
        lastUpdateTry = LastUpdateTry.objects.last()
        lu = lastUpdateTry.updated_at.replace(tzinfo=None)
        indrei = lu + timedelta(hours=3)
        now = datetime.now()
        td = datetime.today()
        if now < indrei:
            return False
        if lastUpdateTry.created_at.date() == td.date() and lastUpdateTry.data_updated == True:
            lastUpdateTry.save()
            return False
        if td.weekday() == 6:
            return False
        else:
            return True
    else:
        LastUpdateTry.objects.create(data_updated=False)
        return True

def cookie_settings(request):
    cookieStatus = request.POST.get("cookieStatus")
    if cookieStatus == "all":
        return JsonResponse({"cookieStatus": "all"})

def impressum(request):
    return render(request, TEMPLATES["impressum"])

def datenschutz(request):
    return render(request, TEMPLATES["datenschutz"])


def get_base_context():
    landkreise = CityModel.objects.all().order_by("name")
    try:
        lastDay = RLPCovidDataModel.objects.filter(date=RLPCovidDataModel.objects.order_by("date").last().date).order_by("landkreis__name")
    except:
        lastDay = ["keine Daten vorhanden"]
    context={
        "Landkreise":landkreise,
        "CovidData":lastDay,
        "can_update": can_update(),
        }
    return context

def index(request):
    logger.info('Seite besucht')
    context = get_base_context()
    update_on_visit()
    return render(request, TEMPLATES["index"], context)


def get_data_by_landkreis(request):
    ListeData = []
    ListeNamen = []

    lk1Id = request.GET.get("lk1Id")
    if lk1Id != "":
        lk1 = CityModel.objects.get(pk=lk1Id)
        lk1data = RLPCovidDataModel.objects.filter(landkreis=lk1).order_by("date")
        ListeData.append(lk1data)
        ListeNamen.append(lk1.name)

    lk2Id = request.GET.get("lk2Id")
    if lk2Id != "":
        lk2 = CityModel.objects.get(pk=lk2Id)
        lk2data = RLPCovidDataModel.objects.filter(landkreis=lk2).order_by("date")
        ListeData.append(lk2data)
        ListeNamen.append(lk2.name)

    lk3Id = request.GET.get("lk3Id")
    if lk3Id != "":
        lk3 = CityModel.objects.get(pk=lk3Id)
        lk3data = RLPCovidDataModel.objects.filter(landkreis=lk3).order_by("date")
        ListeData.append(lk3data)
        ListeNamen.append(lk3.name)

    key = request.GET.get("key")
    titel = ""
    if key in CovidKeys:
        titel = CovidKeys[key]


    data = get_plot_for_multiple_qs(ListeData,ListeNamen, key, titel, True, False, None, 3)

    response = render(request, TEMPLATES["plot"], { "LKData":data})
    return HttpResponse(response)



def get_plot_for_multiple_qs(
        liste_daten_als_queryset,
        liste_labels,
        value_to_display,
        fig_title,
        starts_with_0,
        b_subplot_rlp,
        dateformat,
        legend_position
        ):
        if fig_title == None:
            fig_title = value_to_display
        if dateformat == None:
            dateformat = '%d.%m'
        if legend_position == None:
            legend_position = 3
        if value_to_display == "verstorben":
            starts_with_0 = False

        fig=Figure()
        ax = fig.add_subplot(111,facecolor="none")

        x = 0
        for queryset in liste_daten_als_queryset:
            date = []
            inz=[]
            for d in queryset:
                date.append(d.date)
                inz.append(getattr(d, value_to_display))
            ax.plot(date, inz, '-', label=liste_labels[x])
            x+=1
        if starts_with_0 == True:
            ax.set_ylim(ymin=0)
        ax.legend(loc=legend_position)

        ax.set_xlabel('Date')
        ax.set_ylabel(value_to_display)
        ax.set_title(fig_title)

        myFmt = mdates.DateFormatter(dateformat)
        ax.xaxis.set_major_formatter(myFmt)

        if b_subplot_rlp == True:
            ax2 = fig.add_subplot(222,facecolor="none")
            landkreis_Rheinland_Pfalz = covid_models.CityModel.objects.get(name="Rheinland-Pfalz")
            data_rheinland_pfalz = covid_models.RLPCovidDataModel.objects.filter(landkreis=landkreis_Rheinland_Pfalz).order_by("date")
            date=[]
            inz=[]
            for d in data_rheinland_pfalz:
                date.append(d.date)
                inz.append(getattr(d, value_to_display))
            ax2.plot(date, inz, 'm-', label=d.landkreis)
            ax2.xaxis.set_major_formatter(myFmt)
            if starts_with_0 == True:
                ax2.set_ylim(ymin=0)
            ax2.legend(loc=3)
        
        imgdata = StringIO()
       
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        
        data = imgdata.getvalue()
        return data





