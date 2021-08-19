#!/usr/bin/env python3
####################################################################################################
######################################### PRACA DYPLOMOWA ##########################################
####################################################################################################
############################################# eWybory ##############################################
######################### Developed by Patryk Wojdak & Bartosz Żółtowski ###########################
####################################################################################################
import os
import sys
import socket
import pickle
from time import sleep
from datetime import datetime
os.environ["PYTHONIOENCODING"] = "utf-8"   

inProgeress ={}
while True:
    from master_ewybory_queries import *
    print("#"*100)
    print("#"*44, " E_WYBORY ", "#"*44)
    print("#"*23, " PROGRAM DO ZARZĄDZANIA GŁOSOWANIAMI I URZĄDZENIAMI ", "#"*23)
    print("#"*29, " ODPOWIEDZIALNYMI ZA TWORZENIE STATYSTYK ", "#"*28)
    print("#"*100)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("#"*30, " WYZNACZONY CZAS:"+str(current_date)+" ","#"*31)
    print("#"*100)
    idGlosowaniaKandydatury = [3, 4, 9]  
    idStatusWTrakcie = sql_Select_One("SELECT IdStatusy FROM Statusy WHERE Nazwa='wTrakcie'")
    idStatusZakonczone = sql_Select_One("SELECT IdStatusy FROM Statusy WHERE Nazwa='zakonczone'")
    if(idStatusZakonczone == 0):
        continue
    else:
        print("#\t Następuje przegląd listy głosowań, które zostały zakończone...") 
        close_Votings(current_date, idStatusZakonczone)
        print("#\t Pomyślnie zaktualizowano listę zakończonych głosowań")
    print("#\t Następuje przegląd listy urządzeń, które zostały wyznaczone do obliczeń głosowań...") 
    if(len(inProgeress) > 0):
        print("#\t Wykryto ", str(len(inProgeress)), " głosowań, które są w trakcie obliczania...")
        for idNode in get_All_Online_Nodes():
            for idGlosowanieInProgress, idNodeInProgress in inProgeress.items():
                if(int(idNode[0]) == int(idNodeInProgress)):
                    print("##\t Urządzenie służące do obliczeń o ID: "+str(idNode[0])+" zakończyło głosowanie głosowania o ID:"+str(idGlosowanieInProgress)+"\t##")
                    del inProgeress[idGlosowanieInProgress]
                    break
    print("#\t Pomyślnie zaktualizowano listę dostępnych urządzeń, odpowiedzialnych za obliczanie głosowań")
    for row in get_Voting(current_date):
        IdGlosowania = row[0]
        print("#\t Trwa aktualizowanie statusu głosowania o ID: ", IdGlosowania, "\t#")
        set_Voting_Status(row[0], idStatusWTrakcie)
        print("#\t Pomyślnie zaktualizowano status głosowania o ID: ", IdGlosowania, "\t#")
        print("#\t Otrzymano informacje o głosowaniu z ID: ", IdGlosowania, "\t###")
        print("#\t Następuje analiza otrzymanych danych...") 
        if(type(row[1]) == None or row[1] is None):
            print("###\t Wartość 'Suma Oddanych Glosow' posiada nieznaną wartością 'NoneType'\t###")
            print("###\t Obliczenia statystyk dla tego głosowania zostają przerwane.\t###")
            continue
        if(len(str(row[1]))<=0):
            print("###\t Wartość 'Suma Oddanych Glosow' jest mniejsza od 0\t###")
            print("###\t Obliczenia statystyk dla tego głosowania zostają przerwane.\t###")
            continue
        iloscGlosow = int(row[1])
        inProgeressFlag = False
        for idGlosowanieInProgress, idNodeInProgress in inProgeress.items():
            if (idGlosowanieInProgress == IdGlosowania):
                sleep(10)
                inProgeressFlag = True
                continue
        if(inProgeressFlag):
            print("##\t Glosowanie o ID: ", IdGlosowania, " jest aktualnie obliczane.")
            print("###\t Następuje przejście do kolejnego głosowania.\t###")
            continue
        countOfVotes = get_Last_Stats(IdGlosowania)
        if(iloscGlosow <= countOfVotes):
            print("##\t Glosowanie o ID: ", IdGlosowania, " posiada najświeższe statystyki.")
            print("###\t Następuje przejście do kolejnego głosowania.\t###")
            continue
        getNode = get_First_Online_Node()
        NoneType = type(None)
        if (isinstance(getNode, NoneType)):
            print("###\t Nie otrzymano właściwych informacji o urządzeniu odpowiedzialnym za obliczanie statystyk.\t###")
            print("###\t Następuje przejście do kolejnego głosowania.\t###")
            continue
        getData = get_Votes(IdGlosowania)
        if(len(getData)<=0):
            print("###\t Nie otrzymano właściwych informacji o oddanych głosach.\t###")
            print("###\t Następuje przejście do kolejnego głosowania.\t###")
            continue
        
        print("##\t Następuje sprawdzenie typu głosowania.\t##")
        if(int(row[0]) in idGlosowaniaKandydatury):
            print("##\t Zidentyfikowano głosowanie bez pytań.\t##")
            print("##\t Trwa zbieranie informacji o kandydatach...\t##")
            get_Answers = get_Candidacy(IdGlosowania)
            get_Questions = None
        else:
            print("##\t Zidentyfikowano głosowanie z pytaniami.\t##")
            print("##\t Trwa zbieranie informacji o odpowiedziach...\t##")
            get_Answers = get_Answers(IdGlosowania)
            print("##\t Trwa zbieranie informacji o pytaniach...\t##")
            get_Questions = get_Questions(IdGlosowania)
        print("##\t Zebrano wszystkie wymagane informacje.\t##")
        data = [getData, get_Questions, get_Answers, "http://10.0.2.5/api/node_transfer.php", "http://10.0.2.5/api/node.py", str(getNode[0]), row[2]]
        print("##\t Następuje próba wysłania informacji do wybranego urządzenia o adresie IP:"+str(getNode[1])+"\t##")
        try:
            socketToNode = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize socket to NODE
            socketToNode.connect((getNode[1], int(getNode[2]))) #Set connection to NODE
            socketToNode.send(pickle.dumps(data)) #Prepare object and send to NODE
            socketToNode.close() #close connection
            print("##\t Wysłano wszystkie niezbędne informacje do wybranego urządzenia.\t##")
            update_Node(getNode[0])
            inProgeress[IdGlosowania] = getNode[0]
            print("##\t Zaktualizowano informacje o urządzeniu.\t##")
        except Exception as inst:
            print("###\t Nie udało się wysłać zebranych informacji.\t###")
            print("###\t Następuje przejście do kolejnego głosowania.\t###")
            continue
    
    print("--> Następuje 10-cio sekundowe opóźnienie, dla zaobserwowania wyników. <--")
    sleep(10)