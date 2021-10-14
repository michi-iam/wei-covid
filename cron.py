from .models import *


def cron_create_daily_rlp_ab_september():
    import requests
    from bs4 import BeautifulSoup
    import datetime
    url_rlp = "https://lua.rlp.de/de/presse/detail/news/News/detail/coronavirus-sars-cov-2-aktuelle-fallzahlen-fuer-rheinland-pfalz/"
    url = url_rlp
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    tables = soup.find_all("table")
    table = tables[2]
    rows = table.find_all("tr")
    #date
    d_array = rows[0].text[rows[0].text.find("Stand")+6:rows[0].text.find("Labor")].split(".")
    date = datetime.datetime.strptime(d_array[0]+"."+d_array[1]+"."+d_array[2], "%d.%m.%Y")
    if date.date() != RLPCovidDataModel.objects.last().date: #date.day
        rows = rows[3:]
        for row in rows:
            tds=row.find_all("td")
            landkreis = tds[0].text
            landkreis = CityModel.objects.get(name=landkreis)
            gesamt = tds[1].text
            differenz_vortag = tds[2].text
            hospitalisiert = tds[3].text
            verstorben = tds[4].text
            genesen = tds[5].text
            if "#" in genesen:
                genesen = genesen.replace("#","")
            aktuelle_faelle = tds[6].text
            inzidenz = tds[8].text
            if("," in inzidenz):
                inzidenz = inzidenz.replace(",",".")
            rlpCovidDataModel = RLPCovidDataModel.objects.create(
                landkreis=landkreis,
                date=date,
                gesamt=gesamt,
                differenz_vortag=differenz_vortag,
                hospitalisiert=hospitalisiert,
                verstorben=verstorben,
                genesen=genesen,
                aktuelle_faelle=aktuelle_faelle,
                inzidenz=inzidenz
            )
        print("RLP-Daten geupdated -sep")
        return True
    else:
        print("RLP-Daten NICHT geupdatet, weil auf dem akt. Stand -sep")
        return False