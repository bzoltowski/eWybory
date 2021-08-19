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
import time 
import socket
import pickle
import hashlib
import requests
import worker_charts
import worker_statistics
from datetime import datetime
os.environ["PYTHONIOENCODING"] = "utf-8"
def get_Data(HOST, PORT):
    setSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    setSocket.bind((HOST, PORT))
    # Oczekiwanie na otrzymanie danych
    setSocket.listen(1)
    print("# Oczekuje na połączenie... ")
    conn, addr = setSocket.accept()
    print("# Nawiązano połączenie... ")
    output = b""
    while True:
        get_DataFromServer = conn.recv(65536)
        if not get_DataFromServer: break
        output += get_DataFromServer
    # Zamiana danych otrzymanych z głównego serwera do listy, przy użyciu pickle.loads
    dataFromServer = pickle.loads(output)
    print("# Otrzymano dane.")
    conn.close()
    for row in dataFromServer:
        print(row)
    setSocket.close()
    return dataFromServer

def main():
    print("#"*100)
    print("#"*45, " E_WYBORY ", "#"*45)
    print("#"*38, " Serwer o parametrach: ", "#"*38)
    # Przypisanie adresu IP v4 z karty sieciowej enp0s8 do zmiennej 
    HOST = ipv4 = os.popen('ip addr show enp0s8').read().split("inet ")[1].split("/")[0]
    print("#"*45, " ", HOST, " ", "#"*45)
    PORT = 13372
    print("#"*45, " ", PORT, " ", "#"*45)
    busy = False
    while True:
        if busy == False:
            dataFromServer = get_Data(HOST, PORT)
            busy = True
        if busy == True:
            print("# Trwa wstępna analiza danych...")
            flagIntegrity = True
            
            try:
                if( len(dataFromServer[0][0])!=6):
                    flagIntegrity = False
                    
                if( len(dataFromServer[4][0])!=1):
                    flagIntegrity = False
                    
                if( len(dataFromServer[5][0])!=1):
                    flagIntegrity = False
                    
                if( len(dataFromServer[6][0])!=1):
                    flagIntegrity = False
            except Exception as inst:
                msgToServer = requests.post(dataFromServer[4], json={"Error":"Błędne dane wejściowe", "IP_Address": str(HOST), "Data": str(hashlib.sha256(str(dataFromServer).encode('utf-8')).hexdigest())})
                
                print("# Proces został przerwany. Otrzymano błędne dane wejściowe.")
                print("# Informacjie o błędzie zostały przesłane na serwer.")
                print("# Następuje przejście w proces oczekiwania na połączenie.")
                busy = False
                continue
            if(flagIntegrity == False):
                msgToServer = requests.post(dataFromServer[4], json={"Error":"Błędne dane wejściowe", "IP_Address": str(HOST), "Data": dataFromServer})
                print("# Proces został przerwany. Otrzymano błędne dane wejściowe.")
                print("# Informacjie o błędzie zostały przesłane na serwer.")
                print("# Następuje przejście w proces oczekiwania na połączenie.")
                busy = False
                continue
                
            #Weryfikacja rodzaju otrzymanych danych
            if( dataFromServer[1] != None):
                questions = {}
                
                print("# Wstępna analiza danych została zakończona pomyślnie. ")
                print("str(dataFromServer[1]): ",str(dataFromServer[1]))
                statistic = {}
                # podział odpowiedzi na pytania
                for question in dataFromServer[1]:
                    tempVotes = []
                    for answer in dataFromServer[2]:
                        for vote in dataFromServer[0]:
                            if((int(question[0]) == int(answer[2])) and (int(answer[0])==int(vote[2]))):
                                tempVotes.append(vote)
                    print("# Trwa generwanie statystyk dla pytania "+ str(question[1]))
                    questions[question[0]] = worker_statistics.get_Statistic(tempVotes, dataFromServer[2])
                    if type(questions[question[0]])== int and questions[question[0]] == 1:
                        msgToServer = requests.post(dataFromServer[4], json={"Error":"get_Statistic return 1", "IP_Address": str(HOST), "Data": str(hashlib.sha256(str(dataFromServer).encode('utf-8')).hexdigest())})
                        print("# Proces został przerwany. Generowanie statystyk nie powiodło się.")
                        print("# Informacjie o błędzie zostały przesłane na serwer.")
                        print("# Następuje przejście w proces oczekiwania na połączenie.")
                        continue
                statistic = {}
                # Utworzenie wykresów
                for question, stats in questions.items():
                    if(type(stats) == int):
                        continue
                    print(str(dataFromServer[6]))
                    tresc_pytania = ""
                    for i in dataFromServer[1]:
                        if int(question) == i[0]:
                            tresc_pytania = i[1]
                    statistic[question] = worker_charts.get_All_Charts(tresc_pytania, stats, dataFromServer[6], dataFromServer[3], dataFromServer[4], HOST)
                print("# Statystyki zostały wygenerowane poprawnie.")
                print("# Rozpoczęto proces tworzenia wykresów...")
            else:
                statistic = {}
                percentData = worker_statistics.get_Statistic(dataFromServer[0], dataFromServer[2])
                statistic["KANDYDATURY_NODE"] = worker_charts.get_All_Charts("", percentData, dataFromServer[6], dataFromServer[3], dataFromServer[4], HOST)
            
            print("# Wykresy zostały wygenerowane poprawnie.")
            print("# Trwa przygotowanie danych do wysłania na główny serwer...")
            # Przygotowanie danych do wysłania na główny serwer
            output = {
            "Id_Nodes": str(dataFromServer[5][0]),
            "IP_Address":str(HOST),
            "IdGlosowania": str(dataFromServer[0][1][1]),
            "IloscGlosow": len(dataFromServer[0]),
            "Date": str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')),
            "Statystyki": statistic}
            print("# Dane zostały przygotowane pomyślnie.")
            msgToServer = requests.post(dataFromServer[4], json=json.dumps(output))
            print(msgToServer.text)
            print("# Informacjie zostały przesłane na serwer.")
            print("# Następuje przejście w proces oczekiwania na połączenie.")
            busy = False
            print("#"*100)
    
    
if __name__ == "__main__":
    main()