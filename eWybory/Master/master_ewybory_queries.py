#!/usr/bin/env python3
####################################################################################################
######################################### PRACA DYPLOMOWA ##########################################
####################################################################################################
############################################# eWybory ##############################################
######################### Developed by Patryk Wojdak & Bartosz Żółtowski ###########################
####################################################################################################
from cassandra.cluster import Cluster
import sqlite3
import os
os.environ["PYTHONIOENCODING"] = "utf-8"   

# funkcja, która zwraca informacje o wszystkch głosowaniach (z bazy SQL), których data rozpoczęcie jest mniejsza, od aktualnej daty, oraz data zakończenia, jest większa od aktualnej daty.
def get_Voting(current_day):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute('SELECT IdGlosowania, SumaOddanychGlosow, Nazwa FROM GLOSOWANIA WHERE (DataRozpoczecia<="'+ str(current_day) +'") AND (DataZakonczenia>="'+ str(current_day) +'")')
    data = query.fetchall()
    sessionSQL.close()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    return output   

# funkcja, która zwraca informacje o pierwszym wierszu z bazy SQL, z zapytania, które zostało podane jako argument funkcji
def sql_Select_One(query):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute(query)
    data = query.fetchone()
    sessionSQL.close()
    if(len(data)>0):
        return(data[0])
    else:
        return 0    
        
# funkcja, która zwraca informacje wszystkich wierszach z bazy SQL, z zapytania, które zostało podane jako argument funkcji
def sql_Select_Many(query):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute(query)
    data = query.fetchall()
    sessionSQL.close()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    return output    
        
# funkcja, która zwraca informacje o wszystkich wierszach dot. tabeli pytania z bazy SQL, z wartością IdGlosowania, które zostało podane jako argument funkcji
def get_Questions(IdGlosowania):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute('SELECT Pytania.IdPytania, Pytania.TrescPytania FROM Pytania WHERE Pytania.IdGlosowania='+str(IdGlosowania))
    data = query.fetchall()
    sessionSQL.close()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    return output    
    
# funkcja, która zwraca informacje o wszystkich wierszach dot. tabeli odpowiedzi z bazy SQL, z wartością IdGlosowania, które zostało podane jako argument funkcji
def get_Answers(IdGlosowania):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute('SELECT Odpowiedzi.IdOdpowiedzi, Odpowiedzi.TrescOdpowiedzi, Odpowiedzi.IdPytania FROM Odpowiedzi INNER JOIN Pytania ON Odpowiedzi.IdPytania=Pytania.IdPytania WHERE Pytania.IdGlosowania='+str(IdGlosowania))
    data = query.fetchall()
    sessionSQL.close()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    return output
    
# funkcja, która zwraca informacje o wszystkich wierszach dot. tabeli Kandydatury z bazy SQL, z wartością IdGlosowania, które zostało podane jako argument funkcji
def get_Candidacy(IdGlosowania):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    query = cursorSQL.execute('SELECT Kandydatury.IdKandydatury, Kandydatury.Opis FROM Kandydatury WHERE Kandydatury.IdGlosowania='+str(IdGlosowania))
    data = query.fetchall()
    sessionSQL.close()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    return output
    
# funkcja, która zwraca informacje o wszystkich wierszach dot. tabeli głosy z bazy NoSQL, z wartością IdGlosowania, które zostało podane jako argument funkcji
def get_Votes(IdGlosowania):
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute("SELECT IdGlosy, IdGlosowania, IdOdpowiedzi, Plec, Wiek, Wojewodztwa FROM Glosy WHERE IdGlosowania='"+str(IdGlosowania)+ "' ALLOW FILTERING")
    cluster.shutdown()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    return output  
    
# funkcja, która zwraca informacje o wszystkich wierszach dot. tabeli Statystyki z bazy NoSQL, z wartością IdGlosowania, które zostało podane jako argument funkcji
def get_Last_Stats(IdGlosowania):
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute("SELECT IloscGlosow FROM Statystyki WHERE IdGlosowania='"+str(IdGlosowania)+"' ALLOW FILTERING")
    output = []
    cluster.shutdown()
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    if(len(output) == 0):
        return -1
    return int(output[-1][0])
    
# funkcja, która zwraca informacje o pierwszym wierszu dot. tabeli Nodes z bazy NoSQL, które dotyczną urządzeń w bazie danych zwaierającymi status 'Online'
def get_First_Online_Node():
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    output = session.execute("SELECT idNodes, IP_Address, PORT FROM Nodes WHERE Status='Online' LIMIT 1 ALLOW FILTERING")
    # print("get_First_Online_Node: "+str(output.one()))
    cluster.shutdown()    
    return output.one()
    
# funkcja, która zwraca informacje o wszystkich wierszach dot. tabeli Nodes z bazy NoSQL, które dotyczną urządzeń w bazie danych zwaierającymi status 'Online'
def get_All_Online_Nodes():
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    data = session.execute("SELECT idNodes FROM Nodes WHERE Status='Online' ALLOW FILTERING")
    output = []
    cluster.shutdown()  
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)  
    return output

# funkcja, która zmienia status urządzenia w tabeli Nodes z bazy NoSQL, na status 'Busy'. Urządzenie o podanym ID w argumencie funkcji 
def update_Node(Node_ID):
    cluster = Cluster(["10.0.2.5"])#[settings.Cluster1_IP])
    session = cluster.connect()
    session.set_keyspace('e_wybory')
    output = session.execute("UPDATE Nodes SET Status='Busy' WHERE idNodes="+str(Node_ID))
    cluster.shutdown()
    return 0

# funkcja, która zmienia status głosowania w tabeli Glosowania z bazy SQL, na status o ID podanym jako drugi argument funkcji w głosowaniu o ID podanym, jako pierwszy argument funkcji. 
def set_Voting_Status(idGlosowania, idStatusWTrakcie):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    cursorSQL.execute('UPDATE Glosowania SET IdStatusy='+str(idStatusWTrakcie)+' WHERE IdGlosowania='+str(idGlosowania))
    sessionSQL.commit()
    sessionSQL.close()
    

# funkcja, która sprawdza czy dane głosowanie zostało zakończone i zmienia status głosowania w tabeli Glosowania z bazy SQL, na status o ID podanym jako drugi argument funkcji w głosowaniu o ID podanym, jako pierwszy argument funkcji. 
def close_Votings(current_date, idStatusZakonczone):
    sessionSQL = sqlite3.connect('/mnt/dc/eWybory.db')
    cursorSQL = sessionSQL.cursor()
    data = cursorSQL.execute('SELECT IdGlosowania FROM Glosowania WHERE DataZakonczenia <= date("'+ str(current_date) +'") AND IdStatusy !='+str(idStatusZakonczone))
    data = data.fetchall()
    output = []
    for row in data:
        dataRow = []
        for col in row:
            dataRow.append(col)
        output.append(dataRow)
    print("#\t Wykryta ilość głosowań, które należy zakończyć: ",str(len(output))," \t#") 
    if(len(output)<=0):
        sessionSQL.close()
        return
    for vote in output:
        print("#\t Traw zamykanie głosowania o ID: ",str(vote[0])," \t#") 
        cursorSQL.execute('UPDATE Glosowania SET IdStatusy='+str(idStatusZakonczone)+' WHERE IdGlosowania='+str(vote[0]))
    sessionSQL.commit()
    sessionSQL.close()
    return