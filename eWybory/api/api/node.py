#!/usr/bin/env python3
####################################################################################################
######################################### PRACA DYPLOMOWA ##########################################
####################################################################################################
############################################# eWybory ##############################################
######################### Developed by Patryk Wojdak & Bartosz Żółtowski ###########################
####################################################################################################
import os
import sys
import json
import hashlib
from cassandra.cluster import Cluster
    
content_len = int(os.environ["CONTENT_LENGTH"])
print("Content-type: text/html\n\n")
#Przetworzenie otrzymanych danych z node'a do foramtu dict
req_body = sys.stdin.read(content_len)
req_dict = json.loads(req_body)
req_dict = json.loads(req_dict)
# Pomocnicze zmienne, które posłużą do późniejszej weryfikacji otrzymanych danych.
woj =''
data =''
plci = ''
wiek = ''
node = ''
odpowiedzi =''
ip_address = ''
iloscGlosow = ''
id_glosowania = ''
IPFlag = False
IDFlag = False
AgeFlag = False
NodeFlag = False
DateFlag = False
VotesFlag = False
GenderFlag = False
CountriesFlag = False
CountOfVotesFlag = False

# Funkcja, która wprowadza dane z drugiego argumentu do bazy danych NoSQL, przy odpowiednim formacie, podanym w pierwszym argumencie.
def noSQL_Query(format, quert):
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute(format, quert)
    cluster.shutdown()
    return 0
#Funkcja, która wprowadza dane z argumentu do bazy danych NoSQL
def noSQL_Query_Node(quert):
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute(quert)
    cluster.shutdown()
    return 0
#Wstępne sprawdzeni otrzymanych danych.
node = str(req_dict["Id_Nodes"])
if(len(node)>0):
    NodeFlag = True
ip_address = str(req_dict["IP_Address"])
if(len(ip_address)>0):
    IPFlag = True
id_glosowania = str(req_dict["IdGlosowania"])
if(len(id_glosowania)>0):
    IDFlag = True
iloscGlosow = str(req_dict["IloscGlosow"])
if(len(iloscGlosow)>0):
    CountOfVotesFlag = True
data = str(req_dict["Date"])
if(len(data)>0):
    DateFlag = True
# Weryfikacja danych pod względem rodzaju głosowania
if "KANDYDATURY_NODE" in req_dict["Statystyki"]:
    req_dict["Statystyki"]["KANDYDATURY_NODE"]= json.loads(req_dict["Statystyki"]["KANDYDATURY_NODE"])
    odpowiedzi = req_dict["Statystyki"]["KANDYDATURY_NODE"]["Odpowiedzi"]
    if(len(str(odpowiedzi))>0):
        VotesFlag = True
    plci = req_dict["Statystyki"]["KANDYDATURY_NODE"]["Plec"]
    if(len(str(plci))>0):
        GenderFlag = True
    wiek = req_dict["Statystyki"]["KANDYDATURY_NODE"]["Wiek"]
    if(len(str(wiek))>0):
        AgeFlag = True
    woj = req_dict["Statystyki"]["KANDYDATURY_NODE"]["Wojewodztwa"]
    if(len(str(woj))>0):
        CountriesFlag = True
    
    if(NodeFlag and IPFlag and IDFlag and CountOfVotesFlag and DateFlag and VotesFlag and GenderFlag and AgeFlag and CountriesFlag):
        # Gdy wszystkie dane zostały poprawnie podane, następuje przypisanie wartości do zmiennych, które zostaną wysłane do bazy danych NoSQL
        cqlStatsFormt = '''INSERT INTO statystyki (IdStatystyki, IdGlosowania, DataStatystyki, IloscGlosow, IdPytania, Odpowiedzi, Plec, Wiek, Wojewodztwa) VALUES(now(), %s,%s,%s,%s,%s,%s,%s,%s)'''
        cqlNodeFormt = "UPDATE Nodes SET Status='Online' WHERE idNodes="+str(node)+""
        stat_query = (str(id_glosowania), str(data), str(iloscGlosow), str(0), str(odpowiedzi), str(plci), str(wiek), str(woj))
        # Aktualizacja statystyk w bazie danych NoSQL
        noSQL_Query(cqlStatsFormt, stat_query)
        # Aktualizacja statusu urządzenia w bazie danych NoSQL
        noSQL_Query_Node(cqlNodeFormt)
else:
    for key, value in req_dict["Statystyki"].items():
        req_dict["Statystyki"][key] = json.loads(req_dict["Statystyki"][key])
        # Pomocnicze zmienne, które posłużą do późniejszej weryfikacji otrzymanych danych.
        woj =''
        plci = ''
        wiek = ''
        odpowiedzi =''
        AgeFlag = False
        VotesFlag = False
        GenderFlag = False
        CountriesFlag = False
        # Weryfikacja danych pod względem statystyk w każdym z pytań
        odpowiedzi = str(json.dumps(req_dict["Statystyki"][key]["Odpowiedzi"], ensure_ascii=False))
        if(len(str(odpowiedzi))>0):
            VotesFlag = True
        plci = str(json.dumps(req_dict["Statystyki"][key]["Plec"], ensure_ascii=False))
        if(len(str(plci))>0):
            GenderFlag = True
        wiek = str(json.dumps(req_dict["Statystyki"][key]["Wiek"], ensure_ascii=False))
        if(len(str(wiek))>0):
            AgeFlag = True
        woj = str(json.dumps(req_dict["Statystyki"][key]["Wojewodztwa"], ensure_ascii=False))
        if(len(str(woj))>0):
            CountriesFlag = True
        if(IPFlag and IDFlag and CountOfVotesFlag and DateFlag and VotesFlag and GenderFlag and AgeFlag and CountriesFlag):
            # Gdy wszystkie dane zostały poprawnie podane, następuje przypisanie wartości do zmiennych, które zostaną wysłane do bazy danych NoSQL
            cqlStatsFormt = '''INSERT INTO statystyki (IdStatystyki, IdGlosowania, DataStatystyki, IloscGlosow, IdPytania, Odpowiedzi, Plec, Wiek, Wojewodztwa) VALUES(now(), %s,%s,%s,%s,%s,%s,%s,%s)'''
            stat_query = (str(id_glosowania), str(data), str(iloscGlosow), str(key), str(odpowiedzi), str(plci), str(wiek), str(woj))
            # Aktualizacja statystyk w bazie danych NoSQL
            noSQL_Query(cqlStatsFormt, stat_query)
    # Aktualizacja statusu urządzenia w bazie danych NoSQL
    cqlNodeFormt = "UPDATE Nodes SET Status='Online' WHERE idNodes="+str(node)+""
    noSQL_Query_Node(cqlNodeFormt)
