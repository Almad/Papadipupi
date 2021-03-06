import anyjson
import csv
import sys
import urllib2

import socket
socket.setdefaulttimeout(10)

from lxml.html.soupparser import fromstring
from lxml.cssselect import CSSSelector

STATIONS = {}

def get_station(link):
    link = "http://hydro.chmi.cz/isarrow/" + link

    try:
        tree = fromstring(urllib2.urlopen(link).read().decode('cp1250'))
        ident = CSSSelector("table tr:nth-child(1) td")(tree)[1].text

        STATIONS[tree.xpath("//table/tr[14]/td")[0].text] = {
        'database_id' : ident,
        'id' : tree.xpath("//table/tr[6]/td")[0].text,
        'x' : tree.xpath("//table/tr[14]/td")[0].text,
        'y' : tree.xpath("//table/tr[15]/td")[0].text,
        }
        if tree.xpath("//table/tr[3]/td"):
            STATIONS[tree.xpath("//table/tr[14]/td")[0].text]['name'] = tree.xpath("//table/tr[3]/td")[0].text,
    except Exception:
        print "Failed to retrieve station"


def scrape(start_year=2007, limit=2800):
#    complete_url = "http://hydro.chmi.cz/isarrow/objects.php?ukol_p=1&vod_typ=R&nadmh_sign=%3E&rickm_sign=%3E&rok_od=" + str(start_year) + "&rok_do=2012&objekty_chemdata=1&matrice=2000868184&typodb=41&seq=364924&ordrstr=NM&agenda=POV&limit_clsf=&matrice_clsf=&tscon_clsf=&rok_od_clsf=&rok_do_clsf=&val_sign_clsf=&val_clsf=&agg_clsf=&startpos=0&recnum=" + str(limit)
    complete_url = "http://hydro.chmi.cz/isarrow/objects.php?agenda=POV&objekty_chemdata=&objekty_biodata=&taxon_tree=&id_objekt=&nm_objekt=&tok=&kraj=&okres=&oblast_povodi=&hlgp=&vodutv=&objectsgrp=&rok_od=" + str(start_year) + "&rok_do=2012&objekty_chemdata=1&vod_typ=R&rickm_sign=%3E&rickm=&nadmh_sign=%3E&nadmh=&matrice=2000868184&typodb=41&tscongrp=&tscon=&data_mez_stanovitelnosti=&data_od=&data_do=&taxon=&send=Vyhledat+profily+povrchov%FDch+vod&startpos=0&recnum=" + str(limit)
    print "scraping from uri " + complete_url
    tree = fromstring(urllib2.urlopen(complete_url).read().decode('cp1250'))
    links = CSSSelector("table.tbl a")(tree)
    i = 1
    print str(len(links)) + " links found"
    for link in links:
        print "Retrieving station " + str(i)
        i += 1
        get_station(link.get("href"))

def store():
    f = open('stations.json', 'w')
    f.write(anyjson.serialize(STATIONS))
    f.close()


    f = open('stations.csv', 'wb')
    w = csv.writer(f)
    for k in STATIONS:
        row = STATIONS[k]
        try:
            w.writerow([row['id'].encode('utf-8'), row['x'].encode('utf-8'), row['y'].encode('utf-8'), row['name'][0].encode('utf-8')])
        except:
            print "Error while writing row" 
    
    f.close()

if __name__ == "__main__":
    args = []
    if len(sys.argv) > 1:
        args.append(sys.argv[1])
    if len(sys.argv) > 2:
        args.append(sys.argv[2])
    scrape(*args)
    store()
