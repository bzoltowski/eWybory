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
import sqlite3
from cassandra.cluster import Cluster
from datetime import datetime, timedelta

# Funkcja, która zwraca pierwszy wiersz z zapytania bazy danych NoSQL, bądź 0 jeśli wynik zapytania jest błędny.
def noSql_Select_Data(input_query):
    cluster = Cluster(["10.0.2.5"])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute(input_query)
    output = []
    cluster.shutdown() 
    if(len(str(data))<=0):
        return 0
    for row in data:
        dataRow = {}
        for id, col in enumerate(row):
            dataRow[str(id)] = str(col)
        output.append( dataRow)
    return output[0]["0"]

# Funkcja, która zwraca zapytanie do bazy danych NoSQL w formacie JSON.
def noSql_Select_Query(input_query):
    cluster = Cluster(["10.0.2.5"])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute(input_query)
    output = []
    for row in data:
        dataRow = {}
        for id, col in enumerate(row):
            dataRow[str(id)] = str(col)
        output.append( dataRow)
    cluster.shutdown() 
    return json.dumps(output)
    
# Funkcja, która z odpowiednim formatem danych, wstawia wartości do podanej w formacie tabeli do bazy NoSQL.
def noSql_Insert_Query(format, input_query):
    cluster = Cluster(["10.0.2.5"])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute(format, input_query)
    cluster.shutdown()
    
# Funkcja, która zwraca date zakończenia głosowania, przy podaniu wartości IdGlosowania z tabeli Glosowania w bazie SQL.
def get_Close_Time(IdGlosowania):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute('SELECT DataZakonczenia FROM Glosowania WHERE Glosowania.IdGlosowania='+str(IdGlosowania))
    data = query.fetchone()
    sessionSQL.close()
    if(len(data)>0):
        return(data[0])
    else:
        return 0  

# Ustawienie nagłówka Content-type application/json, dla poinformowania przeglądarki użytkownika,
# który wysłał zapytanie do tego pliku, jakiego formatu danych może się spodziewać.
print("Content-type: application/json\n\n")
currentTime = datetime.now() - timedelta(seconds=5)
# Wczytanie otrzymanych danych i zamiana ich do formatu JSON.
content_len = int(os.environ["CONTENT_LENGTH"])
req_body = sys.stdin.read(content_len)
req_dict = json.loads(req_body)
# Pomocnicze zmienne, które posłużą do późniejszej weryfikacji otrzymanych danych.
get = ""
into = ""
where = ""
query = ""
values = ""
fromTable = ""
tableDesc = ""
sqlFlag = False
noSqlFlag = False
insertValFlag = False
selectGetFlag = False
selectFromFlag = False
insertIntoFlag = False
selectWhereFlag = False
insertTabDescFlag = False
# Weryfikacja otrzymanego formatu danych oraz przypisanie odpowiednich wartości do odpowiednich zmiennych.
for key, value in req_dict.items():
    key = str(key).upper()
    if(key == "QUERY"):
        query = str(value).upper()

    # Query SELECT Segment #
    if(key == "GET"):
        get = value
        selectGetFlag = True

    if(key == "FROM"):
        fromTable = value
        selectFromFlag = True

    if(key == "WHERE"):
        where = value
        selectWhereFlag = True

    # Query INSERT Segment #
    if(key == "INTO"):
        into = value
        insertIntoFlag = True

    if(key == "TABLEDESCRIPTION"):
        tableDesc = value
        insertTabDescFlag = True

    if(key == "VALUES"):
        values = value
        insertValFlag = True

#Sprawdzenie jaki format zapytania przysłał użytkownik, wysyłając zapytanie do tego pliku.
if( query == "SELECT"):
    if(selectFromFlag and (str(fromTable).upper()=="STATYSTYKI")):
        noSqlFlag = True

    if(noSqlFlag):
        if((selectGetFlag) and (selectFromFlag) and (selectWhereFlag)):
            # Przygotowanie zapytania, które zwraca datę ostatnich statystyk, dla wybranego głosowania.
            # Jest to ważne, ponieważ dzięki tej wartości można otrzymać statystyki dla wszystkich pytań w danym głosowaniu.
            dataDevice = "SELECT MAX(DataStatystyki) FROM STATYSTYKI WHERE " + where + " ALLOW FILTERING"
            maxDate = noSql_Select_Data(dataDevice)
            # Przygotowanie zapytania, które zwraca ostatnie statystyki dla wybranego głosowania i wyświetla wynik w formacie JSON.
            dataDevice = "SELECT " + get + " FROM STATYSTYKI WHERE DataStatystyki='"+str(maxDate)+"' AND " + where + " ALLOW FILTERING"
            print(noSql_Select_Query(dataDevice))
if( query == "INSERT"):
    currentTime=currentTime.strftime('%Y-%m-%d %H:%M:%S')
    if(insertIntoFlag and (str(into).upper()=="GLOSY")):
        noSqlFlag = True
    if(noSqlFlag):
        if((insertIntoFlag) and (insertTabDescFlag) and (insertValFlag)):
            # Sprawdzenie otrzymanych danych pod względem ich ilości.
            match = values.split(",")
            for i in range(len(match)):
                match[i] = match[i].replace(' ','')
            if (match[0] is not None) and (len(match)==5):
                # Sprawdzenie daty zakończenia głosowania
                closeTime = get_Close_Time(match[0])
                if(closeTime != 0):
                    if str(currentTime) < str(closeTime):
                        # Jeśli głos przyszedł przed zakończeniem głosowania, to zostaje on dodany do tabeli w bazie danych NoSQL,
                        # Natomiast, jeśli głos został oddany po zakończeniu, głos zostaje oddalony.
                        cqlVoteFormt = '''INSERT INTO glosy (IdGlosy, IdGlosowania, IdOdpowiedzi, Plec, Wiek, Wojewodztwa, DataOddaniaGlosu) VALUES(now(), %s,%s,%s,%s,%s,%s)'''
                        vote_query = (str(match[0]), str(match[1]), match[2], match[3], match[4], str(currentTime))
                        noSql_Insert_Query(cqlVoteFormt, vote_query)

