#!/usr/bin/env python3
####################################################################################################
######################################### PRACA DYPLOMOWA ##########################################
####################################################################################################
############################################# eWybory ##############################################
######################### Developed by Patryk Wojdak & Bartosz Żółtowski ###########################
####################################################################################################
import json
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
def get_Statistic(votes, input_answers):
    try:
        # Zamiana odpowiedzi na format dict z list, dla ułatwienia późniejszczego połączenia treści odpowiedzi i wynikami.
        answers = {str(i[0]):i[1] for i in input_answers}
        countOfVotes = len(votes)
        SortedOdpowiedzi = [row[2] for row in votes]
        SortedWoje = [row[5] for row in votes]
        Lata = [[int(row[4]), row[2]] for row in votes]
        # Przypisanie stałych wartości dla wieku
        Wiek = {"18-26":{"SumaOdpowiedzi":0}, "27-40":{"SumaOdpowiedzi":0}, "41-64":{"SumaOdpowiedzi":0}, "65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":countOfVotes}
        Woje = {}
        # Przypisanie stałych wartości dla każdego z województw
        for val in SortedWoje:
            Woje[val] = {"Odpowiedzi":{}, "Plec":{"SumaOdpowiedzi":0}, "Wiek":{"18-26":{"SumaOdpowiedzi":0}, "27-40":{"SumaOdpowiedzi":0}, "41-64":{"SumaOdpowiedzi":0}, "65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0}, "SumaOdpowiedzi":0}
            
        Plec = {} 
        for vote in votes:
            ################### ZLICZANIE GŁOSÓW WZGLĘDEM PŁCI
            if not vote[3] in Plec:
                # Przypisanie stałych wartości dla każdej z płci
                Plec[vote[3]] = {"Odpowiedzi":{},"18-26":{"SumaOdpowiedzi":0},"27-40":{"SumaOdpowiedzi":0},"41-64":{"SumaOdpowiedzi":0},"65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0}
            if vote[3] in Plec:
                Plec[vote[3]]["SumaOdpowiedzi"] += 1
                if not answers[vote[2]] in Plec[vote[3]]["Odpowiedzi"]:
                    Plec[vote[3]]["Odpowiedzi"][answers[vote[2]]] = 0
                if answers[vote[2]] in Plec[vote[3]]["Odpowiedzi"]:
                    Plec[vote[3]]["Odpowiedzi"][answers[vote[2]]] += 1
                        
                    ################### ZLICZANIE GŁOSÓW WZGLĘDEM PŁCI I WIEKU
                    if(int(vote[4])>= 18 and int(vote[4]) <=26):
                        Plec[vote[3]]["18-26"]["SumaOdpowiedzi"] +=1
                        if(answers[vote[2]] in Plec[vote[3]]["18-26"]):
                            Plec[vote[3]]["18-26"][answers[vote[2]]] += 1
                        else:
                            Plec[vote[3]]["18-26"][answers[vote[2]]] = 1
                    if(int(vote[4]) >= 27 and int(vote[4]) <= 40):
                        Plec[vote[3]]["27-40"]["SumaOdpowiedzi"] +=1
                        if(answers[vote[2]] in Plec[vote[3]]["27-40"]):
                            Plec[vote[3]]["27-40"][answers[vote[2]]] += 1
                        else:
                            Plec[vote[3]]["27-40"][answers[vote[2]]] = 1
                    if(int(vote[4]) >= 41 and int(vote[4]) <= 64):
                        Plec[vote[3]]["41-64"]["SumaOdpowiedzi"] +=1
                        if(answers[vote[2]] in Plec[vote[3]]["41-64"]):
                            Plec[vote[3]]["41-64"][answers[vote[2]]] += 1
                        else:
                            Plec[vote[3]]["41-64"][answers[vote[2]]] = 1
                    if(int(vote[4]) >= 65):
                        Plec[vote[3]]["65+"]["SumaOdpowiedzi"] +=1
                        if(answers[vote[2]] in Plec[vote[3]]["65+"]):
                            Plec[vote[3]]["65+"][answers[vote[2]]] += 1
                        else:
                            Plec[vote[3]]["65+"][answers[vote[2]]] = 1

            ################### ZLICZANIE GŁOSÓW WZGLĘDEM WIEKU
            if(int(vote[4])>= 18 and int(vote[4]) <=26):
                Wiek["18-26"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Wiek["18-26"]):
                    Wiek["18-26"][answers[vote[2]]]+=1
                else:
                    Wiek["18-26"][answers[vote[2]]] = 1
    
            if(int(vote[4]) >= 27 and int(vote[4]) <= 40):
                Wiek["27-40"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Wiek["27-40"]):
                    Wiek["27-40"][answers[vote[2]]]+=1
                else:
                    Wiek["27-40"][answers[vote[2]]] = 1
    
            if(int(vote[4]) >= 41 and int(vote[4]) <= 64):
                Wiek["41-64"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Wiek["41-64"]):
                    Wiek["41-64"][answers[vote[2]]]+=1
                else:
                    Wiek["41-64"][answers[vote[2]]] = 1
    
            if(int(vote[4]) >= 65):
                Wiek["65+"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Wiek["65+"]):
                    Wiek["65+"][answers[vote[2]]]+=1
                else:
                    Wiek["65+"][answers[vote[2]]] = 1
            
            ################### ZLICZANIE GŁOSÓW WZGLĘDEM WOJEWÓDZTW
            if(answers[vote[2]] in Woje[str(vote[5])]["Odpowiedzi"]):
                Woje[str(vote[5])]["Odpowiedzi"][answers[vote[2]]] += 1
            else:
                Woje[str(vote[5])]["Odpowiedzi"][answers[vote[2]]] = 1
                
            if( not vote[3] in Woje[str(vote[5])]["Plec"]):
                Woje[str(vote[5])]["Plec"][vote[3]] = {"Odpowiedzi":{},"18-26":{"SumaOdpowiedzi":0},"27-40":{"SumaOdpowiedzi":0},"41-64":{"SumaOdpowiedzi":0},"65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0} 
            
            ################### ZLICZANIE GŁOSÓW WZGLĘDEM PŁCI W WOJEWÓDZTWACH
            if(vote[3] in Woje[str(vote[5])]["Plec"]):
                Woje[str(vote[5])]["Plec"][vote[3]]["SumaOdpowiedzi"] +=1
                if not answers[vote[2]] in Woje[str(vote[5])]["Plec"][vote[3]]["Odpowiedzi"]:
                    Woje[str(vote[5])]["Plec"][vote[3]]["Odpowiedzi"][answers[vote[2]]] = 0
                if answers[vote[2]] in Woje[str(vote[5])]["Plec"][vote[3]]["Odpowiedzi"]:
                    Woje[str(vote[5])]["Plec"][vote[3]]["Odpowiedzi"][answers[vote[2]]] += 1
                    ################### ZLICZANIE GŁOSÓW WZGLĘDEM PŁCI I WIEKU W WOJEWÓDZTWACH
                    if(int(vote[4])>= 18 and int(vote[4]) <=26):
                        Woje[str(vote[5])]["Plec"][vote[3]]["18-26"]["SumaOdpowiedzi"]+=1
                        if(answers[vote[2]] in Woje[str(vote[5])]["Plec"][vote[3]]["18-26"]):
                            Woje[str(vote[5])]["Plec"][vote[3]]["18-26"][answers[vote[2]]] += 1
                        else:
                            Woje[str(vote[5])]["Plec"][vote[3]]["18-26"][answers[vote[2]]] = 1
                    if(int(vote[4]) >= 27 and int(vote[4]) <= 40):
                        Woje[str(vote[5])]["Plec"][vote[3]]["27-40"]["SumaOdpowiedzi"]+=1
                        if(answers[vote[2]] in Woje[str(vote[5])]["Plec"][vote[3]]["27-40"]):
                            Woje[str(vote[5])]["Plec"][vote[3]]["27-40"][answers[vote[2]]] += 1
                        else:
                            Woje[str(vote[5])]["Plec"][vote[3]]["27-40"][answers[vote[2]]] = 1
                    if(int(vote[4]) >= 41 and int(vote[4]) <= 64):
                        Woje[str(vote[5])]["Plec"][vote[3]]["41-64"]["SumaOdpowiedzi"]+=1
                        if(answers[vote[2]] in Woje[str(vote[5])]["Plec"][vote[3]]["41-64"]):
                            Woje[str(vote[5])]["Plec"][vote[3]]["41-64"][answers[vote[2]]] += 1
                        else:
                            Woje[str(vote[5])]["Plec"][vote[3]]["41-64"][answers[vote[2]]] = 1
                    if(int(vote[4]) >= 65):
                        Woje[str(vote[5])]["Plec"][vote[3]]["65+"]["SumaOdpowiedzi"]+=1
                        if(answers[vote[2]] in Woje[str(vote[5])]["Plec"][vote[3]]["65+"]):
                            Woje[str(vote[5])]["Plec"][vote[3]]["65+"][answers[vote[2]]] += 1
                        else:
                            Woje[str(vote[5])]["Plec"][vote[3]]["65+"][answers[vote[2]]] = 1
                    
            ################### ZLICZANIE GŁOSÓW WZGLĘDEM WIEKU W WOJEWÓDZTWACH
            Woje[str(vote[5])]["SumaOdpowiedzi"] +=1
            vote[4] = int(vote[4])
            Woje[str(vote[5])]["Wiek"]["SumaOdpowiedzi"] +=1
            if(vote[4]>= 18 and vote[4] <=26):
                Woje[str(vote[5])]["Wiek"]["18-26"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Woje[str(vote[5])]["Wiek"]["18-26"]):
                    Woje[str(vote[5])]["Wiek"]["18-26"][answers[vote[2]]]+=1
                else:
                    Woje[str(vote[5])]["Wiek"]["18-26"][answers[vote[2]]] = 1
            if(vote[4] >= 27 and vote[4] <= 40):
                Woje[str(vote[5])]["Wiek"]["27-40"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Woje[str(vote[5])]["Wiek"]["27-40"]):
                    Woje[str(vote[5])]["Wiek"]["27-40"][answers[vote[2]]]+=1
                else:
                    Woje[str(vote[5])]["Wiek"]["27-40"][answers[vote[2]]] = 1
            if(vote[4] >= 41 and vote[4] <= 64):
                Woje[str(vote[5])]["Wiek"]["41-64"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Woje[str(vote[5])]["Wiek"]["41-64"]):
                    Woje[str(vote[5])]["Wiek"]["41-64"][answers[vote[2]]]+=1
                else:
                    Woje[str(vote[5])]["Wiek"]["41-64"][answers[vote[2]]] = 1
            if(vote[4] >= 65):
                Woje[str(vote[5])]["Wiek"]["65+"]["SumaOdpowiedzi"]+=1
                if(answers[vote[2]] in Woje[str(vote[5])]["Wiek"]["65+"]):
                    Woje[str(vote[5])]["Wiek"]["65+"][answers[vote[2]]]+=1
                else:
                    Woje[str(vote[5])]["Wiek"]["65+"][answers[vote[2]]] = 1
        # Przypisanie treści wiadomości do liczby oddanych głosów, dla ogólnych statystyk
        Odpowiedzi = {answers[i]:SortedOdpowiedzi.count(i) for i in SortedOdpowiedzi}
        Odpowiedzi["SumaOdpowiedzi"] = countOfVotes
        Plec["SumaOdpowiedzi"] = countOfVotes
        # Zamiana liczby oddanych głosów na wartości liczbowe w podzialne na płci.
        #Plec[vote[3]] = {"Odpowiedzi":{},"18-26":{"SumaOdpowiedzi":0},"27-40":{"SumaOdpowiedzi":0},"41-64":{"SumaOdpowiedzi":0},"65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0}
        for plec, j in Plec.items():
            if plec != "SumaOdpowiedzi":
                for stats, val in j.items(): 
                    if stats != "SumaOdpowiedzi" and stats!="Odpowiedzi":
                        for id_p, iloscOdp in val.items():
                            if id_p != "SumaOdpowiedzi":
                                Plec[plec][stats][id_p] = round((iloscOdp*100)/Plec[plec][stats]["SumaOdpowiedzi"],2)
                    if stats=="Odpowiedzi":
                        for id_p, iloscOdp in val.items():
                                Plec[plec][stats][id_p] = round((iloscOdp*100)/Plec[plec]["SumaOdpowiedzi"],2)
        
        # Zamiana liczby oddanych głosów na wartości liczbowe w podzialne na ogólne odpowiedzi.
        for i,j in Odpowiedzi.items():
            if i != "SumaOdpowiedzi":
                Odpowiedzi[i] = round((j*100)/Odpowiedzi["SumaOdpowiedzi"],2)
        #Wiek = {"18-26":{"SumaOdpowiedzi":0}, "27-40":{"SumaOdpowiedzi":0}, "41-64":{"SumaOdpowiedzi":0}, "65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":countOfVotes}
        # Zamiana liczby oddanych głosów na wartości liczbowe w podzialne na wiek.
        for i,j in Wiek.items():
            if i != "SumaOdpowiedzi":
                for przedzial, iloscOdp in j.items():
                    if przedzial != "SumaOdpowiedzi":
                        Wiek[i][przedzial] = round((iloscOdp*100)/Wiek[i]["SumaOdpowiedzi"], 2)
        #Woje[val] = {"Odpowiedzi":{}, "Plec":{"SumaOdpowiedzi":0}, "Wiek":{"18-26":{"SumaOdpowiedzi":0}, "27-40":{"SumaOdpowiedzi":0}, "41-64":{"SumaOdpowiedzi":0}, "65+":{"SumaOdpowiedzi":0}}, "SumaOdpowiedzi":0}
        #Woje[str(vote[5])]["Plec"][vote[3]] = {"Odpowiedzi":{},"18-26":{"SumaOdpowiedzi":0},"27-40":{"SumaOdpowiedzi":0},"41-64":{"SumaOdpowiedzi":0},"65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0} 
        # Zamiana liczby oddanych głosów na wartości liczbowe w podzialne na województwa.
        for woje_key, woje_stats in Woje.items():        
            for woje_stat, woje_stat_value in woje_stats.items():
                if woje_stat != "SumaOdpowiedzi":
                    if(woje_stat=="Odpowiedzi"):
                        for id_odp, ilosc_odp in woje_stat_value.items():
                            Woje[woje_key][woje_stat][id_odp] = round((ilosc_odp*100)/Woje[woje_key]["SumaOdpowiedzi"], 2)
                    if(woje_stat=="Wiek"):
                        for id_wieku, woje_stat_id_wieku_value in woje_stat_value.items():
                            if(id_wieku!="SumaOdpowiedzi"):
                                for id_odp, iloscOdp in woje_stat_id_wieku_value.items():
                                    if(id_odp!="SumaOdpowiedzi"):
                                        Woje[woje_key][woje_stat][id_wieku][id_odp] = round((iloscOdp*100)/Woje[woje_key][woje_stat][id_wieku]["SumaOdpowiedzi"], 2)
                    if(woje_stat=="Plec"):
                        for id_plci, woje_stat_id_plci_stats in woje_stat_value.items():
                            if(id_plci !="SumaOdpowiedzi"):
                                for plci_stats, plci_stats_value in woje_stat_id_plci_stats.items():
                                    if(plci_stats =="Odpowiedzi"):
                                        for id_odp, iloscOdp in plci_stats_value.items():
                                            Woje[woje_key][woje_stat][id_plci][plci_stats][id_odp] = round((iloscOdp*100)/Woje[woje_key][woje_stat][id_plci]["SumaOdpowiedzi"], 2)
                                    if((plci_stats!="SumaOdpowiedzi") and (plci_stats!="Odpowiedzi")):
                                        for id_odp, iloscOdp in plci_stats_value.items():
                                            if(id_odp!="SumaOdpowiedzi"):
                                                Woje[woje_key][woje_stat][id_plci][plci_stats][id_odp] = round((iloscOdp*100)/Woje[woje_key][woje_stat][id_plci][plci_stats]["SumaOdpowiedzi"], 2)
        return json.dumps({"Odpowiedzi": Odpowiedzi, "Plec": Plec,"Wiek": Wiek, "Wojewodztwa": Woje}, ensure_ascii=False)#.encode('utf8')
    except Exception as inst:
        print("get_Statistic" + str(inst))   
        return 1
      