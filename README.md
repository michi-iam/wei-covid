# Wei-Covid

## Demo
http://covid-rlp.herokuapp.com/

## Flow
* ***copydb.py*** - copy data:
http://covid-rlp.herokuapp.com/api/...(Landkreise/RLPData)
* ***cron.py*** - read data with bs4 from https://lua.rlp.de/de/presse/detail/news/News/detail/coronavirus-sars-cov-2-aktuelle-fallzahlen-fuer-rheinland-pfalz/ 
* ***views.py/get_plot_for_multiple_qs*** - plot

## Dependencies 
* among others:
    * django-rest-framework
    * matplotlib
    * bs4
    * numpy
    * pandas
    * django-import-export
* all in ***requirements.txt***

## Why?
* I wanted to work with beautifulsoup, pandas, matplotlib and django-rest-framework - that's all...

## miscellaneous
* This very cool project: https://github.com/django-import-export/django-import-export allows you to import/export data as csv from the admin-interface