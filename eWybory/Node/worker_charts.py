####################################################################################################
######################################### PRACA DYPLOMOWA ##########################################
####################################################################################################
############################################# eWybory ##############################################
######################### Developed by Patryk Wojdak & Bartosz Żółtowski ###########################
####################################################################################################
import os
import re
import json
import hashlib
import requests
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
os.environ["PYTHONIOENCODING"] = "utf-8"
def get_Statistic_SVG_Pie(odpowiedzi, wartosci, pytanie, nazwa, iloscOdp, HOST, url):
    #Jeśli żadna odpowiedz nie została oddana, to następuje pominięcie utworzenia wykresu.
    if (len(odpowiedzi) <= 0):
        return "FILE_NOT_FOUND"
    fig, ax = plt.subplots()
    #Wyznaczenie wartości hash, która służy jako nazwa pliku
    hash = "PIE "+str(nazwa) + str(odpowiedzi) + str(pytanie) + str(datetime.now())
    odp = []
    # Dodanie wartości procentowych do treści odpowiedzi, dla lepszego zobrazowania wyników
    for key, value in enumerate(odpowiedzi):
        odp.append(value + " [" + str(wartosci[key]) + "%]")
    
    # Podział wartości liczbowych, na "kawałki", w celu utrzworzenia odpowiednich proporcji na wykresie.
    wedges, texts = ax.pie(wartosci, wedgeprops=dict(width=0.5), startangle=-40)
    # Ustawnienie słów kluczowych i wartości dla nich w funkcji annotate, odpowiedzialnej za przypisanie pozycji x,y dla tekstu.
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")
    # Utworzenie wykresu
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(odp[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.1*y),
                    horizontalalignment=horizontalalignment, **kw)
    # Dodanie tytułu
    ax.set_title(("[" + str(nazwa) + "] " + str(pytanie) + " Ilość odpowiedzi ["+str(iloscOdp)+"]"), bbox=dict(facecolor='white'))
    
    #Zapis wykresu do pliku
    fileName = str(hashlib.sha256(hash.encode('utf-8')).hexdigest()) + ".svg" 
    fig.savefig('/mnt/Node/svg/'+fileName)
    # Wyczyszczenie pamięci
    fig.clear()
    plt.close(fig)
    #Wysłanie pliku na serwer
    pieToTransfer = open(('/mnt/Node/svg/'+fileName), 'rb')
    try:
        pieToServer = requests.post(url, data={"IP_Address": HOST}, files={'eWybory_Statystyki_SVG': pieToTransfer})
        locPieCompile = re.compile("File location: (.*)$")
        localtionPieFile = locPieCompile.search(pieToServer.text)
        localtionPieFile = localtionPieFile.group(1)
        if(not localtionPieFile):
            localtionPieFile = "FILE_NOT_FOUND"
    finally:
        pieToTransfer.close()
    #usunięcie wykresu na lokalnym urządzeniu
    if os.path.exists('/mnt/Node/svg/'+fileName):
        os.remove('/mnt/Node/svg/'+fileName)
    return localtionPieFile + fileName

def get_Statistic_SVG_Bar(odpowiedzi, wartosci, pytanie, nazwa, iloscOdp, HOST, url):
    #Jeśli żadna odpowiedz nie została oddana, to następuje pominięcie utworzenia wykresu.
    if (len(odpowiedzi) <= 0):
        return "FILE_NOT_FOUND"
    #Wyznaczenie wartości hash, która służy jako nazwa pliku
    hash = "BAR "+str(nazwa) + str(odpowiedzi) + str(pytanie) + str(datetime.now())
    # Pozycja odpowiedzi
    x = np.arange(len(odpowiedzi))
    #Szerokość każdego ze słupków
    width = 0.35 

    fig, ax = plt.subplots()
    rects1 = ax.bar(x , wartosci, width, label=(" Ilość odpowiedzi ["+str(iloscOdp)+"]"))
    
    # Dodanie informacji, czego dotyczy osi X i Y, dla prostrzego zrozumienia wykresu
    ax.set_ylabel('Wynik [%]')
    ax.set_title((str(nazwa) + "\n" + str(pytanie)), bbox=dict(facecolor='white'))
    ax.set_xticks(x)
    ax.set_xticklabels(odpowiedzi)
    ax.legend()
    
    # Funkcja służąca do utworzenie wykresu, wraz z treścią pytania 
    def auto_label(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom')
        
    auto_label(rects1)
    fig.tight_layout()
    #Zapis wykresu do pliku
    fileName = str(hashlib.sha256(hash.encode('utf-8')).hexdigest()) + ".svg" 
    fig.savefig('/mnt/Node/svg/'+fileName)
    # Wyczyszczenie pamięci
    fig.clear()
    plt.close(fig)
    #Wysłanie pliku na serwer
    barToTransfer = open(('/mnt/Node/svg/'+fileName), 'rb')
    try:
        barToServer = requests.post(url, data={"IP_Address": HOST}, files={'eWybory_Statystyki_SVG': barToTransfer})
        locBarCompile = re.compile("File location: (.*)$")
        localtionBarFile = locBarCompile.search(barToServer.text)
        localtionBarFile = localtionBarFile.group(1)
        if(not localtionBarFile):
            localtionBarFile = "FILE_NOT_FOUND"
    finally:
        barToTransfer.close()
    #usunięcie wykresu na lokalnym urządzeniu
    if os.path.exists('/mnt/Node/svg/'+fileName):
        os.remove('/mnt/Node/svg/'+fileName)
    return localtionBarFile + fileName
      

# Funkcja służąca do przejścia przez wszystkie utworzone statystyki i dodanie lokalizacji do wykresów.
def get_All_Charts(question, stats, voting_name, url_transfer, url_error, HOST):
    statistics = json.loads(stats)
    stats_answers = []
    stats_values = []
    for (v_key, v_value) in statistics["Odpowiedzi"].items():
        if(v_key != "SumaOdpowiedzi"):
            stats_answers.append(v_key)
            stats_values.append(v_value)
    statistics["Odpowiedzi"]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Odpowiedzi"]["SumaOdpowiedzi"], HOST, url_transfer)
    statistics["Odpowiedzi"]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Odpowiedzi"]["SumaOdpowiedzi"], HOST, url_transfer)

    #Wiek = {"18-26":{"SumaOdpowiedzi":0}, "27-40":{"SumaOdpowiedzi":0}, "41-64":{"SumaOdpowiedzi":0}, "65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":countOfVotes}
    for (v_key, v_value) in statistics["Wiek"].items():            
        stats_answers = []
        stats_values = []
        if(v_key != "SumaOdpowiedzi"):
            for (odp, proc) in v_value.items():
                if(odp != "SumaOdpowiedzi"):
                    stats_answers.append(odp)
                    stats_values.append(proc)
            statistics["Wiek"][v_key]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Wiek"][v_key]["SumaOdpowiedzi"], HOST, url_transfer)
            statistics["Wiek"][v_key]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Wiek"][v_key]["SumaOdpowiedzi"], HOST, url_transfer)
    #Plec[vote[3]] = {"Odpowiedzi":{},"18-26":{"SumaOdpowiedzi":0},"27-40":{"SumaOdpowiedzi":0},"41-64":{"SumaOdpowiedzi":0},"65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0}
    for (v_key, v_value) in statistics["Plec"].items(): 
        if(v_key != "SumaOdpowiedzi"):    
            for (key_stats, val_stats) in v_value.items():
                stats_answers = []
                stats_values = []
                if(key_stats != "SumaOdpowiedzi"):
                    for (odp, proc) in  val_stats.items():
                        if(odp != "SumaOdpowiedzi"):
                            stats_answers.append(odp)
                            stats_values.append(proc)
                    if(key_stats == "Odpowiedzi"):
                        statistics["Plec"][v_key][key_stats]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Plec"][v_key]["SumaOdpowiedzi"], HOST, url_transfer)
                        statistics["Plec"][v_key][key_stats]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Plec"][v_key]["SumaOdpowiedzi"], HOST, url_transfer)
                    else:
                        statistics["Plec"][v_key][key_stats]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Plec"][v_key][key_stats]["SumaOdpowiedzi"], HOST, url_transfer)
                        statistics["Plec"][v_key][key_stats]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Plec"][v_key][key_stats]["SumaOdpowiedzi"], HOST, url_transfer)
                    
    #Woje[val] = {"Odpowiedzi":{}, "Plec":{"SumaOdpowiedzi":0}, "Wiek":{"18-26":{"SumaOdpowiedzi":0}, "27-40":{"SumaOdpowiedzi":0}, "41-64":{"SumaOdpowiedzi":0}, "65+":{"SumaOdpowiedzi":0}}, "SumaOdpowiedzi":0}
    #Woje[str(vote[5])]["Plec"][vote[3]] = {"Odpowiedzi":{},"18-26":{"SumaOdpowiedzi":0},"27-40":{"SumaOdpowiedzi":0},"41-64":{"SumaOdpowiedzi":0},"65+":{"SumaOdpowiedzi":0}, "SumaOdpowiedzi":0} 
    for (v_key, v_value) in statistics["Wojewodztwa"].items():          
        for (key_stats, val_stats) in v_value.items():
            if(key_stats == "Odpowiedzi"):
                stats_answers = []
                stats_values = []
                for (odp, proc) in  val_stats.items():
                    if(odp != "SumaOdpowiedzi"):
                        stats_answers.append(odp)
                        stats_values.append(proc)
                statistics["Wojewodztwa"][v_key][key_stats]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key]["SumaOdpowiedzi"], HOST, url_transfer)
                statistics["Wojewodztwa"][v_key][key_stats]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key]["SumaOdpowiedzi"], HOST, url_transfer)
            if(key_stats == "Wiek"):
                for przedzial, answers in val_stats.items():
                    stats_answers = []
                    stats_values = []
                    if(przedzial != "SumaOdpowiedzi"):
                        for (odp, proc) in  answers.items():
                            if(odp != "SumaOdpowiedzi"):
                                stats_answers.append(odp)
                                stats_values.append(proc)
                        statistics["Wojewodztwa"][v_key][key_stats][przedzial]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key][key_stats][przedzial]["SumaOdpowiedzi"], HOST, url_transfer)
                        statistics["Wojewodztwa"][v_key][key_stats][przedzial]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key][key_stats][przedzial]["SumaOdpowiedzi"], HOST, url_transfer)
            if(key_stats == "Plec"):
                for plec_key, plec_stats in val_stats.items():
                    if(plec_key != "SumaOdpowiedzi"):
                        for plci_stats_id, plec_stats_values in plec_stats.items():
                            stats_answers = []
                            stats_values = []
                            if(plci_stats_id != "SumaOdpowiedzi"):
                                for (odp, proc) in  plec_stats_values.items():
                                    if(odp != "SumaOdpowiedzi"):
                                        stats_answers.append(odp)
                                        stats_values.append(proc)
                                if(plci_stats_id == "Odpowiedzi"):
                                    statistics["Wojewodztwa"][v_key][key_stats][plec_key][plci_stats_id]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key][key_stats][plec_key]["SumaOdpowiedzi"], HOST, url_transfer)
                                    statistics["Wojewodztwa"][v_key][key_stats][plec_key][plci_stats_id]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key][key_stats][plec_key]["SumaOdpowiedzi"], HOST, url_transfer)
                                else:
                                    statistics["Wojewodztwa"][v_key][key_stats][plec_key][plci_stats_id]["BAR"] = get_Statistic_SVG_Bar(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key][key_stats][plec_key][plci_stats_id]["SumaOdpowiedzi"], HOST, url_transfer)
                                    statistics["Wojewodztwa"][v_key][key_stats][plec_key][plci_stats_id]["PIE"] = get_Statistic_SVG_Pie(stats_answers, stats_values, question, voting_name, statistics["Wojewodztwa"][v_key][key_stats][plec_key][plci_stats_id]["SumaOdpowiedzi"], HOST, url_transfer)
                
    return json.dumps(statistics, ensure_ascii=False)#.encode('utf8')


